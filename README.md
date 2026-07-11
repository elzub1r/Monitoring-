# Lock Screen Monitor - Android APK

A Kivy-based Android application for monitoring and logging lock screen PIN/password attempts with timestamps and success/failure status.

## Features

✅ **Log Attempts** - Record PIN/password attempts with timestamp  
✅ **Track Status** - Mark each attempt as success or failed  
✅ **Statistics** - View success rate and attempt analysis  
✅ **History** - Review all logged attempts with details  
✅ **Charts** - Visual representation of attempts and success rate  
✅ **Export Reports** - Save detailed reports to file  
✅ **Local Storage** - All data stored locally on Android device  

## Files

- `main.py` - Main Kivy application
- `lock_screen_monitor.py` - Core monitoring logic (Python script version)
- `buildozer.spec` - APK build configuration
- `requirements.txt` - Python dependencies

## How to Build APK

### Prerequisites

1. **Install Python 3.9+** - https://www.python.org/downloads/
2. **Install Java JDK** - https://adoptopenjdk.net/
3. **Install Android SDK** - https://developer.android.com/studio
4. **Install Buildozer** - `pip install buildozer`
5. **Install Cython** - `pip install cython`

### Step-by-Step Build Instructions

#### Windows

```bash
# 1. Clone the repository
git clone https://github.com/elzub1r/Monitoring-
cd Monitoring-

# 2. Install buildozer and dependencies
pip install buildozer cython kivy

# 3. Set environment variables (adjust paths to your installation)
set JAVA_HOME=C:\Program Files\Java\jdk-17.0.1
set ANDROID_SDK_ROOT=C:\Android\Sdk
set ANDROID_NDK_ROOT=C:\Android\Ndk\25b

# 4. Build the APK
buildozer -v android debug

# 5. APK will be generated in bin/ folder
# Example: bin/lockmonitor-1.0.0-debug.apk
```

#### Mac

```bash
# 1. Clone the repository
git clone https://github.com/elzub1r/Monitoring-
cd Monitoring-

# 2. Install buildozer
pip install buildozer cython

# 3. Set environment variables
export JAVA_HOME=$(/usr/libexec/java_home)
export ANDROID_SDK_ROOT=~/Library/Android/sdk
export ANDROID_NDK_ROOT=~/Library/Android/ndk/25b

# 4. Build the APK
buildozer -v android debug

# 5. APK will be in bin/ folder
```

#### Linux (Ubuntu/Debian)

```bash
# 1. Install dependencies
sudo apt-get install -y python3-pip openjdk-11-jdk-headless

# 2. Clone the repository
git clone https://github.com/elzub1r/Monitoring-
cd Monitoring-

# 3. Install buildozer
pip install buildozer cython

# 4. Set environment variables
export JAVA_HOME=/usr/lib/jvm/java-11-openjdk-amd64
export ANDROID_SDK_ROOT=~/Android/Sdk
export ANDROID_NDK_ROOT=~/Android/Ndk/25b

# 5. Build the APK
buildozer -v android debug

# 6. APK will be in bin/ folder
```

### Using Docker (Easiest Method)

If you have Docker installed, you can use the buildozer Docker image:

```bash
docker run -v $(pwd):/workspace -it kivy/kivy:latest bash
cd /workspace
buildozer -v android debug
```

## Installation on Android

### Option 1: Install from APK

1. Enable "Unknown Sources" in Settings > Security
2. Transfer `lockmonitor-1.0.0-debug.apk` to your Android device
3. Open the APK file and tap "Install"
4. Grant permissions when prompted
5. Open the app from your app drawer

### Option 2: Install via ADB

```bash
adb install bin/lockmonitor-1.0.0-debug.apk
```

### Option 3: Build and Install Directly

```bash
buildozer -v android debug deploy run
```

This will build and automatically install the app on your connected device.

## Usage

### Log Screen
- Enter PIN/password length
- Select attempt type (PIN, PASSWORD, PATTERN, BIOMETRIC)
- Click ✓ Success or ✗ Failed
- Status will show confirmation

### Statistics Screen
- View total attempts count
- See success/failure breakdown
- Check success rate percentage
- View attempts by type
- Click "Show Chart" for visual graphs

### History Screen
- Review all logged attempts
- Each entry shows timestamp, type, and code length
- Scroll through up to 20 recent attempts
- Click "Clear History" to reset all data

### Export Report
- Click "📊 Export Report" from log screen
- Report saves to `/sdcard/LockMonitor/`
- Contains full statistics and detailed attempt log

## Data Storage

All data is stored locally on your Android device at:
```
/sdcard/LockMonitor/attempts.json
```

No data is sent to external servers. All monitoring is done locally.

## Permissions Required

- **WRITE_EXTERNAL_STORAGE** - Save reports
- **READ_EXTERNAL_STORAGE** - Access saved data
- **INTERNET** - (Optional) For future cloud features

## Troubleshooting

### APK Build Fails
- Ensure all dependencies are installed: `pip install -r requirements.txt`
- Update buildozer: `pip install --upgrade buildozer`
- Clear build cache: `buildozer android clean`

### App Crashes on Startup
- Grant storage permissions in Settings
- Ensure `/sdcard/LockMonitor/` directory exists
- Check Android version (requires API 21+)

### Can't Find APK After Build
- Check `bin/` directory in your project folder
- Run with verbose flag: `buildozer -v android debug`

## Building Release APK

For production/release version:

```bash
# Generate keystore (one time only)
keytool -genkey -v -keystore my-release-key.keystore -keyalg RSA -keysize 2048 -validity 10000 -alias my-key-alias

# Update buildozer.spec with keystore info
# Then build release APK:
buildozer -v android release
```

## Future Enhancements

- Real-time lock screen event capture via accessibility service
- Cloud sync for attempt logs
- Multi-device monitoring
- Advanced analytics dashboard
- Biometric attempt logging
- Custom alert notifications

## License

This project is open source and available for educational and authorized monitoring purposes only.

## Support

For issues or questions:
1. Check the troubleshooting section above
2. Review buildozer documentation: https://buildozer.readthedocs.io/
3. Open an issue on GitHub

## Important Notes

⚠️ **Legal Disclaimer**: This tool is intended for personal use on devices you own or have explicit authorization to monitor. Use responsibly and in compliance with all local laws and regulations.

---

**Version**: 1.0.0  
**Last Updated**: 2026-07-11  
**Repository**: https://github.com/elzub1r/Monitoring-
