import pandas as pd
from pathlib import Path

# Project directory
PROJECT_ROOT = Path(__file__).resolve().parent.parent

INPUT_FILE = PROJECT_ROOT / "results" / "main_results.csv"

OUTPUT_FILE = (
    PROJECT_ROOT / "results" / "answer_evaluation.csv"
)

# Load experiment results
df = pd.read_csv(INPUT_FILE)

# Keep only successful API responses
success = df[df["status"] == "success"].copy()

# Prepare evaluation sheet
evaluation = success[
    [
        "id",
        "category",
        "difficulty",
        "method",
        "question",
        "correct_answer",
        "response"
    ]
].copy()

# Add a column for manual correctness evaluation
evaluation["is_correct"] = ""

evaluation["remarks"] = ""

# Save evaluation sheet
evaluation.to_csv(OUTPUT_FILE, index=False)

print("Accuracy evaluation sheet created!")
print("Total responses to evaluate:", len(evaluation))

print("\nMethod-wise response count:")
print(evaluation.groupby("method").size())

print("\nFile saved at:")
print(OUTPUT_FILE)