import re

def extract_numbers(text):
    """Find all numbers (with $ and other prefixes) in text"""
 
    patterns = [
        r'\$[\d,]+\.?\d*',      # Dollar amounts: $2.5, $2,500
        r'\d+\.?\d*%',          # Percentages: 25%, 30.5%
        r'\d{1,3}(?:,\d{3})*',  # Numbers with commas: 1,200, 15,000
        r'\d+\.?\d*'            # Plain numbers: 2.5, 25
    ]

    numbers = []
    for pattern in patterns:
        matches = re.findall(pattern, text)
        numbers.extend(matches)
    
    return numbers