# 🔍 Eligibility Case Review Tracker

Python-based review tool that flags incomplete case records for follow-up. Designed to support QA and structured case review in high-volume operational environments.

Reads case data from a CSV or Excel file, checks each record for missing information and missing review dates on decided cases, and saves a copy with a review status and notes for each case.

## 🔧 What It Does

- Loads case records from a CSV file or the Excel template (`.xlsx`)
- Flags records missing a Case ID, Client Name, Program, or Status (including blank or space-only entries)
- Flags approved or denied cases with no review date (pending cases without one are allowed)
- Adds a "Review Status" column (Needs Review or OK) and a "Review Notes" column explaining each flag
- Prints a summary of cases checked and cases needing review, and saves results to `review_output.csv`

## 🧪 Sample Data

`demo_data.csv` includes 8 case records: 3 complete records and 5 with intentional issues (missing or blank client names, missing status, missing program, and decided cases with no review date). Case ID 1006 is a pending case with no review date and is not flagged.

## 🧰 Tools Used

- Python (pandas, AI-assisted development)
- Microsoft Excel (input template)

## 📁 File Overview

- `data_checker.py` - Script that reviews each case and adds a review status and notes
- `demo_data.csv` - Sample case dataset for testing
- `tracker_template.xlsx` - Excel template with the same column layout for entering case data

## ▶ How to Use It

1. Install dependencies: `pip install pandas openpyxl`
2. Enter case data in `demo_data.csv` or `tracker_template.xlsx`
3. If using the Excel template, change `INPUT_FILE` in the script to `tracker_template.xlsx`
4. Run `data_checker.py`
5. Review `review_output.csv` for cases marked Needs Review

## 📌 Purpose

Built to reflect real-world case review and QA workflows in regulated, high-volume environments. Focuses on catching incomplete records early so they can be corrected before review or reporting.
