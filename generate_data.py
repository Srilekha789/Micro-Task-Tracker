"""
generate_data.py
----------------
Simulates a raw data export from a custom-built "To-Do" task tracking app.

Why this file exists:
    Real production logs aren't available for a portfolio project, so this
    script generates a realistic stand-in: 5,000+ task entries with the same
    kinds of problems real user-generated logs have -- missing durations,
    missing categories, duplicate/typo'd category labels, and a handful of
    extreme outlier durations (e.g. someone left a timer running overnight).

Run this once to produce data/raw_task_logs.csv, which the analysis
notebook (notebooks/task_tracker_analysis.ipynb) then cleans and analyzes.
"""

import numpy as np
import pandas as pd
from datetime import datetime, timedelta

# Reproducible "randomness" so the dataset is the same every time it's regenerated
rng = np.random.default_rng(seed=42)

N_ROWS = 5250  # 5,000+ entries as referenced in the resume bullet

# --- Reference data -------------------------------------------------------

CATEGORIES_CLEAN = ["Work", "Study", "Chores", "Health", "Personal", "Errands"]

# Intentionally inconsistent variants of the same categories, to be cleaned later
CATEGORIES_MESSY_VARIANTS = {
    "Work": ["work", " Work", "WORK", "Work "],
    "Study": ["study", "Study ", " study", "STUDY"],
    "Chores": ["chores", "Chore", " Chores", "CHORES"],
    "Health": ["health", "Health ", " health"],
    "Personal": ["personal", "Personal ", "PERSONAL"],
    "Errands": ["errand", "Errands ", " errands"],
}

TASK_NAMES = {
    "Work": ["Email cleanup", "Sprint planning notes", "Client report", "Code review",
             "Team sync prep", "Budget spreadsheet"],
    "Study": ["Read chapter", "Practice problems", "Flashcard review", "Online course module",
              "Essay draft"],
    "Chores": ["Laundry", "Dishes", "Vacuuming", "Grocery shopping", "Tidy desk"],
    "Health": ["Workout", "Meal prep", "Meditation", "Walk", "Stretching"],
    "Personal": ["Journaling", "Read for fun", "Call family", "Budget review"],
    "Errands": ["Bank visit", "Pharmacy pickup", "Post office", "Car wash"],
}

# --- Generate base (clean) fields -----------------------------------------

start_date = datetime(2025, 1, 1)
dates = [start_date + timedelta(days=int(d), hours=int(h), minutes=int(m))
         for d, h, m in zip(
             rng.integers(0, 210, N_ROWS),           # spread across ~7 months
             rng.integers(6, 23, N_ROWS),            # hour of day (waking hours)
             rng.integers(0, 60, N_ROWS)
         )]

category_choice = rng.choice(CATEGORIES_CLEAN, size=N_ROWS, p=[0.30, 0.20, 0.15, 0.15, 0.10, 0.10])
task_name = [rng.choice(TASK_NAMES[c]) for c in category_choice]

# Base duration in minutes: most tasks are short, drawn from a realistic right-skewed distribution
duration_minutes = rng.gamma(shape=2.2, scale=15, size=N_ROWS).round(1)

user_id = rng.integers(1000, 1050, N_ROWS)  # ~50 simulated users
completed_flag = rng.choice(["Yes", "No"], size=N_ROWS, p=[0.88, 0.12])

df = pd.DataFrame({
    "task_id": np.arange(1, N_ROWS + 1),
    "user_id": user_id,
    "task_name": task_name,
    "category": category_choice,
    "timestamp": dates,
    "duration_minutes": duration_minutes,
    "completed": completed_flag,
})

# --- Inject the messiness the resume bullets describe ----------------------

# 1) Missing task durations (~6% of rows) -- simulates timer not stopped / app crash
missing_duration_idx = rng.choice(df.index, size=int(0.06 * N_ROWS), replace=False)
df.loc[missing_duration_idx, "duration_minutes"] = np.nan

# 2) Incomplete / missing categorical values (~4% of rows)
missing_category_idx = rng.choice(df.index, size=int(0.04 * N_ROWS), replace=False)
df.loc[missing_category_idx, "category"] = np.nan

# 3) Inconsistent categorical string formatting (typos, casing, whitespace) on a
#    separate random slice of rows that DO have a category value
messy_format_idx = rng.choice(
    df.index.difference(missing_category_idx), size=int(0.18 * N_ROWS), replace=False
)
for idx in messy_format_idx:
    clean_cat = df.loc[idx, "category"]
    variants = CATEGORIES_MESSY_VARIANTS.get(clean_cat)
    if variants:
        df.loc[idx, "category"] = rng.choice(variants)

# 4) Extreme duration outliers / manual entry typos (~1.5% of rows)
#    e.g. "125" typed instead of "12.5", or a forgotten running timer (600+ min)
outlier_idx = rng.choice(
    df.index.difference(missing_duration_idx), size=int(0.015 * N_ROWS), replace=False
)
outlier_style = rng.choice(["typo", "forgotten_timer"], size=len(outlier_idx))
for idx, style in zip(outlier_idx, outlier_style):
    if style == "typo":
        df.loc[idx, "duration_minutes"] = df.loc[idx, "duration_minutes"] * rng.integers(8, 15)
    else:
        df.loc[idx, "duration_minutes"] = rng.integers(480, 900)  # 8-15 hrs, clearly not a real task

# 5) A few fully duplicate rows, as real app exports often have (~0.5%)
dupe_rows = df.sample(n=int(0.005 * N_ROWS), random_state=1)
df = pd.concat([df, dupe_rows], ignore_index=True)

# Shuffle so injected issues aren't clustered at the end of the file
df = df.sample(frac=1, random_state=7).reset_index(drop=True)
df["task_id"] = np.arange(1, len(df) + 1)  # re-sequence IDs after shuffle

# --- Save raw (messy) export ------------------------------------------------

output_path = "raw_task_logs.csv"
df.to_csv(output_path, index=False)
print(f"Generated {len(df)} rows -> {output_path}")
print(f"  Missing duration_minutes: {df['duration_minutes'].isna().sum()}")
print(f"  Missing category:         {df['category'].isna().sum()}")
print(f"  Unique category strings:  {df['category'].nunique(dropna=True)} (should be > 6 due to messiness)")
