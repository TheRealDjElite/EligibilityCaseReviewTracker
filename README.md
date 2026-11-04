# 🔍 Eligibility Case Review Tracker

Python-based review tool that flags incomplete case records for follow-up. Designed to support QA and structured case review in high-volume operational environments.

Reads case data from a CSV file, identifies records with missing information, and saves a flagged copy for review.

## 🔧 What It Does

- Loads case records from `demo_data.csv`
- Identifies rows with any missing values
- Identifies rows with blank client names
- Adds a "Flag - Missing Info" column and saves results to `review_output.csv`

## 🧰 Tools Used

- Python (pandas, AI-assisted development)
- Microsoft Excel (input template)

## 📁 File Overview

- `demo_data.csv` - Sample case dataset for testing
- `data_checker.py` - Script that checks records and flags missing information
- `tracker_template.xlsx` - Excel template with the same column layout for entering case data

## ▶ How to Use It

1. Enter case data in `demo_data.csv` (the Excel template shows the column layout)
2. Install dependencies: `pip install pandas`
3. Run `data_checker.py`
4. Review `review_output.csv` for flagged records

## 📌 Purpose

Built to reflect real-world case review and QA workflows in regulated, high-volume environments. Focuses on catching incomplete records early so they can be corrected before review or reporting.
