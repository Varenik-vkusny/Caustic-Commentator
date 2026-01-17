import asyncio
import edge_tts
import pygame
import os
import uuid

class AudioNarrator:
    def __init__(self):
        pygame.mixer.init()
        self.voice = "ru-RU-DmitryNeural" # Russian Male Voice
        # self.voice = "en-US-AriaNeural" # Female voice
        self.output_dir = "temp_audio"
        os.makedirs(self.output_dir, exist_ok=True)

    async def speak(self, text: str):
        """Generates TTS and plays it."""
        if not text:
            return

        filename = os.path.join(self.output_dir, f"{uuid.uuid4()}.mp3")
        
        # Determine duration roughly for logging
        print(f"Narrator: {text}")

        # Generate Audio
        communicate = edge_tts.Communicate(text, self.voice)
        await communicate.save(filename)

        # Play Audio
        # We run this in a thread or just block slightly if it's main loop? 
        # Since pygame play is async-ish (it just loads), the waiting happens if we want to block.
        # For a narrator, we generally want to queue them or just play immediately if channel free.
        
        if pygame.mixer.music.get_busy():
             # If something is already playing, wait for it loop to finish or stop?
             # User wants it to finish.
             pass

        self.play_audio(filename)
        
        # Wait for audio to finish playing
        while pygame.mixer.music.get_busy():
             await asyncio.sleep(0.5)

    def play_audio(self, filename):
        try:
            pygame.mixer.music.load(filename)
            pygame.mixer.music.play()
            
            # Implementation Detail: We need to keep the event loop alive or managing this.
            # In a real async app we might fire and forget, but we need to cleanup files.
            # For MVP, we'll leave files or clean up on exit.
            
        except Exception as e:
            print(f"Audio Error: {e}")

    def cleanup(self):
        pygame.mixer.quit()
        # Remove temp files
        for f in os.listdir(self.output_dir):
            try:
                os.remove(os.path.join(self.output_dir, f))
            except:
                pass
