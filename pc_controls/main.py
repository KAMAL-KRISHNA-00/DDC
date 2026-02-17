import time
import keyboard
from state_machine import MeetingStateMachine
from mqtt_handler import MQTTHandler
from meeting_detector import detect_teams
from audio_controller import AudioController
from notifier import show_interrupt_notification, show_resume_notification, show_emergency_notification


state_machine = MeetingStateMachine()
mqtt_handler = MQTTHandler(state_machine)
audio = AudioController()

mqtt_handler.connect()

print("Deep-Work Digital Concierge Running...\n")

previous_state = None

previous_state = None

while True:
    meeting_active = detect_teams()
    state_machine.update_meeting_status(meeting_active)
    current_state = state_machine.get_state()

    print("State:", current_state)

    # Door interrupt → mute
    if current_state == "INTERRUPTED" and previous_state != "INTERRUPTED":
        print("→ Entered INTERRUPTED state")
        audio.mute()
        show_interrupt_notification()

    # Exit door interrupt → unmute
    if current_state == "ACTIVE_MEETING" and previous_state == "INTERRUPTED":
        print("→ Exited INTERRUPTED state")
        audio.unmute()
        show_resume_notification()

    # Emergency request → NO mute
# Emergency request → NO mute
    if current_state == "EMERGENCY_PENDING" and previous_state != "EMERGENCY_PENDING":
        print("Emergency request received.")
        print("Press W for WAIT or D for DO NOT DISTURB.")
        show_emergency_notification()


    # Handle emergency replies
    if current_state == "EMERGENCY_PENDING":
        if keyboard.is_pressed('w'):
            print("Sending WAIT response")
            mqtt_handler.client.publish("room/response", "WAIT")
            state_machine.resolve_emergency()

        if keyboard.is_pressed('d'):
            print("Sending DO_NOT_DISTURB response")
            mqtt_handler.client.publish("room/response", "DO_NOT_DISTURB")
            state_machine.resolve_emergency()

    previous_state = current_state
    mqtt_handler.publish_status()

    time.sleep(1)
