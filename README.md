# Automated Micro-Task Tracker — "To-Do" Data Engine

A data cleaning and analysis pipeline for productivity logs exported from a custom-built task tracking app. Built with **Python (Pandas & NumPy)** in **Jupyter Notebook**.

## Project Overview

Task-tracking apps generate messy, real-world data: missing values, inconsistent category labels, typos, and outliers from forgotten timers. This project simulates that reality with **5,000+ synthetic task log entries** and builds a full pipeline to clean, validate, and analyze it — surfacing patterns like task friction and peak procrastination periods.

## What This Project Does

1. **Data quality profiling** — quantifies missing values and inconsistent category strings before any cleaning decisions are made
2. **Missing value handling** — using Pandas to isolate and treat missing task durations (category-level median imputation) and incomplete categorical values
3. **Category standardization** — normalizes inconsistent casing/whitespace/typos (27 raw string variants → 6 canonical categories)
4. **Outlier detection** — uses NumPy to implement a MAD-based modified z-score for statistical filtering, isolating extreme duration outliers and manual entry errors without being skewed by the outliers themselves
5. **Duplicate removal** — identifies and removes fully duplicated log entries
6. **Exploratory Data Analysis (EDA)** — maps task friction (high duration + low completion rate), identifies peak procrastination hours, and analyzes completion rates by day of week
7. **Sanitized data export** — outputs a clean dataset ready for downstream reporting

## Project Structure

```
micro-task-tracker/
├── data/
│   ├── generate_data.py       # Generates the synthetic raw dataset
│   └── raw_task_logs.csv      # 5,000+ raw, intentionally messy task log entries
├── notebooks/
│   └── task_tracker_analysis.ipynb   # Full cleaning + EDA pipeline (with outputs)
├── outputs/
│   ├── sanitized_task_logs.csv           # Cleaned, analysis-ready dataset
│   ├── flagged_outliers.csv              # Isolated outlier rows for manual review
│   ├── duration_by_category_with_outliers.png
│   ├── category_time_and_completion.png
│   ├── procrastination_by_hour.png
│   └── completion_by_day.png
├── requirements.txt
└── README.md
```

## How to Run

```bash
# 1. Clone the repo
git clone https://github.com/<your-username>/micro-task-tracker.git
cd micro-task-tracker

# 2. Install dependencies
pip install -r requirements.txt

# 3. (Optional) Regenerate the raw dataset
cd data && python generate_data.py && cd ..

# 4. Launch the notebook
jupyter notebook notebooks/task_tracker_analysis.ipynb
```

## Key Techniques Used

| Technique | Tool | Purpose |
|---|---|---|
| Median imputation by group | Pandas (`groupby().transform()`) | Fill missing durations without distortion from outliers |
| String normalization | Pandas (`.str.strip()`, `.str.title()`) | Standardize inconsistent category labels |
| Modified z-score (MAD-based) | NumPy | Robust outlier detection on skewed duration data |
| Duplicate detection | Pandas (`drop_duplicates`) | Remove logging-bug duplicate rows |
| Time-based aggregation | Pandas (`dt.hour`, `dt.day_name()`) | Identify procrastination windows and weekly patterns |

## Sample Findings

- Standardized category labels from **27 inconsistent raw string variants down to 6 canonical categories**
- Flagged and isolated **duration outliers** (manual entry typos and forgotten running timers) using a MAD-based modified z-score
- Identified the **peak procrastination hour** and the category with the highest time share and lowest completion rate ("friction")
- Exported a clean, de-duplicated dataset for downstream reporting

## Tech Stack

- **Python 3** — Pandas, NumPy, Matplotlib, Seaborn
- **Jupyter Notebook** — interactive analysis and visualization

---

*Note: `raw_task_logs.csv` is synthetically generated (see `data/generate_data.py`) to realistically simulate messy real-world task-log data, since no real user data was available for this portfolio project.*
