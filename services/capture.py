import mss
import mss.tools
from PIL import Image
import io

class ScreenCapture:
    def __init__(self):
        # We don't initialize mss here because it's not thread-safe to share 
        # the instance across the asyncio executor threads.
        pass

    def capture(self):
        """Captures the screen and returns a PIL Image object."""
        with mss.mss() as sct:
            # Capture the first monitor (monitor 1 is usually the primary)
            # monitor[0] is 'all monitors combined'
            monitor = sct.monitors[1] 
            
            sct_img = sct.grab(monitor)
            img = Image.frombytes("RGB", sct_img.size, sct_img.bgra, "raw", "BGRX")
            
            # Resize for performance/latency
            img.thumbnail((1024, 1024)) 
            return img
