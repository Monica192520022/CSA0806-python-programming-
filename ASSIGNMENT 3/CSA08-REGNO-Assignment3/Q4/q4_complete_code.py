ai_elective = {"192311001", "192311004", "192311007", "192311009"}
iot_elective = {"192311002", "192311004", "192311009", "192311010"}
all_students = {f"1923110{i:02d}" for i in range(1, 11)}

# TODO 1: Use set operators to find: students in both electives, students in exactly
#   one, and students in neither
pass  # replace this line with your code

print("clash      :", sorted(both))
print("exactly one:", sorted(exactly_one))
print("neither    :", sorted(neither))

# Then rewrite using set methods (intersection, symmetric_difference, difference, union)
# and check results are the same.
