rows, cols = 3, 4

bad = [[0] * cols] * rows          # every row is the SAME list object
bad[0][1] = 7

# TODO 1: Create a rows x cols grid of zeros using a list comprehension so that every
#   row is a separate list
pass  # replace this line with your code

good[0][1] = 7

print("bad :", bad)
print("good:", good)
print(bad[0] is bad[1], good[0] is good[1])

# Tuples are immutable, so they can be used as dictionary keys
stops = {(13.0827, 80.2707): "Chennai Central", (13.0418, 80.2341): "T. Nagar"}
print(stops[(13.0418, 80.2341)])

# Extra: try a list as a dictionary key and explain the error (in notes.md)
# stops[[13.0418, 80.2341]] = "x"
