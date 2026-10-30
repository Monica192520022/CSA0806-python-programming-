# Q1 - State Electricity Subsidy Eligibility

def buggy(units, ration, senior):
    """Separate if statements: conditions overlap, so more than one can fire."""
    result = []
    if units <= 100:
        result.append("FULL")
    if units <= 200 and ration:          # missing lower bound (101)
        result.append("PARTIAL")
    if units > 200 and senior:
        result.append("SENIOR")
    return result or ["NONE"]

def fixed_elif(units, ration, senior):
    """if-elif-else: exactly one branch runs."""
    if units <= 100:
        return "FULL"
    elif 101 <= units <= 200:
        return "PARTIAL" if ration else "NONE"
    else:                                 # units > 200
        return "SENIOR" if senior else "NONE"

def fixed_nested(units, ration, senior):
    """Nested version, for the design-decision comparison."""
    if units <= 100:
        return "FULL"
    else:
        if units <= 200:
            if ration:
                return "PARTIAL"
            return "NONE"
        else:
            if senior:
                return "SENIOR"
            return "NONE"

# (units, ration_card, senior_above_80, my predicted answer)
tests = [
    (50,  True,  False, "FULL"),
    (100, False, False, "FULL"),
    (101, True,  False, "PARTIAL"),
    (101, False, False, "NONE"),
    (200, True,  True,  "PARTIAL"),
    (200, False, True,  "NONE"),
    (201, False, True,  "SENIOR"),
    (250, True,  False, "NONE"),
]

print(f"{'units':>5} {'ration':>6} {'senior':>6} | {'predicted':9} | {'if-elif':9} | buggy (separate ifs)")
for u, r, s, pred in tests:
    new = fixed_elif(u, r, s)
    old = buggy(u, r, s)
    flag = "  <-- DOUBLE" if len(old) > 1 else ""
    assert new == pred == fixed_nested(u, r, s)
    print(f"{u:>5} {str(r):>6} {str(s):>6} | {pred:9} | {new:9} | {old}{flag}")
print("All predictions matched if-elif-else and nested versions.")
