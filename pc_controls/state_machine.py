import time


class MeetingStateMachine:
    # ----- STATES -----
    IDLE = "IDLE"
    ACTIVE_MEETING = "ACTIVE_MEETING"
    INTERRUPTED = "INTERRUPTED"
    EMERGENCY_PENDING = "EMERGENCY_PENDING"

    def __init__(self, interrupt_timeout=10):
        self._state = self.IDLE
        self._last_interrupt_time = 0
        self._interrupt_timeout = interrupt_timeout

    # ----- PUBLIC METHODS -----

    def update_meeting_status(self, meeting_active: bool):
        """
        Handles automatic state transitions based on meeting detection.
        """

        # Emergency state blocks auto transitions
        if self._state == self.EMERGENCY_PENDING:
            return

        # Handle interrupt timeout recovery
        if self._state == self.INTERRUPTED:
            if self._interrupt_expired():
                self._state = (
                    self.ACTIVE_MEETING if meeting_active else self.IDLE
                )
            return

        # Normal meeting transitions
        if meeting_active and self._state == self.IDLE:
            self._state = self.ACTIVE_MEETING

        elif not meeting_active:
            self._state = self.IDLE

    def door_interrupt(self) -> bool:
        """
        Triggered by reed switch event.
        Returns True if transition occurred.
        """
        if self._state == self.ACTIVE_MEETING:
            self._state = self.INTERRUPTED
            self._last_interrupt_time = time.time()
            return True
        return False

    def emergency_request(self) -> bool:
        """
        Triggered by emergency button.
        Returns True if transition occurred.
        """
        if self._state == self.ACTIVE_MEETING:
            self._state = self.EMERGENCY_PENDING
            return True
        return False

    def resolve_emergency(self):
        """
        Resolves emergency state.
        """
        if self._state == self.EMERGENCY_PENDING:
            self._state = self.ACTIVE_MEETING

    def get_state(self) -> str:
        return self._state

    # ----- INTERNAL METHODS -----

    def _interrupt_expired(self) -> bool:
        return (time.time() - self._last_interrupt_time) > self._interrupt_timeout