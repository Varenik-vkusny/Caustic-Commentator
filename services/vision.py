import os
import asyncio
from google import genai
from google.genai import types
from PIL import Image
import config

class VisionBrain:
    def __init__(self):
        self.api_key = config.GOOGLE_API_KEY
        if not self.api_key:
            print("WARNING: GOOGLE_API_KEY not found in env.")
        
        self.client = genai.Client(api_key=self.api_key)
        # Priority list of models to try
        self.model_candidates = [
            "models/gemini-2.5-flash"
        ]
        self.current_model = None

    async def analyze_image(self, image: Image.Image, previous_context: str = "") -> str:
        if config.USE_MOCK_VISION:
            import random
            roasts = [
                "Wow, you're still staring at that same line of code? It's not going to fix itself.",
                "Opening a new tab won't solve your problems, but sure, go ahead.",
                "I see you're 'working hard'... or strictly speaking, moving the mouse aimlessly.",
                "Is that a syntax error? Embarrassing.",
                "You call this a productivity workflow? I call it a cry for help."
            ]
            print("Using Mock Vision (API connection failed previously)")
            return random.choice(roasts)

        if self.current_model:
            candidates = [self.current_model]
        else:
            candidates = self.model_candidates

        # ... (rest of the code)
        full_prompt = config.SELECTED_PERSONA
        if previous_context:
            full_prompt += f"\n\nCONTEXT (What you said last time): {previous_context}\nDon't repeat yourself if the screen hasn't changed much."

        for model in candidates:
            # ... (real api call)
            try:
                print(f"Trying VLM Model: {model}")
                response = await asyncio.to_thread(
                    self.client.models.generate_content,
                    model=model,
                    contents=[image, full_prompt],
                    config=types.GenerateContentConfig(
                        temperature=0.7,
                        top_k=40
                    )
                )
                self.current_model = model # Lock in successful model
                return response.text.strip()
            except Exception as e:
                print(f"Model {model} failed: {e}")
                # Log simplified error
                continue
        
        return "I'm blind! No models are working for me right now."
