def write_outputs(master_records, error_logs):
    print(f"Successfully processed {len(master_records)} unique valid registrations.")
    print(f"Logged {len(error_logs)} errors/duplicates.")
