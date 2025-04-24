# Eligibility Case Review Tracker

A tool to help QA analysts and case reviewers track eligibility cases (SNAP, TANF, Medicaid) and identify common data issues using Python and Excel.

## 🔍 What It Does
- Tracks eligibility case reviews across public programs
- Flags missing or invalid data using simple Python logic
- Uses Excel or CSV inputs for flexibility
- Helps remote teams stay organized and audit-ready

## 🧰 Tools Used
- Microsoft Excel
- Python (pandas)
- CSV (for demo/testing)

## 📁 File Overview
- `demo_data.csv` — Sample data for testing
- `data_checker.py` — Python script that reads and validates the data
- `tracker_template.xlsx` — Optional Excel version of the input

## 🧪 How to Use It
1. Add your case data to `demo_data.csv`
2. Run `data_checker.py`
3. Review the output to spot issues

## ✅ Use Case
Built for remote Medicaid/SNAP/TANF teams that need an accurate and auditable way to review eligibility cases.

---

Made with 💡 by #EliteTheOctoDog™ 🐙🐶
[LinkedIn →](https://linkedin.com/in/JoeNetherland)

<details>
<summary>📘 Instructions for Non-Technical Users (Click to Expand)</summary>

### 💡 How to Use This Tool (No Tech Skills Needed)

This tool checks your eligibility case data for missing or incorrect information, and flags any issues for review. You don’t need technical knowledge to use it.

---

### ✅ What You’ll Need:
1. A computer with Excel (or Google Sheets)
2. Python installed on your system (download at: https://www.python.org/downloads)
3. Your case data saved as a `.csv` file (can be exported from Excel or Google Sheets)

---

### 🧭 Step-by-Step Instructions

#### 1. Download the Tool
- Go to:  
  [https://github.com/TheRealDjElite/EligibilityCaseReviewTracker](https://github.com/TheRealDjElite/EligibilityCaseReviewTracker)
- Click the green **Code** button → **Download ZIP**
- Unzip the folder

#### 2. Open the Folder
- Find the file: `data_checker.py`

#### 3. Run the Tool
- On **Windows**:
  - Inside the folder, click the **address bar**, type `cmd`, and press **Enter**
  - In the black window that opens, type:
    ```
    python data_checker.py
    ```

- On **Mac**:
  - Open the **Terminal**
  - Drag the folder into the Terminal after typing:
    ```
    cd 
    ```
    Then press **Enter**
  - Run the script:
    ```
    python3 data_checker.py
    ```

#### 4. See Your Results
- The tool will show any missing or invalid data
- It will create an `error_report.csv` file with the flagged issues
- Open the `error_report.csv` file in Excel or Google Sheets to see what needs fixing

---

### 👩‍💼 Example Use
You’re checking SNAP, TANF, or Medicaid eligibility cases submitted by case managers. After running this tool, you’ll see which records have missing data, invalid dates, or mismatched status — and then you can fix them quickly before they’re submitted.

</details>
