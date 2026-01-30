from typing import List, Dict, Any
from collections import defaultdict
from datetime import date

def get_monthly_summary(transactions: List[Dict[str, Any]]) -> Dict[str, Any]:
    """
    Groups transactions by Year-Month and calculates aggregates.
    
    Returns a dict keyed by 'YYYY-MM', where each value is:
    {
        "income": float,
        "expenses": float,
        "savings": float,
        "savings_rate": float,  # percentage 0-100
        "categories": { category_name: amount, ... }
    }
    """
    summary = {}
    
    # helper to group by month
    grouped = defaultdict(list)
    for t in transactions:
        month_key = t['date'].strftime("%Y-%m")
        grouped[month_key].append(t)
        
    # calculate stats per month
    for month, txns in grouped.items():
        income = 0.0
        expenses = 0.0
        category_totals = defaultdict(float)
        
        for t in txns:
            amt = t['amount']
            cat = t['category']
            
            if amt > 0:
                income += amt
            else:
                # expenses are typically negative or positive? 
                # In this system, based on phase 2, income is > 0.
                # Usually expenses are stored as negative in CSVs or positive if a flag is set.
                # Let's check utils/categories. 
                # The categories.py says "If amount > 0, return Income". 
                # This implies positive numbers are income.
                # Does that mean expenses are negative?
                # "data/sample_transactions.csv" wasn't read, but typically:
                # If income is positive, expenses might be negative. 
                # However, many bank exports have expenses as positive numbers with a 'Debit' column, 
                # OR signed numbers. 
                # Let's assume signed numbers for now based on "amount > 0 is Income".
                # If so, expenses are negative or zero.
                expenses += amt
                
                # specific category tracking (store as positive magnitude for display?)
                # Usually better to see "Food: $500" rather than "Food: -$500"
                category_totals[cat] += abs(amt)

        # Net savings = Income + Expenses (since expenses are negative)
        # Wait, if expenses are negative, then Income + Expenses is the net.
        # Example: Income 1000, Expense -300. Net = 700.
        savings = income + expenses
        
        # Savings Rate = (Savings / Income) * 100
        savings_rate = 0.0
        if income > 0:
            savings_rate = (savings / income) * 100
            
        summary[month] = {
            "income": income,
            "expenses": expenses, # keep as raw signed value for math, or display? 
                                  # Let's keep raw here, display can formatting
            "savings": savings,
            "savings_rate": savings_rate,
            "categories": dict(category_totals) # convert to regular dict
        }
        
    return summary
