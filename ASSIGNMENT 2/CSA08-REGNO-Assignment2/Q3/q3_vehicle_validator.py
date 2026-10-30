def normalise(text):
    return text.replace(" ", "").replace("-", "").upper()

def is_valid(reg):
    if len(reg) not in (9, 10):
        return False
    series_len = len(reg) - 8             # 1 or 2
    state    = reg[:2]
    district = reg[2:4]
    series   = reg[4:4+series_len]
    number   = reg[-4:]
    return (state.isalpha() and district.isdigit()
            and series.isalpha() and number.isdigit())

def format_reg(reg):
    return " ".join([reg[:2], reg[2:4], reg[4:-4], reg[-4:]])

for raw in ["tn 09 ab 1234", "KA-01-M-0007", "TN9AB1234", "TN 22 1234 AB"]:
    reg = normalise(raw)
    print(f"{raw:15} -> {reg:11} {'valid' if is_valid(reg) else 'INVALID'}")
print(format_reg("TN09AB1234"), "|", format_reg("KA01M0007"))
for s in ["TN09AB1234","KA01M0007"]:
    print(s, len(s), "s[-4:]=",s[-4:], "s[4:-4]=",s[4:-4])
s="tn"; t=s.upper(); print(s,t)
extra = ["Tn09Ab1234","", "TN 09 ABC 1234","1N09AB1234","TN0AAB1234"]
for e in extra:
    r=normalise(e); print(repr(e),"->",repr(r), is_valid(r))
