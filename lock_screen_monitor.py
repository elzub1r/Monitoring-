"""
Android Lock Screen PIN/Password Attempt Monitor
Captures lock screen authentication attempts with timestamps and success/failure status.
"""

import json
import logging
from datetime import datetime
from pathlib import Path
from typing import List, Dict, Optional
import subprocess

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


class LockScreenMonitor:
    """Monitor lock screen authentication attempts on Android."""
    
    def __init__(self, storage_path: str = "lock_attempts.json"):
        """
        Initialize the lock screen monitor.
        
        Args:
            storage_path: Path to store lock attempt logs
        """
        self.storage_path = Path(storage_path)
        self.attempts: List[Dict] = self._load_attempts()
        
    def _load_attempts(self) -> List[Dict]:
        """Load previous attempts from storage."""
        if self.storage_path.exists():
            try:
                with open(self.storage_path, 'r') as f:
                    return json.load(f)
            except (json.JSONDecodeError, IOError) as e:
                logger.warning(f"Could not load attempts: {e}")
                return []
        return []
    
    def _save_attempts(self) -> None:
        """Save attempts to storage."""
        try:
            with open(self.storage_path, 'w') as f:
                json.dump(self.attempts, f, indent=2)
            logger.info(f"Saved {len(self.attempts)} attempts to {self.storage_path}")
        except IOError as e:
            logger.error(f"Could not save attempts: {e}")
    
    def log_attempt(self, pin_or_code: str, success: bool, 
                   attempt_type: str = "PIN") -> None:
        """
        Log a lock screen authentication attempt.
        
        Args:
            pin_or_code: The PIN/password that was entered
            success: Whether the attempt was successful
            attempt_type: Type of attempt (PIN, PASSWORD, PATTERN, BIOMETRIC)
        """
        attempt = {
            "timestamp": datetime.now().isoformat(),
            "type": attempt_type,
            "code_length": len(pin_or_code),
            "success": success,
            "attempt_count": len(self.attempts) + 1
        }
        
        self.attempts.append(attempt)
        self._save_attempts()
        
        status = "✓ SUCCESS" if success else "✗ FAILED"
        logger.info(f"{status} - {attempt_type} attempt at {attempt['timestamp']} "
                   f"(Length: {attempt['code_length']})")
    
    def get_statistics(self) -> Dict:
        """Get statistics about lock attempts."""
        if not self.attempts:
            return {
                "total_attempts": 0,
                "successful_attempts": 0,
                "failed_attempts": 0,
                "success_rate": 0.0
            }
        
        total = len(self.attempts)
        successful = sum(1 for a in self.attempts if a["success"])
        failed = total - successful
        
        return {
            "total_attempts": total,
            "successful_attempts": successful,
            "failed_attempts": failed,
            "success_rate": (successful / total * 100) if total > 0 else 0.0,
            "first_attempt": self.attempts[0]["timestamp"],
            "last_attempt": self.attempts[-1]["timestamp"]
        }
    
    def get_attempts_summary(self, limit: int = 10) -> List[Dict]:
        """
        Get recent lock attempts summary.
        
        Args:
            limit: Number of recent attempts to return
        
        Returns:
            List of recent attempts
        """
        return self.attempts[-limit:] if self.attempts else []
    
    def get_failed_attempts(self) -> List[Dict]:
        """Get all failed lock attempts."""
        return [a for a in self.attempts if not a["success"]]
    
    def get_successful_attempts(self) -> List[Dict]:
        """Get all successful lock attempts."""
        return [a for a in self.attempts if a["success"]]
    
    def export_report(self, output_file: str = "lock_report.txt") -> None:
        """Export a human-readable report of all attempts."""
        with open(output_file, 'w') as f:
            f.write("=" * 60 + "\n")
            f.write("LOCK SCREEN AUTHENTICATION ATTEMPT REPORT\n")
            f.write("=" * 60 + "\n\n")
            
            # Statistics
            stats = self.get_statistics()
            f.write("STATISTICS:\n")
            f.write(f"Total Attempts: {stats['total_attempts']}\n")
            f.write(f"Successful: {stats['successful_attempts']}\n")
            f.write(f"Failed: {stats['failed_attempts']}\n")
            f.write(f"Success Rate: {stats['success_rate']:.1f}%\n")
            f.write(f"First Attempt: {stats.get('first_attempt', 'N/A')}\n")
            f.write(f"Last Attempt: {stats.get('last_attempt', 'N/A')}\n\n")
            
            # Detailed attempts
            f.write("DETAILED ATTEMPTS:\n")
            f.write("-" * 60 + "\n")
            
            for i, attempt in enumerate(self.attempts, 1):
                status = "✓ SUCCESS" if attempt["success"] else "✗ FAILED"
                f.write(f"{i}. {status}\n")
                f.write(f"   Time: {attempt['timestamp']}\n")
                f.write(f"   Type: {attempt['type']}\n")
                f.write(f"   Code Length: {attempt['code_length']}\n\n")
        
        logger.info(f"Report exported to {output_file}")


class AndroidLockScreenADB(LockScreenMonitor):
    """Monitor lock screen attempts using ADB (Android Debug Bridge)."""
    
    def __init__(self, storage_path: str = "lock_attempts.json"):
        """Initialize with ADB support."""
        super().__init__(storage_path)
        self.device_connected = self._check_adb_connection()
    
    def _check_adb_connection(self) -> bool:
        """Check if device is connected via ADB."""
        try:
            result = subprocess.run(['adb', 'devices'], 
                                  capture_output=True, text=True, timeout=5)
            return "device" in result.stdout and "offline" not in result.stdout
        except Exception as e:
            logger.warning(f"ADB connection check failed: {e}")
            return False
    
    def monitor_lock_screen(self) -> None:
        """Monitor lock screen events using logcat."""
        if not self.device_connected:
            logger.error("No Android device connected via ADB")
            return
        
        try:
            # Filter for authentication-related logs
            cmd = [
                'adb', 'logcat', '-s', 'KeyguardUpdateMonitor:I',
                'LockPatternKeyguardView:I', 'PasswordEntry:I'
            ]
            
            process = subprocess.Popen(cmd, stdout=subprocess.PIPE, 
                                      stderr=subprocess.PIPE, text=True)
            
            logger.info("Monitoring lock screen... Press Ctrl+C to stop")
            
            for line in process.stdout:
                self._parse_logcat_line(line)
        
        except KeyboardInterrupt:
            logger.info("Monitoring stopped by user")
        except Exception as e:
            logger.error(f"Monitoring error: {e}")


def simulate_attempts() -> None:
    """Simulate lock screen attempts for testing."""
    monitor = LockScreenMonitor("lock_attempts.json")
    
    test_cases = [
        ("1234", True, "PIN"),
        ("5678", False, "PIN"),
        ("abcdefg", True, "PASSWORD"),
        ("wrongpass", False, "PASSWORD"),
        ("1234", True, "PIN"),
        ("9999", False, "PIN"),
    ]
    
    for pin, success, attempt_type in test_cases:
        monitor.log_attempt(pin, success, attempt_type)
    
    # Print statistics
    print("\n" + "=" * 50)
    print("STATISTICS:")
    stats = monitor.get_statistics()
    for key, value in stats.items():
        print(f"{key}: {value}")
    
    # Show recent attempts
    print("\n" + "=" * 50)
    print("RECENT ATTEMPTS:")
    for attempt in monitor.get_attempts_summary(5):
        status = "✓" if attempt["success"] else "✗"
        print(f"{status} {attempt['timestamp']} - {attempt['type']} "
              f"(Length: {attempt['code_length']})")
    
    # Export report
    monitor.export_report("lock_report.txt")
    print("\nReport exported to lock_report.txt")


if __name__ == "__main__":
    # Run simulation for testing
    simulate_attempts()
