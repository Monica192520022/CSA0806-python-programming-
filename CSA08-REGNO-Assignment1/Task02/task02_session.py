"""Task 2 - reproduces an interactive (>>>) session so it can be pasted as evidence."""
import code
import contextlib
import io

LINES = [
    "type(10)", "type(10.0)", 'type("10")', "type(True)", "type([10, 8.5])",
    "isinstance(True, int)", "True + True",
    "7 / 2", "7 // 2", "7 % 2", "-7 // 2", "-7 % 2",
    "0.1 + 0.2", "0.1 + 0.2 == 0.3", "round(0.1 + 0.2, 2) == 0.3",
    "(4.2 - 3.5) / 0.1",
    "from decimal import Decimal",
    "Decimal('0.1') + Decimal('0.2')",
    "Decimal('0.1') + Decimal('0.2') == Decimal('0.3')",
    "Decimal(0.1)",
    "Decimal('0.1')",
    "int(33.40 * 100)",
    "round(33.40 * 100)",
    "'10' + 5",
]

console = code.InteractiveConsole()
for line in LINES:
    buffer = io.StringIO()
    with contextlib.redirect_stdout(buffer), contextlib.redirect_stderr(buffer):
        console.push(line)
    print(">>>", line)
    out = buffer.getvalue()
    if out:
        print(out, end="" if out.endswith("\n") else "\n")
