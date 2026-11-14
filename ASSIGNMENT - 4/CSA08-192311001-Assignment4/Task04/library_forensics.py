# Task 4: Library Returns Forensics - Repaired Script
import os
import datetime

def save_returns(books, log_file="returns.log"):
    # Repaired: Use append mode ('a') and newline characters
    try:
        with open(log_file, "a", encoding="utf-8") as log:
            for b in books:
                if b.strip():
                    log.write(b.strip() + "\n")
    except IOError as e:
        with open("error.log", "a", encoding="utf-8") as err_log:
            err_log.write(f"{datetime.datetime.now()} - Error writing returns: {e}\n")

def process(day_file):
    try:
        with open(day_file, "r", encoding="utf-8") as f:
            books = f.read().splitlines()
        save_returns(books)
    except FileNotFoundError:
        print(f"Error: Missing file {day_file}")
    except PermissionError:
        print(f"Error: Permission denied for {day_file}")

if __name__ == "__main__":
    # Test simulation
    open("day1_returns.txt", "w").write("BookA\nBookB\n")
    open("day2_returns.txt", "w").write("BookC\n")
    
    if os.path.exists("returns.log"):
        os.remove("returns.log")
        
    process("day1_returns.txt")
    process("day2_returns.txt")
    
    print("--- returns.log content ---")
    if os.path.exists("returns.log"):
        print(open("returns.log", "r").read())
        
    # Cleanup
    for fn in ["day1_returns.txt", "day2_returns.txt", "returns.log"]:
        if os.path.exists(fn):
            os.remove(fn)
