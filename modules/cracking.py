import subprocess, os, time, sys, re, shutil
from pathlib import Path
from core.ui import UI, C, W, R, G, B, NC, Y, D

class HandshakeCracker:
    def __init__(self, proj_dir):
        self.path = Path(proj_dir)
        self.history_file = Path.home() / "Nighthawk_Suite" / "success_patterns.txt"
        self.cap_files = []
        self.priority_years = [str(time.strftime("%Y")), str(int(time.strftime("%Y"))-1)]
        self.seasons = ["Spring", "Summer", "Autumn", "Winter"]

    def find_caps(self):
        self.cap_files = []
        if self.path.exists():
            self.cap_files = list(self.path.glob("*.cap"))
        return self.cap_files

    def load_learned_patterns(self):
        patterns = set()
        if self.history_file.exists():
            with open(self.history_file, 'r') as f:
                patterns.update([line.strip() for line in f if line.strip()])
        return patterns

    def save_success(self, password):
        # Ensure parent dir exists
        self.history_file.parent.mkdir(parents=True, exist_ok=True)
        with open(self.history_file, 'a') as f:
            f.write(f"{password}\n")

    def convert_to_hashcat(self, cap_path):
        cap_path = Path(cap_path)
        hc_path = cap_path.with_suffix(".hc22000")
        
        # Check for conversion tool (Linux mostly)
        if shutil.which("hcxpcapngtool"):
            subprocess.run(f"hcxpcapngtool -o {hc_path} {cap_path}", shell=True, stdout=subprocess.DEVNULL)
            return hc_path
        # Return path anyway if user manually converted it, or return None
        return hc_path if hc_path.exists() else None

    def generate_warp_list(self, essid):
        print(f"\n{C}[*] WARP ENGINE: Analyzing Patterns for '{essid}'...{NC}")
        clean = essid.replace("-", "").replace("_", "").replace(" ", "")
        keywords = {clean, clean.lower(), clean.title()}
        
        parts = re.findall(r'[A-Z][a-z]*', essid) or [essid]
        for p in parts:
            keywords.add(p); keywords.add(p.lower())

        passwords = self.load_learned_patterns()
        
        for k in keywords:
            for y in self.priority_years:
                passwords.add(f"{k}{y}"); passwords.add(f"{k}{y}!")
            passwords.add(f"{k}123"); passwords.add(f"{k}!"); passwords.add("Password123")

        list_path = self.path / f"warp_{clean}.txt"
        with open(list_path, "w") as f:
            f.write('\n'.join(passwords))
        return list_path

    def run(self):
        while True:
            UI.banner()
            caps = self.find_caps()
            if not caps:
                UI.print_box(["NO CAPTURES FOUND", f"Scan Dir: {self.path}"], title="WAR ROOM EMPTY")
                input(f"{W}Press Enter...{NC}"); return

            UI.print_box(["SELECT TARGET CAPTURE"], title="HASHCAT MASTER ENGINE")
            for i, f in enumerate(caps): print(f" {C}[{i}]{NC} {W}{f.name}{NC}")

            try:
                sel = input(f"\n {B}Target{NC} {C}»{NC} ")
                if not sel: return
                target_cap = caps[int(sel)]
                target_essid = target_cap.stem.split("-01")[0].replace("_", " ")
            except: continue

            hc_file = self.convert_to_hashcat(target_cap)
            
            UI.banner()
            print(f"{G} [ WORLD-CLASS HASH CRACKING ]{NC}")
            print(f" {C}1.{NC} {G}Warp-Drive (15m){NC}  {D}:: Learning-Mode Enabled{NC}")
            print(f" {C}2.{NC} {W}Standard Brute{NC}     {D}:: RockYou List{NC}")

            m = input(f"\n {B}Execute{NC} {C}»{NC} ")
            found = False
            password = None

            if m == '1' and hc_file:
                wlist = self.generate_warp_list(target_essid)
                pot = self.path / "temp.pot"
                
                # Check if hashcat is installed
                if not shutil.which("hashcat"):
                    print(f"{R}[!] Hashcat not found in PATH.{NC}")
                    input(); break

                cmd = f"hashcat -m 22000 -a 0 {hc_file} {wlist} --outfile={pot} --outfile-format=2 --force"
                os.system(cmd)
                
                if pot.exists() and pot.stat().st_size > 0:
                    with open(pot, 'r') as f: password = f.read().strip()
                    found = True; pot.unlink()

            if found:
                print(f"\n{G}{B} [!!!] SUCCESS: {password} [!!!] {NC}")
                self.save_success(password)
                with open(self.path / "CRACKED.txt", "a") as f: 
                    f.write(f"{target_essid}:{password}\n")
            else:
                print(f"\n{R}[!] Audit Failed.{NC}")
            
            input(f"\n{W}Press Enter to return to menu...{NC}")
            break
