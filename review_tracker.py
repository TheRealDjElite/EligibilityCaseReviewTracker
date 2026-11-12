"""
Eligibility Case Review Tracker

Checks case records for incomplete information, then keeps a running review log
across runs. Each run adds new issues, carries forward the ones still open,
marks issues Resolved when the data no longer shows them, and flags follow-ups
that are past due. Reviewer notes typed into the log are kept between runs.

Usage:
    python review_tracker.py data/cases_2025-04-14.csv --run-date 2025-04-14
    python review_tracker.py data/cases_2025-04-24.csv --run-date 2025-04-24
"""

import argparse
import os
from datetime import date, datetime, timedelta

import pandas as pd
from openpyxl import Workbook, load_workbook
from openpyxl.formatting.rule import CellIsRule
from openpyxl.styles import Alignment, Font, PatternFill

# ---------------------------------------------------------------- settings ---
DEFAULT_INPUT = "data/cases_2025-04-14.csv"   # CSV or Excel (.xlsx)
LOG_FILE = "output/review_log.xlsx"

REQUIRED_FIELDS = ["Case ID", "Client Name", "Program", "Status", "Worker"]
DECISION_STATUSES = ["approved", "denied"]    # decided cases need a review date
FOLLOW_UP_DAYS = 7                            # days a worker has to fix an issue

LOG_COLUMNS = [
    "Case ID", "Issue", "Worker", "Date Flagged", "Follow-Up Due",
    "Status", "Days Open", "Date Resolved", "History", "Reviewer Notes",
]

# ------------------------------------------------------------- formatting ---
HEADER_FILL = PatternFill("solid", fgColor="1F3864")
HEADER_FONT = Font(bold=True, color="FFFFFF")
NOTES_FILL = PatternFill("solid", fgColor="FFF8E1")   # marks the column to type in
RED = PatternFill("solid", fgColor="F8CBAD")
YELLOW = PatternFill("solid", fgColor="FFE699")
GREEN = PatternFill("solid", fgColor="C6EFCE")
DATE_FORMAT = "yyyy-mm-dd"


# ------------------------------------------------------------- load input ---
def load_cases(path):
    if path.lower().endswith(".xlsx"):
        df = pd.read_excel(path, dtype=str)
    else:
        df = pd.read_csv(path, dtype=str)
    # Skip rows that are completely empty (common at the bottom of Excel sheets)
    has_data = df.apply(lambda r: any(not is_blank(v) for v in r), axis=1)
    return df[has_data].reset_index(drop=True)


def is_blank(value):
    return pd.isna(value) or str(value).strip() == ""


def clean(value):
    return "" if is_blank(value) else str(value).strip()


def find_issues(row):
    """Return a list of issue descriptions for one case record."""
    issues = []
    for field in REQUIRED_FIELDS:
        if is_blank(row[field]):
            issues.append(f"Missing {field}")

    status = clean(row["Status"]).lower()
    if status in DECISION_STATUSES and is_blank(row["Review Date"]):
        issues.append(f"{status.title()} case with no Review Date")
    return issues


# --------------------------------------------------------- load prior log ---
def to_date(value):
    if isinstance(value, datetime):
        return value.date()
    if isinstance(value, date):
        return value
    return None


def load_log(path):
    """Read the review log from the last run. Returns {issue key: entry}."""
    if not os.path.exists(path):
        return {}
    ws = load_workbook(path)["Review Log"]
    rows = ws.iter_rows(values_only=True)
    headers = list(next(rows))
    log = {}
    for values in rows:
        entry = dict(zip(headers, values))
        if not entry.get("Issue"):
            continue
        entry["Case ID"] = clean(entry["Case ID"])
        for col in ("Date Flagged", "Follow-Up Due", "Date Resolved"):
            entry[col] = to_date(entry[col])
        entry["History"] = entry.get("History") or ""
        entry["Reviewer Notes"] = entry.get("Reviewer Notes") or ""
        log[(entry["Case ID"], entry["Issue"])] = entry
    return log


# ------------------------------------------------------ update review log ---
def update_log(log, current_issues, run_date):
    """Add new issues, carry forward open ones, resolve fixed ones.
    Returns counts of what changed this run."""
    counts = {"new": 0, "reopened": 0, "resolved": 0}
    due = run_date + timedelta(days=FOLLOW_UP_DAYS)

    for key, worker in current_issues.items():
        entry = log.get(key)
        if entry is None:
            log[key] = {
                "Case ID": key[0], "Issue": key[1], "Worker": worker,
                "Date Flagged": run_date, "Follow-Up Due": due,
                "Date Resolved": None, "Status": "Open",
                "History": f"{run_date} flagged", "Reviewer Notes": "",
            }
            counts["new"] += 1
        else:
            entry["Worker"] = worker
            if entry["Status"] == "Resolved":       # issue came back
                entry["Status"] = "Open"
                entry["Date Resolved"] = None
                entry["Follow-Up Due"] = due
                entry["History"] += f"; {run_date} reopened"
                counts["reopened"] += 1

    for key, entry in log.items():
        if key not in current_issues and entry["Status"] != "Resolved":
            entry["Status"] = "Resolved"
            entry["Date Resolved"] = run_date
            entry["History"] += f"; {run_date} resolved"
            counts["resolved"] += 1

    # Recalculate status and age for everything still open
    for entry in log.values():
        if entry["Status"] == "Resolved":
            entry["Days Open"] = (entry["Date Resolved"] - entry["Date Flagged"]).days
        else:
            entry["Status"] = "Overdue" if run_date > entry["Follow-Up Due"] else "Open"
            entry["Days Open"] = (run_date - entry["Date Flagged"]).days
    return counts


# ------------------------------------------------------------ write output ---
def style_header(ws, widths):
    for col, width in enumerate(widths, start=1):
        cell = ws.cell(row=1, column=col)
        cell.fill, cell.font = HEADER_FILL, HEADER_FONT
        ws.column_dimensions[cell.column_letter].width = width
    ws.freeze_panes = "A2"


def write_review_log(wb, log):
    ws = wb.create_sheet("Review Log")
    ws.append(LOG_COLUMNS)
    order = {"Overdue": 0, "Open": 1, "Resolved": 2}
    entries = sorted(
        log.values(),
        key=lambda e: (order[e["Status"]], e["Follow-Up Due"], e["Case ID"], e["Issue"]),
    )
    for e in entries:
        ws.append([e[col] for col in LOG_COLUMNS])

    last = ws.max_row
    for row in ws.iter_rows(min_row=2, max_row=last):
        for cell in row:
            if LOG_COLUMNS[cell.column - 1] in ("Date Flagged", "Follow-Up Due", "Date Resolved"):
                cell.number_format = DATE_FORMAT
        row[LOG_COLUMNS.index("Reviewer Notes")].fill = NOTES_FILL
        row[LOG_COLUMNS.index("History")].alignment = Alignment(wrap_text=True, vertical="top")

    status_range = f"F2:F{max(last, 2)}"
    ws.conditional_formatting.add(status_range, CellIsRule(operator="equal", formula=['"Overdue"'], fill=RED))
    ws.conditional_formatting.add(status_range, CellIsRule(operator="equal", formula=['"Open"'], fill=YELLOW))
    ws.conditional_formatting.add(status_range, CellIsRule(operator="equal", formula=['"Resolved"'], fill=GREEN))

    style_header(ws, [10, 34, 12, 14, 14, 11, 10, 14, 44, 40])
    ws.auto_filter.ref = f"A1:J{last}"


def write_cases(wb, df):
    ws = wb.create_sheet("Cases This Run")
    ws.append(list(df.columns))
    for row in df.itertuples(index=False):
        ws.append(list(row))
    status_col = ws.cell(row=1, column=df.columns.get_loc("Review Status") + 1).column_letter
    rng = f"{status_col}2:{status_col}{max(ws.max_row, 2)}"
    ws.conditional_formatting.add(rng, CellIsRule(operator="equal", formula=['"Needs Review"'], fill=RED))
    ws.conditional_formatting.add(rng, CellIsRule(operator="equal", formula=['"OK"'], fill=GREEN))
    style_header(ws, [10, 18, 11, 11, 13, 10, 15, 50])


def write_summary(wb, run_date, input_file, df, counts, log):
    ws = wb.create_sheet("Summary", 0)
    ws["A1"] = "Case Review Summary"
    ws["A1"].font = Font(bold=True, size=14)

    flagged_cases = int((df["Review Status"] == "Needs Review").sum())
    run_rows = [
        ("Run date", run_date),
        ("Input file", input_file),
        ("Cases checked", len(df)),
        ("Cases needing review", flagged_cases),
        ("New issues this run", counts["new"]),
        ("Reopened this run", counts["reopened"]),
        ("Resolved this run", counts["resolved"]),
        ("Follow-up window (days)", FOLLOW_UP_DAYS),
    ]
    for i, (label, value) in enumerate(run_rows, start=3):
        ws.cell(row=i, column=1, value=label).font = Font(bold=True)
        cell = ws.cell(row=i, column=2, value=value)
        if isinstance(value, date):
            cell.number_format = DATE_FORMAT
        cell.alignment = Alignment(horizontal="left")

    # Issues by worker. These are Excel formulas, so they update if the log is edited.
    top = len(run_rows) + 5
    headers = ["Worker", "Open", "Overdue", "Resolved", "Total"]
    for col, text in enumerate(headers, start=1):
        cell = ws.cell(row=top, column=col, value=text)
        cell.fill, cell.font = HEADER_FILL, HEADER_FONT

    workers = sorted({e["Worker"] for e in log.values()})
    for i, worker in enumerate(workers, start=top + 1):
        ws.cell(row=i, column=1, value=worker)
        for col, status in ((2, "Open"), (3, "Overdue"), (4, "Resolved")):
            ws.cell(row=i, column=col,
                    value=f"=COUNTIFS('Review Log'!C:C,$A{i},'Review Log'!F:F,\"{status}\")")
        ws.cell(row=i, column=5, value=f"=SUM(B{i}:D{i})")

    total_row = top + len(workers) + 1
    ws.cell(row=total_row, column=1, value="Total").font = Font(bold=True)
    for col in range(2, 6):
        letter = ws.cell(row=top, column=col).column_letter
        cell = ws.cell(row=total_row, column=col, value=f"=SUM({letter}{top + 1}:{letter}{total_row - 1})")
        cell.font = Font(bold=True)

    overdue_rng = f"C{top + 1}:C{total_row}"
    ws.conditional_formatting.add(overdue_rng, CellIsRule(operator="greaterThan", formula=["0"], fill=RED))
    ws.column_dimensions["A"].width = 26
    for letter in "BCDE":
        ws.column_dimensions[letter].width = 12
    ws.column_dimensions["B"].width = 28


# -------------------------------------------------------------------- main ---
def main():
    parser = argparse.ArgumentParser(description="Flag incomplete case records and track follow-up across runs.")
    parser.add_argument("input_file", nargs="?", default=DEFAULT_INPUT, help="CSV or .xlsx file of case records")
    parser.add_argument("--run-date", help="Date of this review run (YYYY-MM-DD). Defaults to today.")
    args = parser.parse_args()

    run_date = date.fromisoformat(args.run_date) if args.run_date else date.today()

    if not os.path.exists(args.input_file):
        print(f"Input file not found: {args.input_file}")
        return

    df = load_cases(args.input_file)
    missing_columns = [c for c in REQUIRED_FIELDS + ["Review Date"] if c not in df.columns]
    if missing_columns:
        print(f"Input file is missing required columns: {', '.join(missing_columns)}")
        return
    if df.empty:
        print("No case records found. Enter case data and run again.")
        return

    # Check every case and collect this run's issues
    current_issues = {}
    review_status, review_notes = [], []
    for row_number, (_, row) in enumerate(df.iterrows(), start=2):
        issues = find_issues(row)
        review_status.append("Needs Review" if issues else "OK")
        review_notes.append("; ".join(issues))
        case_id = clean(row["Case ID"]) or f"Row {row_number}"   # no Case ID: track by file row
        worker = clean(row["Worker"]) or "(unassigned)"
        for issue in issues:
            current_issues[(case_id, issue)] = worker

    df["Review Status"] = review_status
    df["Review Notes"] = review_notes

    # Update the running log and save the workbook
    log = load_log(LOG_FILE)
    counts = update_log(log, current_issues, run_date)

    wb = Workbook()
    wb.remove(wb.active)
    write_review_log(wb, log)
    write_cases(wb, df)
    write_summary(wb, run_date, args.input_file, df, counts, log)
    os.makedirs(os.path.dirname(LOG_FILE), exist_ok=True)
    try:
        wb.save(LOG_FILE)
    except PermissionError:
        print(f"Could not save {LOG_FILE}. Close it in Excel and run again.")
        return

    open_count = sum(e["Status"] == "Open" for e in log.values())
    overdue_count = sum(e["Status"] == "Overdue" for e in log.values())
    print(f"Run date: {run_date}")
    print(f"Cases checked: {len(df)} | needing review: {review_status.count('Needs Review')}")
    print(f"Issues new: {counts['new']} | reopened: {counts['reopened']} | resolved: {counts['resolved']}")
    print(f"Open: {open_count} | Overdue: {overdue_count}")
    print(f"Review log saved to {LOG_FILE}")


if __name__ == "__main__":
    main()
