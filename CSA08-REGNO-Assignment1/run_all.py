"""Runs every program of the assignment and stores its output next to the source
(output_<script>.txt).  Usage:  python run_all.py
"""
import os
import subprocess
import sys

JOBS = [
    ("Task01", ["task01_analysis.py"]),
    ("Task02", ["task02_session.py"], ["task02_complete.py"], ["task02_alternatives.py"]),
    ("Task03", ["task03_constants.py"]),
    ("Task04", ["task04_expressions.py"]),
    ("Task05", ["task05_input.py"]),
    ("Task06", ["task06_functions.py"]),
    ("Task07", ["milkrate.py"], ["use_milkrate.py"]),
    ("Task08", ["task08_algorithm.py"]),
    ("Task09", ["calculator.py", "entries.csv"], ["test_calculator.py"]),
    ("Task10", ["task10_compare.py"]),
    ("Task11", ["task11_recommend.py"]),
    ("Task12", ["evaluate_old_design.py"], ["test_task12.py"]),
]

root = os.path.dirname(os.path.abspath(__file__))
for folder, *commands in JOBS:
    if isinstance(commands[0], str):
        commands = [commands]
    for command in commands:
        script = command[0]
        cwd = os.path.join(root, folder)
        result = subprocess.run([sys.executable] + command, cwd=cwd, capture_output=True, text=True)
        out_name = "output_" + os.path.splitext(script)[0] + ".txt"
        with open(os.path.join(cwd, out_name), "w", encoding="utf-8") as f:
            f.write(result.stdout + result.stderr)
        status = "OK " if result.returncode == 0 else "ERR"
        print(f"{status} {folder}/{script:<28} -> {out_name}")
