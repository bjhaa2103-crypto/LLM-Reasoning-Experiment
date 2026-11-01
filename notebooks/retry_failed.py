import os
import sys
import time
import pandas as pd
from pathlib import Path
from dotenv import load_dotenv
from google import genai

# Locate project folder
PROJECT_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

import src.model as model

# File paths
INPUT_FILE = PROJECT_ROOT / "results" / "results.csv"
OUTPUT_FILE = PROJECT_ROOT / "results" / "results_recovered.csv"

# Select alternative model for failed requests
RETRY_MODEL = "gemini-3.6-flash"

# Load API key
load_dotenv(PROJECT_ROOT / ".env")
api_key = os.getenv("GEMINI_API_KEY")

if not api_key:
    print("ERROR: API key not found in .env")
    sys.exit(1)

# Check input file
if not INPUT_FILE.exists():
    print("ERROR: results.csv not found.")
    sys.exit(1)

# Read original results
df = pd.read_csv(INPUT_FILE)

# Add model tracking column
if "model_used" not in df.columns:
    df["model_used"] = "gemini-3.8-flash"

# Make sure the columns we overwrite can hold text and mixed values
for col in ["response", "status", "model_used"]:
    if col in df.columns:
        df[col] = df[col].astype(object)

# Identify failed requests
failed_indices = df.index[
    df["status"].astype(str).str.strip().str.lower() == "failed"
].tolist()

print("Original total requests:", len(df))
print("Successful requests:", (df["status"] == "Success").sum())
print("Failed requests:", len(failed_indices))
print("Retry model:", RETRY_MODEL)

if not failed_indices:
    print("\nNo failed requests found.")
    sys.exit(0)

# Confirm before sending requests
confirm = input(
    "\nDo you want to retry these failed requests? (yes/no): "
)

if confirm.strip().lower() != "yes":
    print("Retry cancelled. Original results remain unchanged.")
    sys.exit(0)

# Set model for retry requests
model.MODEL_NAME = RETRY_MODEL

# Create Gemini client
client = genai.Client(api_key=api_key)

try:
    for position, index in enumerate(failed_indices, start=1):

        row = df.loc[index]

        print("\n" + "=" * 50)
        print(f"Retrying {position}/{len(failed_indices)}")
        print("Question ID:", row["id"])
        print("Method:", row["method"])

        try:
            result = model.generate_response(
                client=client,
                question=row["question"],
                method=row["method"],
                max_retries=1
            )

            # Update only this failed row
            df.at[index, "response"] = result["response"]
            df.at[index, "response_time_seconds"] = (
                result["response_time_seconds"]
            )
            df.at[index, "total_elapsed_seconds"] = (
                result["total_elapsed_seconds"]
            )
            df.at[index, "input_tokens"] = result["input_tokens"]
            df.at[index, "output_tokens"] = result["output_tokens"]
            df.at[index, "status"] = "Success"
            df.at[index, "model_used"] = RETRY_MODEL

            print("SUCCESS:", result["response"])

        except Exception as error:
            print("FAILED:", str(error))

            # Keep the failed status
            df.at[index, "model_used"] = RETRY_MODEL

        # Save after every request
        df.to_csv(OUTPUT_FILE, index=False)

        # Small pause between requests
        if position < len(failed_indices):
            time.sleep(3)

finally:
    client.close()

print("\n" + "=" * 50)
print("RETRY PROCESS COMPLETED")
print("Total requests:", len(df))
print("Successful requests:", (df["status"] == "Success").sum())
print(
    "Failed requests:",
    (df["status"].astype(str).str.strip().str.lower() == "failed").sum()
)
print("\nRecovered results saved to:")
print(OUTPUT_FILE)