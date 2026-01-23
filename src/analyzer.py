import csv
from datetime import datetime
from typing import List, Dict, Any

REQUIRED_COLUMNS = {"date", "description", "amount"}


def load_transactions(csv_path: str) -> List[Dict[str, Any]]:
    """Load transactions from a CSV file.

    Expects columns: date, description, amount
    - Parses date into datetime.date
    - Parses amount into float
    - Skips malformed rows with a warning
    """
    transactions: List[Dict[str, Any]] = []
    with open(csv_path, newline='', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        if not reader.fieldnames:
            print("Error: CSV has no header row.")
            return transactions
        # Normalize header names to lower-case for robust checks
        header_set = set(col.lower() for col in reader.fieldnames)
        if not REQUIRED_COLUMNS.issubset(header_set):
            missing = REQUIRED_COLUMNS - header_set
            raise ValueError(f"CSV is missing required columns: {', '.join(sorted(missing))}")

        for idx, row in enumerate(reader, start=2):  # header is row 1
            try:
                date_str = (row.get("date") or "").strip()
                descr = (row.get("description") or "").strip()
                amount_str = (row.get("amount") or "").strip()
                if not date_str or not descr or amount_str == "":
                    print(f"Warning: Skipping malformed row {idx}: missing fields")
                    continue
                # Parse date and amount
                date_obj = datetime.strptime(date_str, "%Y-%m-%d").date()
                amount = float(amount_str)
                transactions.append({"date": date_obj, "description": descr, "amount": amount})
            except Exception as e:
                print(f"Warning: Skipping row {idx} due to error: {e}")
    return transactions


def main():
    import argparse
    parser = argparse.ArgumentParser(description="Smart Expense Analyzer - Phase 1: CSV Parsing")
    parser.add_argument("csv", help="Path to the transactions CSV file")
    args = parser.parse_args()
    txns = load_transactions(args.csv)
    print(f"Parsed {len(txns)} transactions:")
    for t in txns:
        print(f"{t['date']} | {t['description'][:40]:40} | {t['amount']:.2f}")


if __name__ == "__main__":
    main()
