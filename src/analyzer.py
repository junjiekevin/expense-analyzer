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
    from datetime import date
    parser = argparse.ArgumentParser(description="Smart Expense Analyzer - Phase 4: Terminal Output & Reporting")
    parser.add_argument("csv", help="Path to the transactions CSV file")
    args = parser.parse_args()
    
    try:
        txns = load_transactions(args.csv)
        
        # Period Summary Header
        if not txns:
            print("\nNo transactions found to analyze.")
            return
            
        dates = [t['date'] for t in txns]
        min_date = min(dates)
        max_date = max(dates)
        period_str = f"{min_date.strftime('%B %Y')} - {max_date.strftime('%B %Y')}"
        
        print("\n" + "="*60)
        print("  SMART EXPENSE ANALYZER")
        print("="*60)
        print(f"  Period: {period_str}")
        print(f"  Transactions: {len(txns)}")
        print("="*60)
        
        # Transaction Table
        print(f"\n{'Date':<12} | {'Description':<30} | {'Amount':>10} | {'Category':<15}")
        print("-" * 75)
        for t in txns:
            print(f"{str(t['date']):<12} | {t['description'][:30]:<30} | {t['amount']:>10.2f} | {t['category']:<15}")

    except Exception as e:
        print(f"Error: {e}")
        return

    # Monthly Aggregation
    import stats
    monthly_data = stats.get_monthly_summary(txns)
    
    for month, data in sorted(monthly_data.items()):
        month_name = date(int(month.split('-')[0]), int(month.split('-')[1]), 1).strftime('%B %Y')
        
        print("\n" + "="*60)
        print(f"  {month_name.upper()} SUMMARY")
        print("="*60)
        
        income_str = f"${data['income']:,.2f}"
        expenses_str = f"${abs(data['expenses']):,.2f}"
        savings_str = f"${data['savings']:,.2f}"
        rate_str = f"{data['savings_rate']:.1f}%"
        
        print(f"\n  Total Income:      {income_str:>15}")
        print(f"  Total Expenses:    {expenses_str:>15}")
        print(f"  Net Savings:       {savings_str:>15}")
        print(f"  Savings Rate:      {rate_str:>15}")
        
        print("\n" + "-"*60)
        print("  TOP SPENDING CATEGORIES")
        print("-"*60)
        
        # Calculate category percentages
        total_expenses = abs(data['expenses'])
        sorted_cats = sorted(data['categories'].items(), key=lambda x: x[1], reverse=True)
        
        for cat, amt in sorted_cats:
            pct = (amt / total_expenses * 100) if total_expenses > 0 else 0.0
            print(f"  {cat:<18} ${amt:>10,.2f}  ({pct:>5.1f}%)")
        
        print("="*60)


if __name__ == "__main__":
    main()
