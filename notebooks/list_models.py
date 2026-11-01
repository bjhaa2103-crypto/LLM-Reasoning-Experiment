import os
import sys
from pathlib import Path

# Locate the project folder
PROJECT_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

from dotenv import load_dotenv
from google import genai

# Load API key
load_dotenv(PROJECT_ROOT / ".env")
api_key = os.getenv("GEMINI_API_KEY")

if not api_key:
    print("ERROR: GEMINI_API_KEY was not found in your .env file.")
    sys.exit(1)

# Create Gemini client
client = genai.Client(api_key=api_key)

try:
    print("Checking models available to your API key...\n")

    models = client.models.list()

    count = 0

    for model in models:
        supported_actions = getattr(
            model, "supported_actions", []
        ) or []

        if "generateContent" in supported_actions:
            count += 1

            print("Model name:", model.name)
            print("Display name:", getattr(model, "display_name", "N/A"))
            print("-" * 50)

    if count == 0:
        print("No models supporting generateContent were listed.")

    print(f"\nTotal compatible models listed: {count}")

except Exception as error:
    print("\nFAILED TO LIST MODELS.")
    print("Error type:", type(error).__name__)
    print("Error details:", str(error))

finally:
    client.close()