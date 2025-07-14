import os
import google.generativeai as genai
from dotenv import load_dotenv
from pathlib import Path

load_dotenv()

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
if not GEMINI_API_KEY:
    raise ValueError("GEMINI_API_KEY is missing in .env file.")

genai.configure(api_key=GEMINI_API_KEY)


def load_user_raw_text(username: str) -> str:
    """Loads raw Reddit content from local file."""
    filepath = f"raw_data/{username}_raw.txt"
    if not os.path.exists(filepath):
        raise FileNotFoundError(f"No raw data found for {username}")
    with open(filepath, "r", encoding="utf-8") as f:
        return f.read()

def generate_persona(raw_text: str, username: str) -> str:
    """
    Generates a user persona using Gemini with logging and retry logic.
    """
    try:
        model = genai.GenerativeModel("gemini-pro")

        prompt = f"""
You are a social profiling AI assistant. Based on the following Reddit posts and comments from the user u/{username}, generate a detailed user persona.

Include:
- Interests
- Tone and style of writing
- Behavioral patterns
- Political/social views (if any)
- Short quotes from their posts or comments as citations

Reddit data:
{raw_text}
"""

        # Validate chunk size (Gemini limit ~30k chars)
        if len(prompt) > 28000:
            prompt = prompt[:28000]
            print("⚠️ Prompt truncated to fit token limit.")

        response = model.generate_content(prompt)

        if hasattr(response, "text") and response.text.strip():
            return response.text.strip()
        else:
            print("❌ Gemini returned no usable text.")
            return "❌ Gemini API returned no usable response."

    except Exception as e:
        print(f"❌ Gemini API Error: {e}")
        return f"❌ Gemini API Error: {e}"


def save_persona(username: str, persona_text: str):
    """Saves persona to local file."""
    Path("personas").mkdir(exist_ok=True)
    filepath = f"personas/{username}_persona.txt"
    with open(filepath, "w", encoding="utf-8") as f:
        f.write(persona_text)
    print(f"✅ Persona saved to: {filepath}")

    return filepath