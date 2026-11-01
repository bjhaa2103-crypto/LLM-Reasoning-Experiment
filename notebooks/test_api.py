import os
import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

from dotenv import load_dotenv
from google import genai
from src.model import generate_response, MODEL_NAME

load_dotenv(PROJECT_ROOT / ".env")
api_key = os.getenv("GEMINI_API_KEY")

if not api_key:
    print("ERROR: GEMINI_API_KEY was not found in your .env file.")
    sys.exit(1)

client = genai.Client(api_key=api_key)

question = "What is 12 multiplied by 8?"

print(f"Testing Gemini model: {MODEL_NAME}")
print("Sending one test request...")

try:
    result = generate_response(
        client=client,
        question=question,
        method="Direct",
        max_retries=1
    )

    print("\nSUCCESS! Gemini responded.")
    print("Question:", question)
    print("Response:", result["response"])
    print("Response time:", result["response_time_seconds"], "seconds")
    print("Input tokens:", result["input_tokens"])
    print("Output tokens:", result["output_tokens"])

except Exception as error:
    print("\nAPI REQUEST FAILED.")
    print("Error type:", type(error).__name__)
    print("Error details:", str(error))