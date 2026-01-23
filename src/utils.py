from datetime import datetime
from typing import Optional


def parse_date(date_str: str) -> Optional[object]:
    """Parse a date string in YYYY-MM-DD format to a date object."""
    try:
        return datetime.strptime(date_str, "%Y-%m-%d").date()
    except Exception:
        return None


def parse_amount(amount_str: str) -> Optional[float]:
    """Parse a numeric amount string to float. Returns None on failure."""
    try:
        return float(amount_str)
    except Exception:
        return None
