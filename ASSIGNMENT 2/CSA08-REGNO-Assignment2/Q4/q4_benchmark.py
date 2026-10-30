import time
def build_plus(parts):
    text = ""
    for p in parts: text += p + ";"
    return text
def build_join(parts):
    return ";".join(parts) + ";"
def build_fstring(parts):
    text = ""
    for p in parts: text += f"{p};"
    return text
def build_fstring_join(parts):
    return "".join([f"{p};" for p in parts])
def build_stringio(parts):
    import io
    b = io.StringIO()
    for p in parts: b.write(p + ";")
    return b.getvalue()
for n in (1000, 10000, 200000):
    items = [f"Item{i}:Rs{i % 50}" for i in range(n)]
    row=[]
    for f in (build_plus, build_join, build_fstring_join, build_stringio):
        ts=[]
        for _ in range(3):
            s=time.perf_counter(); r=f(items); ts.append(time.perf_counter()-s)
        row.append(sum(ts)/3)
    print(n, " ".join(f"{x:.5f}" for x in row), len(r))
items = [f"Item{i}:Rs{i % 50}" for i in range(200_000)]
a=build_plus(items); b=build_join(items)
print("same text:", a==b, "| length:", len(b))
