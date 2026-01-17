import asyncio
import signal
import sys
from services.capture import ScreenCapture
from services.vision import VisionBrain
from services.audio import AudioNarrator
from state import NarrativeState
import config

# Global flag for shutdown
RUNNING = True

def handle_exit(signum, frame):
    global RUNNING
    print("\nShutting down Life Narrator...")
    RUNNING = False

class LifeNarratorApp:
    def __init__(self):
        self.capture = ScreenCapture()
        self.brain = VisionBrain()
        self.audio = AudioNarrator()
        self.state = NarrativeState(max_history=config.image_history_size)
        self.queue = asyncio.Queue(maxsize=1) # Backpressure handling: Only hold 1 recent image

    async def producer_loop(self):
        """Captures screenshots periodically."""
        print("Started Vision Producer...")
        while RUNNING:
            try:
                # Capture
                img = await asyncio.to_thread(self.capture.capture)
                
                # Push to queue (non-blocking, drop if full to maintain real-time)
                if self.queue.full():
                    try:
                        self.queue.get_nowait() # Remove old
                        self.queue.task_done()
                    except asyncio.QueueEmpty:
                        pass
                
                await self.queue.put(img)
                print(f"Captured Query. Queue Size: {self.queue.qsize()}")
                
                # Wait for next interval
                await asyncio.sleep(config.SCREENSHOT_INTERVAL)
            except Exception as e:
                print(f"Producer Error: {e}")
                await asyncio.sleep(1)

    async def consumer_loop(self):
        """Consumes images and generates narration."""
        print("Started Narrative Consumer...")
        while RUNNING:
            try:
                # Get image
                img = await self.queue.get()
                
                # Analyze
                print("Analyzing frame...")
                context = self.state.get_context()
                narration = await self.brain.analyze_image(img, context)
                
                if narration:
                    print(f"Saying: {narration}")
                    self.state.add_event(narration)
                    await self.audio.speak(narration)
                
                self.queue.task_done()
                
            except Exception as e:
                print(f"Consumer Error: {e}")
                await asyncio.sleep(1)

    async def run(self):
        # Create tasks
        producer = asyncio.create_task(self.producer_loop())
        consumer = asyncio.create_task(self.consumer_loop())
        
        # Wait until stopped
        try:
            await asyncio.gather(producer, consumer)
        except asyncio.CancelledError:
            pass
        finally:
            self.audio.cleanup()

if __name__ == "__main__":
    # Handle Ctrl+C
    signal.signal(signal.SIGINT, handle_exit)
    signal.signal(signal.SIGTERM, handle_exit)

    if sys.platform == "win32":
        # Windows specific asyncio policy if needed, 
        # usually 3.8+ handles it well, but ProactorEventLoop is default.
        asyncio.set_event_loop_policy(asyncio.WindowsProactorEventLoopPolicy())

    app = LifeNarratorApp()
    try:
        asyncio.run(app.run())
    except KeyboardInterrupt:
        pass
