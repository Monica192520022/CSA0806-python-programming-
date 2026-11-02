import random, time

def normalise_number(raw):
    # TODO: keep digits only, drop leading +91 / 0, keep last 10 digits
    pass

def normalise_name(raw):
    # TODO: lowercase, strip, remove "dr."/"mr." etc., collapse spaces
    pass

def merge_contacts(*contact_lists):
    # TODO: dict keyed by normalised number; values hold names (set), numbers (set), emails (set)
    pass

def merge_pairwise(contacts):
    pass  # TODO (alternative): O(n^2) all-pairs comparison

def generate(n):
    pass  # TODO: n random contacts with duplicates / formats

def experiment():
    for n in (1_000, 100_000):
        pass  # TODO: time dict version (and pairwise for 1,000)

if __name__ == "__main__":
    # TODO: small hand-verified example, missing fields, different formats, same-name different people
    experiment()
