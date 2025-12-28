import os, sys, time, threading, itertools
from datetime import datetime

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

class UI:
    @staticmethod
    def banner():
        """Cross-platform terminal clearing for v62.0 Evolution."""
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
            # Enhanced color-safe length calculation
            clean = line
            for code in [C, W, G, R, Y, B, NC, D]:
                clean = clean.replace(code, '')
            padding = width - len(clean) - 2
            print(f"{C}│ {W}{line}{' '*padding}{C} │{NC}")
        print(f"{C}└{'─'*width}┘{NC}")

    @staticmethod
    def draw_table(headers, rows):
        col_widths = [len(h) for h in headers]
        for row in rows:
            for i, val in enumerate(row):
                clean_len = len(str(val).replace(C,'').replace(W,'').replace(NC,'').replace(G,'').replace(R,'').replace(Y,'').replace(D,''))
                if clean_len > col_widths[i]:
                    col_widths[i] = clean_len

        header_str = ""
        separator_str = ""
        for i, h in enumerate(headers):
            header_str += f"{C} {h:<{col_widths[i]}} {D}│{NC}"
            separator_str += f"{C}{'─'*(col_widths[i]+2)}┼{NC}"
        
        print(f"{C}┌{separator_str[:-1].replace('┼', '─')}{'─'*10}┐{NC}")
        print(f"{D}│{NC}{header_str}") 
        print(f"{C}├{separator_str[:-1]}┤{NC}")

        for row in rows:
            row_str = ""
            for i, val in enumerate(row):
                content = str(val)
                clean_content = content.replace(C,'').replace(W,'').replace(NC,'').replace(G,'').replace(R,'').replace(Y,'').replace(D,'')
                padding = col_widths[i] - len(clean_content)
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
            sys.stdout.write('\b' * (len(self.message) + 10))

    def __enter__(self):
        self.running = True
        self.thread = threading.Thread(target=self.spin)
        self.thread.start()

    def __exit__(self, exception, value, tb):
        self.running = False
        self.thread.join()
        sys.stdout.write(f"\r{G}[✔]{NC} {self.message} Complete.      \n")
        sys.stdout.flush()

    def mini_banner():
    print('--- Nighthawk ---')
