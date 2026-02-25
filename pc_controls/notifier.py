from plyer import notification


class Notifier:
    DEFAULT_TIMEOUT = 5

    @staticmethod
    def _notify(title: str, message: str, timeout: int = DEFAULT_TIMEOUT):
        try:
            notification.notify(
                title=title,
                message=message,
                timeout=timeout
            )
        except Exception as e:
            print(f"[Notifier] Failed to send notification: {e}")

    # ---------- PUBLIC METHODS ----------

    @classmethod
    def interrupt(cls):
        cls._notify(
            title="Door Interruption Detected",
            message="Microphone has been muted for privacy."
        )

    @classmethod
    def resume(cls):
        cls._notify(
            title="Meeting Resumed",
            message="Microphone can now be unmuted."
        )

    @classmethod
    def emergency(cls):
        cls._notify(
            title="Emergency Request Outside",
            message="Select a response (WAIT / DO NOT DISTURB)."
        )