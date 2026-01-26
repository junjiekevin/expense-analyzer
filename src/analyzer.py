import csv
from typing import List, Dict, Any
import utils
import categories

REQUIRED_COLUMNS = {"date", "description", "amount"}


def load_transactions(csv_path: str) -> List[Dict[str, Any]]:
    """Load and categorize transactions from a CSV file.

    Expects columns: date, description, amount
    - Parses date into datetime.date
    - Parses amount into float
    - Assigns a category based on description
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
                
                # Use utility helpers for parsing
                date_obj = utils.parse_date(date_str)
                amount = utils.parse_amount(amount_str)
                
                if date_obj is None or amount is None:
                    print(f"Warning: Skipping malformed row {idx}: parsing error")
                    continue
                
                # Assign category
                category = categories.categorize_transaction(descr, amount)
                
                transactions.append({
                    "date": date_obj, 
                    "description": descr, 
                    "amount": amount,
                    "category": category
                })
            except Exception as e:
                print(f"Warning: Skipping row {idx} due to error: {e}")
    return transactions


def main():
    import argparse
    parser = argparse.ArgumentParser(description="Smart Expense Analyzer - Phase 2: Categorization")
    parser.add_argument("csv", help="Path to the transactions CSV file")
    args = parser.parse_args()
    
    try:
        txns = load_transactions(args.csv)
        print(f"\nSuccessfully parsed and categorized {len(txns)} transactions:\n")
        print(f"{'Date':<12} | {'Description':<30} | {'Amount':>10} | {'Category':<15}")
        print("-" * 75)
        for t in txns:
            print(f"{str(t['date']):<12} | {t['description'][:30]:<30} | {t['amount']:>10.2f} | {t['category']:<15}")
    except Exception as e:
        print(f"Error: {e}")


if __name__ == "__main__":
    main()
