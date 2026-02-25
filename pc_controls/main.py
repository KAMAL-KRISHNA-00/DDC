import time
import keyboard

from state_machine import MeetingStateMachine
from mqtt_handler import MQTTHandler
from meeting_detector import MeetingDetector
from audio_controller import AudioController
from notifier import Notifier


class DeepWorkController:
    LOOP_INTERVAL = 1  # seconds

    def __init__(self):
        self.state_machine = MeetingStateMachine()
        self.mqtt_handler = MQTTHandler(self.state_machine)
        self.audio = AudioController()
        self.detector = MeetingDetector()

        self.previous_state = None

    # ---------- STARTUP ----------

    def start(self):
        print("Deep-Work Digital Concierge Running...\n")
        self.mqtt_handler.connect()

        try:
            while True:
                self._update()
                time.sleep(self.LOOP_INTERVAL)

        except KeyboardInterrupt:
            print("\nShutting down safely...")

    # ---------- MAIN UPDATE LOOP ----------

    def _update(self):
        meeting_active = self.detector.detect_teams()
        self.state_machine.update_meeting_status(meeting_active)

        current_state = self.state_machine.get_state()
        print("State:", current_state)

        self._handle_state_transitions(current_state)
        self._handle_emergency_input(current_state)

        self.previous_state = current_state
        self.mqtt_handler.publish_status()

    # ---------- STATE TRANSITIONS ----------

    def _handle_state_transitions(self, current_state):

        # Enter INTERRUPTED
        if current_state == "INTERRUPTED" and self.previous_state != "INTERRUPTED":
            print("→ Entered INTERRUPTED state")
            self.audio.mute()
            Notifier.interrupt()

        # Exit INTERRUPTED
        if current_state == "ACTIVE_MEETING" and self.previous_state == "INTERRUPTED":
            print("→ Exited INTERRUPTED state")
            self.audio.unmute()
            Notifier.resume()

        # Emergency received
        if current_state == "EMERGENCY_PENDING" and self.previous_state != "EMERGENCY_PENDING":
            print("Emergency request received.")
            print("Press W for WAIT or D for DO NOT DISTURB.")
            Notifier.emergency()

    # ---------- EMERGENCY RESPONSE ----------

    def _handle_emergency_input(self, current_state):

        if current_state != "EMERGENCY_PENDING":
            return

        if keyboard.is_pressed('w'):
            print("Sending WAIT response")
            self.mqtt_handler.client.publish("room/response", "WAIT")
            self.state_machine.resolve_emergency()

        elif keyboard.is_pressed('d'):
            print("Sending DO_NOT_DISTURB response")
            self.mqtt_handler.client.publish("room/response", "DO_NOT_DISTURB")
            self.state_machine.resolve_emergency()


if __name__ == "__main__":
    app = DeepWorkController()
    app.start()