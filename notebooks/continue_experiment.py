print("Continuing the Modern AI Assignment experiment")
from pathlib import Path
import pandas as pd

PROJECT_DIR = Path(__file__).resolve().parent.parent
RESULTS_FILE = PROJECT_DIR / "results" / "results.csv"

df = pd.read_csv(RESULTS_FILE)

print("\n========== FAILED REQUESTS ==========\n")

failed = df[df["status"] == "Failed"]

if failed.empty:
    print("No failed requests found.")
else:
    for _, row in failed.iterrows():
        print(
            f"Question ID: {row['id']} | "
            f"Method: {row['method']} | "
            f"Category: {row['category']}"
        )
        print(f"Question: {row['question']}")
        print(f"Expected answer: {row['correct_answer']}")
        print("-" * 60)

print("\n========== SUCCESSFUL REQUESTS ==========\n")

successful = df[df["status"] == "Success"]

for method in ["Direct", "Structured"]:
    subset = successful[successful["method"] == method]

    print(f"{method}: {len(subset)} successful requests")

print("\nInspection complete. No API requests were made.")