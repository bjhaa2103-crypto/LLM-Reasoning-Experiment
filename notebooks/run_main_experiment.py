import os
import sys
import time
import pandas as pd

from pathlib import Path
from dotenv import load_dotenv
from google import genai

# Add project root to Python path
PROJECT_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

import src.model as model


# --------------------------------------------------
# 1. CONFIGURATION
# --------------------------------------------------

load_dotenv(PROJECT_ROOT / ".env")

API_KEY = os.getenv("GEMINI_API_KEY")

if not API_KEY:
    raise ValueError("GEMINI_API_KEY not found in .env file")

# Use one model throughout the main experiment
model.MODEL_NAME = "gemini-3.6-flash"

client = genai.Client(api_key=API_KEY)

INPUT_FILE = PROJECT_ROOT / "data" / "questions_60.csv"

RESULTS_DIR = PROJECT_ROOT / "results"
RESULTS_DIR.mkdir(exist_ok=True)

OUTPUT_FILE = RESULTS_DIR / "main_results.csv"

METHODS = ["Direct", "Structured"]
BATCH_SIZE = 10


# --------------------------------------------------
# 2. LOAD QUESTIONS AND EXISTING RESULTS
# --------------------------------------------------

questions_df = pd.read_csv(INPUT_FILE)

print("Total questions:", len(questions_df))
print("Model:", model.MODEL_NAME)

if OUTPUT_FILE.exists():

    results_df = pd.read_csv(OUTPUT_FILE)

    print("Existing records:", len(results_df))

else:

    results_df = pd.DataFrame()

    print("No previous results found. Starting fresh.")


# Track successful requests only.
# Failed requests will be retried.

successful = set()

# Track the position of existing records.
# This allows us to update failed records.

existing_records = {}

if not results_df.empty:

    for index, row in results_df.iterrows():

        key = (str(row["id"]), row["method"])

        existing_records[key] = index

        if row["status"] == "success":
            successful.add(key)


total_tasks = len(questions_df) * len(METHODS)

completed_count = len(successful)

print("Total API responses planned:", total_tasks)
print("Already successful:", completed_count)
print("Remaining requests:", total_tasks - completed_count)


# --------------------------------------------------
# 3. RUN EXPERIMENT IN BATCHES
# --------------------------------------------------

for batch_start in range(0, len(questions_df), BATCH_SIZE):

    batch = questions_df.iloc[
        batch_start:batch_start + BATCH_SIZE
    ]

    print("\n===================================")
    print(
        f"Starting Batch {batch_start // BATCH_SIZE + 1}"
    )
    print("===================================")

    for _, row in batch.iterrows():

        question_id = row["id"]

        for method_name in METHODS:

            key = (str(question_id), method_name)

            # Skip only successful requests

            if key in successful:

                print(
                    f"Skipping {question_id} - {method_name} (already successful)"
                )

                continue

            print(
                f"\nRunning {question_id} | {method_name}"
            )

            try:

                result = model.generate_response(
                    client=client,
                    question=row["question"],
                    method=method_name
                )

                record = {
                    "id": question_id,
                    "category": row["category"],
                    "difficulty": row["difficulty"],
                    "method": method_name,
                    "question": row["question"],
                    "correct_answer": row["correct_answer"],
                    "response": result["response"],
                    "response_time_seconds":
                        result["response_time_seconds"],
                    "total_elapsed_seconds":
                        result.get("total_elapsed_seconds", None),
                    "input_tokens": result["input_tokens"],
                    "output_tokens": result["output_tokens"],
                    "status": "success",
                    "model_used": model.MODEL_NAME
                }

                print("SUCCESS!")

                successful.add(key)
                completed_count += 1

            except Exception as error:

                print("Error:", error)

                record = {
                    "id": question_id,
                    "category": row["category"],
                    "difficulty": row["difficulty"],
                    "method": method_name,
                    "question": row["question"],
                    "correct_answer": row["correct_answer"],
                    "response": "",
                    "response_time_seconds": None,
                    "total_elapsed_seconds": None,
                    "input_tokens": None,
                    "output_tokens": None,
                    "status": "failed",
                    "model_used": model.MODEL_NAME
                }

            # Update an existing failed record
            # or append a new record if it doesn't exist.

            if key in existing_records:

                index = existing_records[key]

                for column, value in record.items():

                    results_df.at[index, column] = value

            else:

                new_row = pd.DataFrame([record])

                results_df = pd.concat(
                    [results_df, new_row],
                    ignore_index=True
                )

                existing_records[key] = len(results_df) - 1

            # Save after every response

            results_df.to_csv(OUTPUT_FILE, index=False)

            print(
                f"Successful progress: {completed_count}/{total_tasks}"
            )

            time.sleep(1)


# --------------------------------------------------
# 4. FINAL SUMMARY
# --------------------------------------------------

print("\n===================================")
print("EXPERIMENT COMPLETED")
print("===================================")

print("Total recorded responses:", len(results_df))

print("\nStatus:")

print(results_df["status"].value_counts())

print("\nMethod-wise results:")

print(
    results_df.groupby(["method", "status"]).size()
)

print("\nResults saved at:")

print(OUTPUT_FILE)