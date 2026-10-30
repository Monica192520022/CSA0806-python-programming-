OTP = "4821"
def while_version(inputs):
    attempts = 0
    it = iter(inputs)
    while attempts < 3:
        entry = next(it, "").strip()
        if entry == "":
            continue                      # blank: not counted
        attempts += 1                     # counter updated only AFTER a real entry
        if entry == OTP:
            print("  OK on attempt", attempts); break
        print("  wrong, attempt", attempts)
    else:
        print("  LOCKED for 30 minutes")

def for_version(inputs):
    it = iter(inputs)
    for attempt in range(1, 4):
        entry = next(it, "").strip()
        if entry == "":
            pass                          # blank: placeholder (but burns an attempt in for!)
        if entry == OTP:
            print("  OK on attempt", attempt); break
        print("  wrong/blank, attempt", attempt)
    else:
        print("  LOCKED for 30 minutes")

def extended(inputs, security_ok):
    max_attempts = 3 + (2 if security_ok else 0)
    attempts = 0
    it = iter(inputs)
    while attempts < max_attempts:
        entry = next(it, "").strip()
        if not entry: continue
        attempts += 1
        if entry == OTP:
            print("  OK on attempt", attempts); break
    else:
        print(f"  LOCKED after {max_attempts} attempts")

def recursive(inputs, attempt=1, max_attempts=3):
    if attempt > max_attempts:
        print("  LOCKED for 30 minutes"); return
    entry = inputs[attempt-1] if attempt-1 < len(inputs) else ""
    if entry == OTP:
        print("  OK on attempt", attempt); return
    recursive(inputs, attempt+1, max_attempts)

print("while, blank ignored:"); while_version(["1111","","2222","","3333"])
print("while, success:"); while_version(["", "4821"])
print("for, blank burns attempt:"); for_version(["1111","","2222"])
print("extended (security ok), 5 wrong:"); extended(["1","2","3","4","5"], True)
print("extended (security failed), 5 wrong:"); extended(["1","2","3","4","5"], False)
print("recursive:"); recursive(["1","2","3"])
