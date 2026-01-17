from google import genai
import os
from dotenv import load_dotenv
from PIL import Image

load_dotenv()
api_key = os.getenv("GOOGLE_API_KEY")
client = genai.Client(api_key=api_key)

img = Image.new("RGB", (100, 100), color="red")

models = ["models/gemini-2.0-flash"]

print("Starting Model Check...")

for m in models:
    print(f"\nTesting: {m}...")
    try:
        response = client.models.generate_content(
            model=m, contents=[img, "What color is this?"]
        )
        print(f"SUCCESS: {m}")
        print(f"Response: {response.text}")
        break
    except Exception as e:
        print(f"FAILED: {m}")
        print(f"Error: {e}")
