import numpy as np
from ctypes import cast, POINTER
from comtypes import CLSCTX_ALL
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume

class VolumeControl:
    def __init__(self):
        devices = AudioUtilities.GetSpeakers()
        interface = devices.Activate(
            IAudioEndpointVolume._iid_,
            CLSCTX_ALL,
            None
        )
        self.volume = cast(interface, POINTER(IAudioEndpointVolume))
        self.minVol, self.maxVol, _ = self.volume.GetVolumeRange()

    def setVolume(self, length, min_len=30, max_len=200):
        vol = np.interp(length, [min_len, max_len],
                        [self.minVol, self.maxVol])
        self.volume.SetMasterVolumeLevel(vol, None)