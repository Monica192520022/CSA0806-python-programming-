import random, time, sys

timetable = {
    # "12601": {"name": "Chennai Mail",
    #           "stops": [("Chennai", "--", "20:00"), ("Katpadi", "22:10", "22:15")],
    #           "days": {"Mon", "Wed", "Fri"}},
    # TODO: at least 5 trains
}

def trains_at(station, day):
    pass  # TODO

def sorted_by_departure(station, day):
    pass  # TODO: sorted(..., key=lambda ...)

def print_timetable():
    pass  # TODO: neat output

def build_index(tt):
    pass  # TODO: station -> list of train numbers

def generate(n):
    pass  # TODO: random timetable with n trains

def experiment():
    for n in (100, 1_000, 10_000):
        pass  # TODO: time queries with/without index; memory of index

if __name__ == "__main__":
    # TODO: tests - unknown station, train not running on the day
    experiment()
    # TODO (alternative): flat list of (train, station, arr, dep, days) tuples
