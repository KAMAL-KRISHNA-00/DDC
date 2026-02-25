from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume
from comtypes import CLSCTX_ALL
from ctypes import cast, POINTER


class AudioController:
    def __init__(self):
        self._mic = None
        self._initialize_microphone()

    # ---------- INITIALIZATION ----------

    def _initialize_microphone(self):
        try:
            device = AudioUtilities.GetMicrophone()
            if device is None:
                raise RuntimeError("No microphone device found")

            interface = device.Activate(
                IAudioEndpointVolume._iid_,
                CLSCTX_ALL,
                None
            )

            self._mic = cast(interface, POINTER(IAudioEndpointVolume))
            print("[Audio] Microphone initialized")

        except Exception as e:
            print(f"[Audio] Initialization failed: {e}")
            self._mic = None

    # ---------- PUBLIC METHODS ----------

    def mute(self):
        if not self._mic:
            print("[Audio] Cannot mute — microphone not available")
            return

        try:
            if not self.is_muted():
                self._mic.SetMute(1, None)
                print("[Audio] Microphone muted")
        except Exception as e:
            print(f"[Audio] Mute failed: {e}")

    def unmute(self):
        if not self._mic:
            print("[Audio] Cannot unmute — microphone not available")
            return

        try:
            if self.is_muted():
                self._mic.SetMute(0, None)
                print("[Audio] Microphone unmuted")
        except Exception as e:
            print(f"[Audio] Unmute failed: {e}")

    def is_muted(self) -> bool:
        if not self._mic:
            return False

        try:
            return bool(self._mic.GetMute())
        except Exception:
            return False