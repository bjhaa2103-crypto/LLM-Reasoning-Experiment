import os
import sys
from pathlib import Path

# Locate the project folder
PROJECT_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

from dotenv import load_dotenv
from google import genai
import src.model as model

# Load API key
load_dotenv(PROJECT_ROOT / ".env")
api_key = os.getenv("GEMINI_API_KEY")

if not api_key:
    print("ERROR: API key not found.")
    sys.exit(1)

# Select the alternative model temporarily
model.MODEL_NAME = "gemini-3.6-flash"

# Create Gemini client
client = genai.Client(api_key=api_key)

question = "What is 12 multiplied by 8?"

print("Testing model:", model.MODEL_NAME)
print("Sending one test request...\n")

try:
    result = model.generate_response(
        client=client,
        question=question,
        method="Direct",
        max_retries=1
    )

    print("SUCCESS! Gemini responded.")
    print("Question:", question)
    print("Response:", result["response"])
    print("Response time:", result["response_time_seconds"], "seconds")
    print("Input tokens:", result["input_tokens"])
    print("Output tokens:", result["output_tokens"])

except Exception as error:
    print("\nAPI REQUEST FAILED.")
    print("Error type:", type(error).__name__)
    print("Error details:", str(error))

finally:
    client.close()