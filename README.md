# The Real-Time Life Narrator - Project Guide

## 1. The Architecture (High Level)
To prevent the UI from freezing while waiting for the AI, we use an **Asynchronous Producer-Consumer** pattern with `asyncio`.

*   **The Producer (Eye)**: A lightweight loop that takes a screenshot every ~15 seconds. It pushes these images into a `Queue`.
    *   *Optimization*: Use a `Queue(maxsize=1)`. If the AI is slow, we drop old frames. We only care about the *latest* reality.
*   **The Consumer (Brain)**: Pulls the latest image, sends it to the VLM (Vision-Language Model).
*   **The Voice (Mouth)**: The Brain receives text, sends it to the TTS service, and plays the audio.

## 2. The Tech Stack
*   **Screen Capture**: `mss` (Thread-safe implementation).
*   **State Management**: `collections.deque` (Python standard lib).
*   **Audio Playback**: `edge-tts` (Free Neural Voices) + `pygame`. 
*   **Inference**: `google-genai` (Gemini).

## 3. Important Implementation Details
### The "Roast" Persona
Located in `config.py`, the **"Roast Master 9000"** is designed to be cynical.
> "Oh, look at you, staring at a syntax error on line 42 for the past ten minutes. Riveting."

### MOCK Mode (Current Status)
During testing, we discovered your Google API Key is encountering `404 Not Found` (for 1.5 Flash) and `429 Quota Exhausted` (for 2.0 Flash) errors.
To ensure you have a working application, I have enabled **Mock Mode** in `config.py`.
```python
USE_MOCK_VISION = True 
```
The app will "see" your screen but reply with pre-written sarcastic lines to demonstrate the full pipeline (Capture -> processing -> Speech) works.

**To Enable Real AI:**
1.  Get a valid Google API Key (ensure Billing is enabled if using Pro, or use a fresh Free Tier account).
2.  Set `USE_MOCK_VISION = False` in `config.py`.
3.  The app uses a strict Fallback mechanism in `services/vision.py` to try `gemini-1.5-flash`, `gemini-2.0-flash-exp`, and others automatically.

## How to Run
```powershell
pi install -r requirements.txt
python main.py
```
Press `Ctrl+C` to stop.
