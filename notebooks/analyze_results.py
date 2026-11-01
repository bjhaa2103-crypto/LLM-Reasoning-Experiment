import pandas as pd
from pathlib import Path

# Project directory
PROJECT_ROOT = Path(__file__).resolve().parent.parent

# Load results
FILE = PROJECT_ROOT / "results" / "main_results.csv"

df = pd.read_csv(FILE)

# Keep successful responses only
success = df[df["status"] == "success"].copy()

print("\n========== EXPERIMENT SUMMARY ==========")

print("Total API attempts:", len(df))
print("Successful responses:", len(success))
print("Failed requests:", len(df) - len(success))

print("\n========== METHOD-WISE SUMMARY ==========")

print(
    df.groupby(["method", "status"]).size()
)

print("\n========== PERFORMANCE METRICS ==========")

metrics = success.groupby("method").agg(
    Average_Response_Time=(
        "response_time_seconds", "mean"
    ),
    Average_Input_Tokens=(
        "input_tokens", "mean"
    ),
    Average_Output_Tokens=(
        "output_tokens", "mean"
    ),
    Successful_Responses=(
        "id", "count"
    )
)

print(metrics.round(2))

print("\n========== CATEGORY-WISE RESULTS ==========")

category_results = success.groupby(
    ["category", "method"]
).size().unstack(fill_value=0)

print(category_results)

print("\n========== DIFFICULTY-WISE RESULTS ==========")

difficulty_results = success.groupby(
    ["difficulty", "method"]
).size().unstack(fill_value=0)

print(difficulty_results)

print("\n========== MODEL-WISE RESULTS ==========")

print(success.groupby("model_used").size())

# Save summary
metrics.to_csv(
    PROJECT_ROOT / "results" / "performance_summary.csv"
)

category_results.to_csv(
    PROJECT_ROOT / "results" / "category_summary.csv"
)

difficulty_results.to_csv(
    PROJECT_ROOT / "results" / "difficulty_summary.csv"
)

print("\nSummary files saved successfully!")