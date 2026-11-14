def read_attendance(file_path):
    with open(file_path, 'r', encoding='utf-8') as f:
        return [line.strip().split(',') for line in f if line.strip()]
