# 💸 Smart Expense Analyzer (Python CLI)

A lightweight Python command-line tool that analyzes personal finance transactions from a CSV file and generates clear spending summaries and insights.

This project focuses on **clean Python fundamentals**, real-world data handling, and readable output — without unnecessary complexity.

---

## 🚀 Features

- Parse transaction data from a CSV file
- Automatically categorize expenses using keyword matching
- Generate a monthly financial summary
- Calculate key metrics:
  - Total income
  - Total expenses
  - Savings rate
- Display spending breakdown by category
- Provide simple, human-readable insights

---

## 📂 Project Structure

```
smart-expense-analyzer/
├── README.md
├── data/
│   └── sample_transactions.csv
├── src/
│   ├── analyzer.py        # Main CLI entry point
│   ├── categories.py     # Expense categorization rules
│   └── utils.py          # Helper functions (formatting, parsing)
└── requirements.txt
```

---

## 📥 Input Format

The analyzer expects a CSV file with the following columns:

```csv
date,description,amount
2025-01-02,Starbucks,-6.45
2025-01-03,Whole Foods,-52.30
2025-01-05,Uber,-18.90
2025-01-06,Rent,-1400.00
2025-01-10,Netflix,-15.99
2025-01-15,Salary,3200.00
```

### Rules
- **Negative values** → expenses  
- **Positive values** → income  
- Dates must be in `YYYY-MM-DD` format  

---

## ▶️ How to Run

1. Clone the repository:
```bash
git clone https://github.com/your-username/smart-expense-analyzer.git
cd smart-expense-analyzer
```

2. (Optional) Create a virtual environment:
```bash
python -m venv venv
source venv/bin/activate   # Windows: venv\Scripts\activate
```

3. Run the analyzer:
```bash
python src/analyzer.py data/sample_transactions.csv
```

---

## 📊 Example Output

```
📊 Smart Expense Analyzer
-------------------------
Period: January 2025

Total Income:     $3,200.00
Total Expenses:   $1,493.64
Savings Rate:     53.3%

Top Categories:
1. Rent          $1,400.00 (93.7%)
2. Food            $58.75  (3.9%)
3. Transport       $18.90  (1.3%)

Insights:
- ⚠️ Rent dominates your spending.
- ✅ Food spending is well controlled.
```

---

## 🧠 Categorization Logic

Expenses are categorized using keyword matching defined in `categories.py`.

Example:
```python
CATEGORIES = {
    "Food": ["starbucks", "restaurant", "cafe", "whole foods"],
    "Transport": ["uber", "lyft", "bus", "train"],
    "Rent": ["rent"],
    "Subscriptions": ["netflix", "spotify"]
}
```

If no keywords match, the transaction is assigned to **"Other"**.

---

## 🛠️ Technologies Used

- Python 3
- Standard library only (`csv`, `datetime`, `collections`, `sys`)
- No external dependencies

---

## 🎯 Design Philosophy

- Keep complexity low and logic explicit
- Favor readability over cleverness
- Avoid unnecessary frameworks, databases, or GUIs
- Build a complete, usable tool rather than a demo

---

## 📈 Possible Extensions (Optional)

These are intentionally **not implemented** to keep scope controlled:
- Export summary to a text or CSV report
- Support filtering by month or date range
- Add simple visualizations (matplotlib)
- Allow user-defined categories

---

## 📚 What I Learned

- Structuring a Python CLI application
- Parsing and validating real-world CSV data
- Designing clean aggregation logic
- Writing readable, user-focused terminal output
- Keeping project scope intentional and finished

---

## 👤 Author

Kevin Lee  
Built as a portfolio project to demonstrate Python fundamentals, data reasoning, and clean software structure.
