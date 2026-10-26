"""Task 7 - second script that imports milkrate and demonstrates the __name__ test."""
import importlib
import os
import sys
import tempfile
import time

t0 = time.perf_counter()
import milkrate                                  # first import: file is read and run
first_import = time.perf_counter() - t0

print("(no table was printed above: milkrate.__name__ is", repr(milkrate.__name__) + ",")
print(" not '__main__', so the block under  if __name__ == '__main__'  was skipped)\n")

print("1) Three ways of importing")
from milkrate import payout                      # noqa: E402
import milkrate as mr                            # noqa: E402
print("   milkrate.payout(8.5, 4.2, 8.7)      =", milkrate.payout(8.5, 4.2, 8.7))
print("   payout(8.5, 4.2, 8.7)               =", payout(8.5, 4.2, 8.7))
print("   mr.rate_per_litre(3.1, 8.3)         =", mr.rate_per_litre(3.1, 8.3))
print("   same function object?", milkrate.payout is payout is mr.payout)

print("\n2) This script's own __name__ =", repr(__name__))

print("\n3) Where Python looks for modules (first 3 entries of sys.path)")
for p in sys.path[:3]:
    print("  ", p)
print("   milkrate was loaded from:", milkrate.__file__)

print("\n4) Import cost: Python loads a module once and keeps it in sys.modules")
print("   'milkrate' in sys.modules:", "milkrate" in sys.modules)
t0 = time.perf_counter()
import milkrate                                  # noqa: E402,F811  (cache hit)
second_import = time.perf_counter() - t0
t0 = time.perf_counter()
importlib.reload(milkrate)                       # forces a re-read from disk
reload_time = time.perf_counter() - t0
print(f"   first import : {first_import * 1e6:9.1f} microseconds")
print(f"   second import: {second_import * 1e6:9.1f} microseconds (from sys.modules)")
print(f"   reload       : {reload_time * 1e6:9.1f} microseconds (re-reads the file)")

print("\n5) What happens WITHOUT the  if __name__ == '__main__'  guard")
folder = tempfile.mkdtemp()
with open(os.path.join(folder, "noguard.py"), "w") as f:
    f.write("print('   >>> noguard: this table line prints on import!')\n")
sys.path.insert(0, folder)
import noguard                                   # noqa: E402,F401
print("   The module printed text just because it was imported.")
