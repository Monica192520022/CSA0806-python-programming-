import re

def is_valid_email(email):
    pattern = r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$'
    return bool(re.match(pattern, email))

def validate_record(line):
    parts = [p.strip() for p in line.strip().split(',')]
    if len(parts) != 5:
        raise ValueError("Expected 5 fields")
    reg, name, dept, email, events = parts
    if not is_valid_email(email):
        raise ValueError(f"Invalid email: {email}")
    return reg, name, dept, email, events
