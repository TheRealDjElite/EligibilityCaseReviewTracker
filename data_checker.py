import os
import pandas as pd

# Input can be a CSV file or an Excel file (.xlsx), such as tracker_template.xlsx
INPUT_FILE = "demo_data.csv"
OUTPUT_FILE = "review_output.csv"

REQUIRED_FIELDS = ["Case ID", "Client Name", "Program", "Status"]
DECISION_STATUSES = ["approved", "denied"]  # decided cases must have a review date

def load_cases(path):
    if path.lower().endswith(".xlsx"):
        return pd.read_excel(path, dtype=str)
    return pd.read_csv(path, dtype=str)

def is_blank(value):
    return pd.isna(value) or str(value).strip() == ""

def review_case(row):
    notes = []

    # Missing or blank required fields
    for field in REQUIRED_FIELDS:
        if is_blank(row[field]):
            notes.append(f"Missing {field}")

    # Approved or denied cases need a review date (pending cases can wait)
    status = "" if is_blank(row["Status"]) else str(row["Status"]).strip().lower()
    if status in DECISION_STATUSES and is_blank(row["Review Date"]):
        notes.append(f"{status.title()} case with no Review Date")

    return notes

def main():
    if not os.path.exists(INPUT_FILE):
        print(f"Input file not found: {INPUT_FILE}")
        return

    df = load_cases(INPUT_FILE)

    missing_columns = [col for col in REQUIRED_FIELDS + ["Review Date"] if col not in df.columns]
    if missing_columns:
        print(f"Input file is missing required columns: {', '.join(missing_columns)}")
        return

    if df.empty:
        print("No case records found. Enter case data and run again.")
        return

    review_status = []
    review_notes = []
    for _, row in df.iterrows():
        notes = review_case(row)
        review_status.append("Needs Review" if notes else "OK")
        review_notes.append("; ".join(notes))

    df["Review Status"] = review_status
    df["Review Notes"] = review_notes
    df.to_csv(OUTPUT_FILE, index=False)

    flagged = df[df["Review Status"] == "Needs Review"]
    print(f"Cases checked: {len(df)}")
    print(f"Cases needing review: {len(flagged)}")
    if not flagged.empty:
        print()
        print(flagged[["Case ID", "Review Notes"]].fillna("").to_string(index=False))
    print(f"\nResults saved to {OUTPUT_FILE}")

if __name__ == "__main__":
    main()
