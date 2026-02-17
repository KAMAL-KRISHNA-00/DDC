from plyer import notification


def show_interrupt_notification():
    notification.notify(
        title="Door Interruption Detected",
        message="Microphone has been muted for privacy.",
        timeout=5
    )


def show_resume_notification():
    notification.notify(
        title="Meeting Resumed",
        message="Microphone can now be unmuted.",
        timeout=5
    )

def show_emergency_notification():
    notification.notify(
        title="Emergency Request Outside",
        message="Select a response (WAIT / DO NOT DISTURB).",
        timeout=5
    )
