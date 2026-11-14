# Task 6: College Fest Registration Desk Main
from fest_registration.processor import process_department_files
from fest_registration.reporter import write_outputs
import os

if __name__ == '__main__':
    # Create sample department file
    sample_file = "dept_cse.txt"
    with open(sample_file, "w", encoding="utf-8") as f:
        f.write("192311001,Aarav,CSE,aarav@gmail.com,Coding;Quiz\n")
        f.write("192311001,Aarav,CSE,aarav@gmail.com,Coding;Quiz\n") # Duplicate
        f.write("192311002,Priya,CSE,bad-email,Dance\n") # Bad email
        f.write("192311003,Rahul,CSE,rahul@gmail.com\n") # Damaged line
        
    master, errors = process_department_files([sample_file, "missing_dept.txt"])
    write_outputs(master, errors)
    
    if os.path.exists(sample_file):
        os.remove(sample_file)
