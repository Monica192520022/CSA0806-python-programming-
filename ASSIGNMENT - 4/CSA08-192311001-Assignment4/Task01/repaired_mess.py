# Task 1.2: Repaired Mess Bill Script
import os

def process_mess_bills(file_path):
    total = 0.0
    report_lines = []
    rejected_lines = []
    
    if not os.path.exists(file_path):
        print(f"Error: File {file_path} not found.")
        return
        
    with open(file_path, "r", encoding="utf-8") as f:
        for line_num, line in enumerate(f, start=1):
            line_str = line.strip()
            if not line_str:  # Skip empty lines
                continue
            parts = line_str.split(",")
            if len(parts) != 3:
                rejected_lines.append((line_num, line_str, "Expected 3 comma-separated fields"))
                continue
            try:
                reg_no, name, amount_str = parts[0].strip(), parts[1].strip(), parts[2].strip()
                amount = float(amount_str) # Supports paise (.50)
                total += amount
                report_lines.append(f"{name}: ₹{amount:.2f}")
            except ValueError as e:
                rejected_lines.append((line_num, line_str, f"Invalid numeric amount: {e}"))
                
    print("--- MONTHLY MESS BILL REPORT ---")
    print("\n".join(report_lines))
    print(f"--------------------------------")
    print(f"Total Collection: ₹{total:.2f}\n")
    
    if rejected_lines:
        print("--- REJECTED LINES LOG ---")
        for r in rejected_lines:
            print(f"Line {r[0]}: '{r[1]}' -> Reason: {r[2]}")

if __name__ == "__main__":
    process_mess_bills("mess_oct.txt")
