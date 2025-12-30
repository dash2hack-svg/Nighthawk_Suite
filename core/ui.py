import os
import sys
import time
import threading
import itertools
import re
from datetime import datetime

# Performance Optimization: Compiled Regex for ANSI stripping
ANSI_ESCAPE = re.compile(r'\x1B(?:[@-Z\\-_]|\[[0-?]*[ -/]*[@-~])')

# Export Control
__all__ = ['UI', 'Spinner', 'mini_banner', 'C', 'W', 'G', 'R', 'Y', 'B', 'NC', 'D']

# Initialize Windows Terminal for ANSI support
if sys.platform == "win32":
    os.system('color')

# CYBER COLOR PALETTE
C = '\033[96m'  # Cyan (Primary)
W = '\033[97m'  # White (Text)
G = '\033[92m'  # Green (Success)
R = '\033[91m'  # Red (Alert)
Y = '\033[93m'  # Yellow (Warning)
B = '\033[1m'   # Bold
NC = '\033[0m'  # Reset
D = '\033[90m'  # Dark Grey (Subtle)

def mini_banner():
    """Lightweight header used by sub-modules like EvilTwin."""
    tag = f"{C}[{W}NIGHTHAWK-MODULE{C}]{NC}"
    print(f"\n{tag} {D}—{NC} {B}AUTONOMOUS OPERATIONS{NC}")
    print(f"{D}{'━'*50}{NC}")

class UI:
    @staticmethod
    def _strip_ansi(text):
        """Helper to calculate true visible length of strings containing ANSI codes."""
        return len(ANSI_ESCAPE.sub('', str(text)))

    @staticmethod
    def banner():
        """Cross-platform terminal clearing and main framework logo."""
        os.system('cls' if os.name == 'nt' else 'clear')
        print(f"""{C}{B}
    ███╗   ██╗██╗ ██████╗ ██╗  ██╗████████╗██╗  ██╗ █████╗ ██╗    ██╗██╗  ██╗
    ████╗  ██║██║██╔════╝ ██║  ██║╚══██╔══╝██║  ██║██╔══██╗██║    ██║██║ ██╔╝
    ██╔██╗ ██║██║██║  ███╗███████║   ██║   ███████║███████║██║ █╗ ██║█████╔╝ 
    ██║╚██╗██║██║██║   ██║██╔══██║   ██║   ██╔══██║██╔══██║██║███╗██║██╔═██╗ 
    ██║ ╚████║██║╚██████╔╝██║  ██║   ██║   ██║  ██║██║  ██║╚███╔███╔╝██║  ██╗
    ╚═╝  ╚═══╝╚═╝ ╚═════╝ ╚═╝  ╚═╝   ╚═╝   ╚═╝  ╚═╝╚═╝  ╚═╝ ╚══╝╚══╝ ╚═╝  ╚═╝
         {W} GLOBAL FRAMEWORK v62.0 | {Y}AUTONOMOUS EDITION{NC}
        """)
        print(f"{D}{'═'*74}{NC}")

    @staticmethod
    def typewriter(text, speed=0.01):
        for char in text:
            sys.stdout.write(char)
            sys.stdout.flush()
            time.sleep(speed)
        print("")

    @staticmethod
    def print_box(lines, title="SYSTEM INFO"):
        width = 70
        print(f"{C}┌──[ {B}{title}{NC}{C} ]{'─'*(width-7-len(title))}┐{NC}")
        for line in lines:
            clean_len = UI._strip_ansi(line)
            padding = width - clean_len - 2
            print(f"{C}│ {W}{line}{' '*max(0, padding)}{C} │{NC}")
        print(f"{C}└{'─'*width}┘{NC}")

    @staticmethod
    def draw_table(headers, rows):
        # Calculate optimal column widths based on visible characters
        col_widths = [UI._strip_ansi(h) for h in headers]
        for row in rows:
            for i, val in enumerate(row):
                clean_len = UI._strip_ansi(val)
                if clean_len > col_widths[i]:
                    col_widths[i] = clean_len

        # Construct Header and Separator
        header_str = ""
        separator_str = ""
        for i, h in enumerate(headers):
            padding = col_widths[i] - UI._strip_ansi(h)
            header_str += f"{C} {h}{' '*padding} {D}│{NC}"
            separator_str += f"{C}{'─'*(col_widths[i]+2)}┼{NC}"
        
        # Draw Table
        print(f"{C}┌{separator_str[:-1].replace('┼', '─')}┐{NC}")
        print(f"{D}│{NC}{header_str}") 
        print(f"{C}├{separator_str[:-1]}┤{NC}")

        for row in rows:
            row_str = ""
            for i, val in enumerate(row):
                content = str(val)
                padding = col_widths[i] - UI._strip_ansi(content)
                row_str += f" {content}{' '*padding} {D}│{NC}"
            print(f"{D}│{NC}{row_str}")
        print(f"{C}└{separator_str[:-1].replace('┼', '─')}┘{NC}")

class Spinner:
    def __init__(self, message="Processing", delay=0.1):
        self.spinner = itertools.cycle(['⠋', '⠙', '⠹', '⠸', '⠼', '⠴', '⠦', '⠧', '⠇', '⠏'])
        self.delay = delay
        self.message = message
        self.running = False
        self.thread = None

    def spin(self):
        while self.running:
            sys.stdout.write(f"\r{C}[{next(self.spinner)}]{NC} {self.message}...")
            sys.stdout.flush()
            time.sleep(self.delay)
            # Efficient line clearing
            sys.stdout.write('\r' + ' ' * (UI._strip_ansi(self.message) + 10) + '\r')

    def __enter__(self):
        self.running = True
        self.thread = threading.Thread(target=self.spin, daemon=True)
        self.thread.start()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.running = False
        if self.thread:
            self.thread.join()
        sys.stdout.write(f"\r{G}[✔]{NC} {self.message} Complete.      \n")
        sys.stdout.flush()
