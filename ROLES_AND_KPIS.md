# 👥 Roles (RACI) and KPI Definitions

Who does what when a review team runs this tracker, and how to measure whether flagged issues get fixed on time. The roles below describe how the review process works on a team. The tool finds and logs issues. People fix them.

## 🧑‍💼 Roles

| Role | Responsibility |
|---|---|
| QA Reviewer | Runs the tracker, reviews the log, adds notes, and confirms fixes |
| Caseworker | Fixes the case record. Listed in the Worker column |
| Supervisor | Owns follow-up on overdue issues and assigns cases with no worker |
| Program Manager | Receives the summary and tracks results over time |

## 📋 RACI Matrix

**R** = Responsible (does the work) • **A** = Accountable (owns the outcome) • **C** = Consulted • **I** = Informed

| Activity | QA Reviewer | Caseworker | Supervisor | Program Manager | Where in the Tool |
|---|---|---|---|---|---|
| Prepare the case file for the run | A/R | | I | | `tracker_template.xlsx` or a CSV export |
| Run the tracker | A/R | | | | `review_tracker.py` |
| Review new issues | A/R | I | I | | Review Log sheet, Open status |
| Fix the case record | C | R | A | | Source case data |
| Assign a worker to unassigned issues | I | I | A/R | | Worker shows `(unassigned)` |
| Add reviewer notes | A/R | C | | | Reviewer Notes column |
| Confirm the fix | A/R | I | I | | Next run marks the issue Resolved |
| Follow up on overdue issues | I | C | A/R | | Review Log sheet, Overdue status |
| Work reopened issues | I | R | A | | History column shows the reopen date |
| Report results | R | | A | I | Summary sheet and KPIs below |

Each activity has one Accountable role.

## 📊 KPI Definitions

Sample values come from running both sample files in order (April 14, then April 24). Formulas reference the Review Log and Summary sheets in `output/review_log.xlsx`. Each run rebuilds the workbook and keeps only the Review Log entries and Reviewer Notes, so a KPI sheet added by hand gets removed on the next run. Add the formulas to a copy of the log after the run.

| ID | KPI | Definition | Excel Formula | Sample Value |
|---|---|---|---|---|
| K-01 | Open issues | Issues still inside the follow-up window | `=COUNTIF('Review Log'!F:F,"Open")` | 2 |
| K-02 | Overdue issues | Issues past the follow-up due date with no fix | `=COUNTIF('Review Log'!F:F,"Overdue")` | 3 |
| K-03 | Overdue rate | Overdue issues as a share of all unresolved issues | `=IFERROR(COUNTIF('Review Log'!F:F,"Overdue")/(COUNTIF('Review Log'!F:F,"Open")+COUNTIF('Review Log'!F:F,"Overdue")),"N/A")` | 60% |
| K-04 | New issues this run | Issues flagged for the first time on this run | Summary sheet, New issues this run | 2 |
| K-05 | Resolved this run | Issues the run no longer found in the data | Summary sheet, Resolved this run | 4 |
| K-06 | Reopened this run | Resolved issues found again | Summary sheet, Reopened this run | 0 |
| K-07 | Average days to resolve | Average Days Open across resolved issues | `=IFERROR(AVERAGEIF('Review Log'!F:F,"Resolved",'Review Log'!G:G),"N/A")` | 10 days |
| K-08 | Resolved by due date | Share of resolved issues confirmed on or before the follow-up due date | `=IFERROR(SUMPRODUCT(('Review Log'!F2:F1000="Resolved")*('Review Log'!H2:H1000<='Review Log'!E2:E1000))/COUNTIF('Review Log'!F:F,"Resolved"),"N/A")` | 0% (0 of 4) |
| K-09 | Cases needing review rate | Share of cases checked with at least one issue | `=Summary!B6/Summary!B5` | 41.7% (5 of 12) |
| K-10 | Overdue issues by worker | Overdue count for each worker | Summary sheet, worker table | Leilani 2, Mele 1 |

Format K-03, K-08, and K-09 as percentages in Excel. The `IFERROR` wrapper shows N/A instead of a divide-by-zero error when the log has no matching issues. K-08 covers rows 2 through 1000 of the Review Log. Raise the 1000 for a larger log.

## 📏 Measurement Notes

| ID | Note | Effect on the KPIs |
|---|---|---|
| M-01 | Date Resolved is the date of the run that confirms the fix, not the date the worker made the fix. | K-07 and K-08 depend on how often the tracker runs. In the sample, the second run came 3 days after the April 21 due date, so all 4 fixes count as late at 10 days. A second run on April 18 confirms the same 4 fixes on time at 4 days each (100%). |
| M-02 | Run the tracker at least once before each follow-up due date. | A run every 7 days or sooner matches the default `FOLLOW_UP_DAYS` window and keeps K-07 and K-08 close to when fixes happened. |
| M-03 | A reopened issue keeps the original Date Flagged. | Days Open for a reopened issue includes the time before the first resolution. |
| M-04 | Issues with no worker count under `(unassigned)`. | K-10 shows `(unassigned)` as its own row. A count above zero there points to an assignment gap for the Supervisor. |
