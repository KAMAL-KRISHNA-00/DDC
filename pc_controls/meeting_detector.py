import psutil


class MeetingDetector:
    TEAMS_PROCESS_NAMES = {
        "ms-teams.exe",
        "msteams.exe",
        "teams.exe"
    }

    def __init__(self):
        self._last_detected = False

    def detect_teams(self) -> bool:
        """
        Detect if Microsoft Teams is running.
        Returns True if detected.
        """

        try:
            for proc in psutil.process_iter(['name', 'cmdline']):
                name = proc.info.get('name')
                cmdline = proc.info.get('cmdline')

                if not name:
                    continue

                name = name.lower()

                # Microsoft Store version
                if name == "msedgewebview2.exe" and cmdline:
                    cmd_joined = " ".join(cmdline).lower()
                    if "msteams" in cmd_joined:
                        return True

                # Desktop versions
                if name in self.TEAMS_PROCESS_NAMES:
                    return True

        except (psutil.NoSuchProcess, psutil.AccessDenied):
            pass
        except Exception as e:
            print(f"[MeetingDetector] Error: {e}")

        return False