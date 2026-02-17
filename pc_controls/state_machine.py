import time

class MeetingStateMachine:
    def __init__(self):
        self.state = "IDLE"
        self.last_interrupt_time = 0
        self.interrupt_timeout = 10

    def update_meeting_status(self, meeting_active):
        if self.state == "EMERGENCY_PENDING":
            return

        # Timeout recovery only for INTERRUPTED
        if self.state == "INTERRUPTED":
            if time.time() - self.last_interrupt_time > self.interrupt_timeout:
                if meeting_active:
                    self.state = "ACTIVE_MEETING"
                else:
                    self.state = "IDLE"
            return

        # Normal meeting transitions
        if meeting_active and self.state == "IDLE":
            self.state = "ACTIVE_MEETING"
        elif not meeting_active:
            self.state = "IDLE"

    def door_interrupt(self):
        if self.state == "ACTIVE_MEETING":
            self.state = "INTERRUPTED"
            self.last_interrupt_time = time.time()
            return True
        return False

    def emergency_request(self):
        if self.state == "ACTIVE_MEETING":
            self.state = "EMERGENCY_PENDING"
            return True
        return False

    def resolve_emergency(self):
        if self.state == "EMERGENCY_PENDING":
            self.state = "ACTIVE_MEETING"

    def get_state(self):
        return self.state
