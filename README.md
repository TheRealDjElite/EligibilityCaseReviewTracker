# 🔍 Eligibility Case Review Tracker

Python-based data validation tool designed to support QA and structured data review in high-volume operational environments. Built around rule-based checks to identify missing, invalid, or inconsistent data before downstream processing or reporting.

Processes CSV or Excel inputs and generates a clear output of data quality issues for review.

## 🔧 What It Does

- Loads structured data from CSV or Excel files  
- Applies validation checks for missing, invalid, or inconsistent values such as dates, IDs, and key fields  
- Flags records that require review based on defined rules  
- Outputs results to `error_report.csv` for QA or audit follow-up  

## 🧰 Tools Used

- Python (pandas)  
- Microsoft Excel  
- CSV and Excel structured data formats  

## 📁 File Overview

- `demo_data.csv` - Sample dataset for testing  
- `data_checker.py` - Validation and rule-checking script  
- `tracker_template.xlsx` - Optional structured input template  

## ▶ How to Use It

1. Populate `demo_data.csv` or use the Excel template  
2. Run `data_checker.py`  
3. Review `error_report.csv` for flagged issues  

## 📌 Purpose

Built to reflect real-world data validation and QA workflows across regulated and high-volume environments. Focuses on improving data integrity, enforcing consistency, and reducing rework by identifying issues early in the process.