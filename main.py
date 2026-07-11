"""
Android Lock Screen Monitor App
Built with Kivy - Runs as native Android APK
"""

from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput
from kivy.uix.scrollview import ScrollView
from kivy.uix.popup import Popup
from kivy.uix.spinner import Spinner
from kivy.garden.matplotlib.backend_kivyagg import FigureCanvasKivyAgg
from kivy.core.window import Window
from kivy.clock import Clock
from kivy.garden import matplotlib

import json
import os
from datetime import datetime
from pathlib import Path
import matplotlib.pyplot as plt

# Set window size for development
Window.size = (360, 640)

# Storage path for Android
STORAGE_PATH = "/sdcard/LockMonitor/attempts.json"
REPORTS_PATH = "/sdcard/LockMonitor/"

# Create directories if they don't exist
os.makedirs(os.path.dirname(STORAGE_PATH), exist_ok=True)
os.makedirs(REPORTS_PATH, exist_ok=True)


class LockScreenMonitorApp(App):
    """Main Kivy App for Lock Screen Monitoring"""
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.title = "Lock Screen Monitor"
        self.attempts = self._load_attempts()
    
    def _load_attempts(self):
        """Load previous attempts from storage"""
        if os.path.exists(STORAGE_PATH):
            try:
                with open(STORAGE_PATH, 'r') as f:
                    return json.load(f)
            except:
                return []
        return []
    
    def _save_attempts(self):
        """Save attempts to storage"""
        try:
            with open(STORAGE_PATH, 'w') as f:
                json.dump(self.attempts, f, indent=2)
        except Exception as e:
            print(f"Error saving: {e}")
    
    def build(self):
        """Build the UI"""
        main_layout = BoxLayout(orientation='vertical', padding=10, spacing=10)
        
        # Header
        header = Label(
            text='[b]Lock Screen Monitor[/b]',
            markup=True,
            size_hint_y=0.1,
            font_size='20sp'
        )
        main_layout.add_widget(header)
        
        # Tab-like navigation
        nav_layout = BoxLayout(size_hint_y=0.08, spacing=5)
        
        btn_log = Button(text='Log Attempt', background_color=(0.2, 0.6, 1, 1))
        btn_log.bind(on_press=self.show_log_screen)
        
        btn_stats = Button(text='Statistics', background_color=(0.2, 0.8, 0.2, 1))
        btn_stats.bind(on_press=self.show_stats_screen)
        
        btn_history = Button(text='History', background_color=(1, 0.6, 0.2, 1))
        btn_history.bind(on_press=self.show_history_screen)
        
        nav_layout.add_widget(btn_log)
        nav_layout.add_widget(btn_stats)
        nav_layout.add_widget(btn_history)
        
        main_layout.add_widget(nav_layout)
        
        # Content area
        self.content = BoxLayout(orientation='vertical', size_hint_y=0.82)
        main_layout.add_widget(self.content)
        
        # Show log screen by default
        self.show_log_screen(None)
        
        return main_layout
    
    def show_log_screen(self, instance):
        """Show the logging screen"""
        self.content.clear_widgets()
        
        layout = BoxLayout(orientation='vertical', spacing=10, padding=10)
        
        # Instructions
        layout.add_widget(Label(
            text='Log a Lock Attempt',
            size_hint_y=0.1,
            bold=True,
            font_size='18sp'
        ))
        
        # PIN/Code input
        pin_input = TextInput(
            multiline=False,
            hint_text='Enter PIN/Password length or code',
            size_hint_y=0.15
        )
        layout.add_widget(pin_input)
        
        # Type selector
        type_spinner = Spinner(
            text='PIN',
            values=('PIN', 'PASSWORD', 'PATTERN', 'BIOMETRIC'),
            size_hint_y=0.12
        )
        layout.add_widget(type_spinner)
        
        # Success/Failure buttons
        button_layout = GridLayout(cols=2, size_hint_y=0.15, spacing=10)
        
        btn_success = Button(
            text='✓ Success',
            background_color=(0.2, 0.8, 0.2, 1),
            font_size='16sp'
        )
        btn_success.bind(on_press=lambda x: self.log_attempt(
            pin_input.text, True, type_spinner.text
        ))
        
        btn_failed = Button(
            text='✗ Failed',
            background_color=(1, 0.2, 0.2, 1),
            font_size='16sp'
        )
        btn_failed.bind(on_press=lambda x: self.log_attempt(
            pin_input.text, False, type_spinner.text
        ))
        
        button_layout.add_widget(btn_success)
        button_layout.add_widget(btn_failed)
        layout.add_widget(button_layout)
        
        # Status label
        self.status_label = Label(
            text='Ready to log attempts',
            size_hint_y=0.2,
            markup=True
        )
        layout.add_widget(self.status_label)
        
        # Export button
        export_btn = Button(
            text='📊 Export Report',
            size_hint_y=0.1,
            background_color=(0.5, 0.5, 0.5, 1)
        )
        export_btn.bind(on_press=self.export_report)
        layout.add_widget(export_btn)
        
        self.content.add_widget(layout)
    
    def log_attempt(self, pin_code, success, attempt_type):
        """Log a lock screen attempt"""
        if not pin_code.strip():
            pin_code = "****"
        
        attempt = {
            "timestamp": datetime.now().isoformat(),
            "type": attempt_type,
            "code_length": len(pin_code),
            "success": success,
            "attempt_count": len(self.attempts) + 1
        }
        
        self.attempts.append(attempt)
        self._save_attempts()
        
        status = "[color=00ff00]✓ SUCCESS[/color]" if success else "[color=ff0000]✗ FAILED[/color]"
        msg = f"{status}\n{attempt_type} logged at {datetime.now().strftime('%H:%M:%S')}"
        
        self.status_label.text = msg
        
        # Reset after 2 seconds
        Clock.schedule_once(lambda dt: setattr(self.status_label, 'text', 'Ready to log attempts'), 2)
    
    def show_stats_screen(self, instance):
        """Show statistics screen"""
        self.content.clear_widgets()
        
        layout = BoxLayout(orientation='vertical', spacing=10, padding=10)
        
        layout.add_widget(Label(
            text='Statistics',
            size_hint_y=0.08,
            bold=True,
            font_size='18sp'
        ))
        
        if not self.attempts:
            layout.add_widget(Label(text='No attempts logged yet'))
            self.content.add_widget(layout)
            return
        
        # Calculate statistics
        total = len(self.attempts)
        successful = sum(1 for a in self.attempts if a["success"])
        failed = total - successful
        success_rate = (successful / total * 100) if total > 0 else 0
        
        # Stats display
        stats_text = f"""
[b]Total Attempts:[/b] {total}
[b]Successful:[/b] {successful}
[b]Failed:[/b] {failed}
[b]Success Rate:[/b] {success_rate:.1f}%

[b]First Attempt:[/b] {self.attempts[0]['timestamp'][:10]}
[b]Last Attempt:[/b] {self.attempts[-1]['timestamp'][:10]}

[b]Attempt Types:[/b]
"""
        
        # Count by type
        types = {}
        for attempt in self.attempts:
            t = attempt['type']
            types[t] = types.get(t, 0) + 1
        
        for attempt_type, count in types.items():
            stats_text += f"\n  {attempt_type}: {count}"
        
        stats_label = Label(
            text=stats_text,
            markup=True,
            size_hint_y=0.7
        )
        layout.add_widget(stats_label)
        
        # Chart button
        chart_btn = Button(
            text='📈 Show Chart',
            size_hint_y=0.1,
            background_color=(0.5, 0.5, 1, 1)
        )
        chart_btn.bind(on_press=self.show_chart)
        layout.add_widget(chart_btn)
        
        self.content.add_widget(layout)
    
    def show_chart(self, instance):
        """Show success/failure chart"""
        successful = sum(1 for a in self.attempts if a["success"])
        failed = sum(1 for a in self.attempts if not a["success"])
        
        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(8, 4))
        
        # Pie chart
        ax1.pie([successful, failed], labels=['Success', 'Failed'], 
                colors=['green', 'red'], autopct='%1.1f%%')
        ax1.set_title('Success Rate')
        
        # Bar chart by type
        types = {}
        for attempt in self.attempts:
            t = attempt['type']
            types[t] = types.get(t, 0) + 1
        
        ax2.bar(types.keys(), types.values(), color='steelblue')
        ax2.set_title('Attempts by Type')
        ax2.set_xlabel('Type')
        ax2.set_ylabel('Count')
        
        plt.tight_layout()
        
        # Show in popup
        chart_canvas = FigureCanvasKivyAgg(fig)
        popup = Popup(
            title='Attempt Charts',
            content=chart_canvas,
            size_hint=(0.9, 0.9)
        )
        popup.open()
    
    def show_history_screen(self, instance):
        """Show attempt history"""
        self.content.clear_widgets()
        
        layout = BoxLayout(orientation='vertical', spacing=10, padding=10)
        
        layout.add_widget(Label(
            text='Attempt History',
            size_hint_y=0.08,
            bold=True,
            font_size='18sp'
        ))
        
        if not self.attempts:
            layout.add_widget(Label(text='No attempts logged yet'))
            self.content.add_widget(layout)
            return
        
        # Scrollable history
        scroll = ScrollView(size_hint=(1, 0.92))
        
        history_layout = BoxLayout(
            orientation='vertical',
            size_hint_y=None,
            spacing=5,
            padding=5
        )
        history_layout.bind(minimum_height=history_layout.setter('height'))
        
        # Show last 20 attempts
        for attempt in reversed(self.attempts[-20:]):
            status = "✓" if attempt['success'] else "✗"
            color = "00ff00" if attempt['success'] else "ff0000"
            
            attempt_text = f"[color={color}]{status}[/color] {attempt['timestamp'][:19]} | {attempt['type']} (Len: {attempt['code_length']})"
            
            history_layout.add_widget(Label(
                text=attempt_text,
                markup=True,
                size_hint_y=None,
                height=40,
                text_size=(self.width - 20, None)
            ))
        
        scroll.add_widget(history_layout)
        layout.add_widget(scroll)
        
        # Clear history button
        clear_btn = Button(
            text='🗑️ Clear History',
            size_hint_y=0.08,
            background_color=(1, 0.5, 0.5, 1)
        )
        clear_btn.bind(on_press=self.clear_history)
        layout.add_widget(clear_btn)
        
        self.content.add_widget(layout)
    
    def clear_history(self, instance):
        """Clear all logged attempts"""
        self.attempts = []
        self._save_attempts()
        self.show_history_screen(None)
        self.status_label.text = "[color=ff6600]History cleared[/color]"
    
    def export_report(self, instance):
        """Export report to file"""
        report_file = os.path.join(REPORTS_PATH, f"report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt")
        
        with open(report_file, 'w') as f:
            f.write("=" * 60 + "\n")
            f.write("LOCK SCREEN AUTHENTICATION ATTEMPT REPORT\n")
            f.write("=" * 60 + "\n\n")
            
            total = len(self.attempts)
            successful = sum(1 for a in self.attempts if a["success"])
            failed = total - successful
            
            f.write("STATISTICS:\n")
            f.write(f"Total Attempts: {total}\n")
            f.write(f"Successful: {successful}\n")
            f.write(f"Failed: {failed}\n")
            f.write(f"Success Rate: {(successful/total*100) if total > 0 else 0:.1f}%\n\n")
            
            f.write("DETAILED ATTEMPTS:\n")
            f.write("-" * 60 + "\n")
            
            for i, attempt in enumerate(self.attempts, 1):
                status = "✓ SUCCESS" if attempt["success"] else "✗ FAILED"
                f.write(f"{i}. {status}\n")
                f.write(f"   Time: {attempt['timestamp']}\n")
                f.write(f"   Type: {attempt['type']}\n")
                f.write(f"   Code Length: {attempt['code_length']}\n\n")
        
        self.status_label.text = f"[color=00ff00]Report saved to:\n{report_file}[/color]"


if __name__ == '__main__':
    LockScreenMonitorApp().run()
