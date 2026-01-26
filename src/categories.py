import utils

# Expanded category mapping (Phase 2)
CATEGORIES = {
    "Food": ["starbucks", "restaurant", "cafe", "whole foods", "mcdonalds", "chipotle", "grocery", "bakery"],
    "Transport": ["uber", "lyft", "bus", "train", "gas", "petrol", "parking", "bridge toll"],
    "Rent": ["rent", "mortgage", "housing"],
    "Subscriptions": ["netflix", "spotify", "hulu", "disney", "prime", "apple music", "gym"],
    "Utilities": ["electric", "water", "gas bill", "internet", "phone", "verizon", "att"],
    "Shopping": ["amazon", "target", "walmart", "best buy", "clothing", "electronics"]
}


def categorize_transaction(description: str, amount: float) -> str:
    """Assign a category to a transaction based on description and amount.
    
    - If amount > 0, category is 'Income'
    - Otherwise, find a match in CATEGORIES keywords
    - Default to 'Other'
    """
    if amount > 0:
        return "Income"
    
    norm_descr = utils.normalize_text(description)
    
    for category, keywords in CATEGORIES.items():
        if any(kw in norm_descr for kw in keywords):
            return category
            
    return "Other"
