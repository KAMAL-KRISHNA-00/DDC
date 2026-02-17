from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume
from comtypes import CLSCTX_ALL
from ctypes import cast, POINTER


class AudioController:
    def __init__(self):
        # Get default microphone (capture device)
        devices = AudioUtilities.GetMicrophone()
        interface = devices.Activate(
            IAudioEndpointVolume._iid_,
            CLSCTX_ALL,
            None
        )
        self.mic = cast(interface, POINTER(IAudioEndpointVolume))

    def mute(self):
        self.mic.SetMute(1, None)
        print("Microphone muted.")

    def unmute(self):
        print("Calling unmute function...")
        self.mic.SetMute(0, None)
        print("Microphone unmuted command sent.")


    def is_muted(self):
        return self.mic.GetMute()
