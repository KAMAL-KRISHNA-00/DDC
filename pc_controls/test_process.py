import psutil

def detect_teams():
    for proc in psutil.process_iter(['name', 'cmdline']):
        try:
            if proc.info['name'] and proc.info['cmdline']:
                name = proc.info['name'].lower()
                cmd = " ".join(proc.info['cmdline']).lower()

                # Microsoft Store Teams detection
                if name == "msedgewebview2.exe" and "msteams" in cmd:
                    print("Detected: Microsoft Teams (Store Version)")
                    return True

                # Desktop Teams detection (backup check)
                if name in ["ms-teams.exe", "msteams.exe", "teams.exe"]:
                    print("Detected: Microsoft Teams (Desktop Version)")
                    return True

        except (psutil.NoSuchProcess, psutil.AccessDenied):
            pass

    return False


if __name__ == "__main__":
    print("Checking for Microsoft Teams...\n")

    if detect_teams():
        print("\nTeams is running.")
    else:
        print("\nTeams is NOT running.")
