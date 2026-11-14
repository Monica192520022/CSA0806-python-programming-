# Task 3: Complete the Code - Attendance Processor
import os
import tempfile

class InvalidRecord(Exception):
    """Raised when a line of the attendance file is not in the expected format."""
    pass

def parse_line(line):
    """'192311001,2026-10-08,P' -> ('192311001', '2026-10-08', 'P')"""
    parts = line.strip().split(",")
    # TODO 1: Raise InvalidRecord if there are not exactly 3 fields or the status is not P or A
    if len(parts) != 3:
        raise InvalidRecord("expected 3 fields, found {}".format(len(parts)))
    reg, date, status = parts[0].strip(), parts[1].strip(), parts[2].strip()
    if status not in ("P", "A"):
        raise InvalidRecord(f"invalid status '{status}'")
    return (reg, date, status)

def summarise(path):
    present, absent, errors = 0, 0, []
    # TODO 2: Open the file with a with statement, parse each line inside try/except InvalidRecord
    try:
        with open(path, "r", encoding="utf-8") as f:
            for line_no, line in enumerate(f, start=1):
                if not line.strip():
                    continue
                try:
                    reg, date, status = parse_line(line)
                    if status == "P":
                        present += 1
                    elif status == "A":
                        absent += 1
                except InvalidRecord as e:
                    errors.append((line_no, str(e)))
                except Exception as e:
                    errors.append((line_no, f"unexpected error: {e}"))
    except FileNotFoundError as e:
        raise FileNotFoundError(f"Attendance file missing: {path}") from e
    return present, absent, errors

if __name__ == "__main__":
    data = ("192311001,2026-10-08,P\n192311002,2026-10-08,A\n"
            "192311003,2026-10-08\n192311004,2026-10-08,L\n")
    with tempfile.NamedTemporaryFile("w", suffix=".csv", delete=False, encoding="utf-8") as tmp:
        tmp.write(data)
        tmp_name = tmp.name
    
    print("Execution Result:", summarise(tmp_name))
    os.remove(tmp_name)
