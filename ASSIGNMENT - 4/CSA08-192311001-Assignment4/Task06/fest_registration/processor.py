import os
from .validator import validate_record

def process_department_files(file_list):
    master_records = {}
    error_logs = []
    seen_regs = set()
    
    for file_path in file_list:
        if not os.path.exists(file_path):
            error_logs.append((file_path, 0, "Missing department file"))
            continue
        with open(file_path, 'r', encoding='utf-8') as f:
            for line_no, line in enumerate(f, start=1):
                if not line.strip(): continue
                try:
                    reg, name, dept, email, events = validate_record(line)
                    if reg in seen_regs:
                        error_logs.append((file_path, line_no, f"Duplicate registration for {reg}"))
                        continue
                    seen_regs.add(reg)
                    master_records[reg] = {
                        'name': name, 'dept': dept, 'email': email, 'events': events.split(';')
                    }
                except Exception as e:
                    error_logs.append((file_path, line_no, str(e)))
                    
    return master_records, error_logs
