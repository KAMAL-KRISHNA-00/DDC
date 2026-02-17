import psutil

def detect_teams():
    for proc in psutil.process_iter(['name', 'cmdline']):
        try:
            if proc.info['name'] and proc.info['cmdline']:
                name = proc.info['name'].lower()
                cmd = " ".join(proc.info['cmdline']).lower()

                if name == "msedgewebview2.exe" and "msteams" in cmd:
                    return True

                if name in ["ms-teams.exe", "msteams.exe", "teams.exe"]:
                    return True

        except (psutil.NoSuchProcess, psutil.AccessDenied):
            pass

    return False
