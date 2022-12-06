from collections import deque
from pathlib import Path

line = Path("day06.txt").read_text().strip()
d = deque(maxlen=4)
d2 = deque(maxlen=14)

# line = "mjqjpqmgbljsphdztnvjfqwrcgsmlb"

p1_seen = False
for i, c in enumerate(line):
    d.append(c)
    d2.append(c)
    if len(set(d)) == 4 and not p1_seen:
        print("part 1:", i + 1)
        p1_seen = True
    if len(set(d2)) == 14:
        print("part 2:", i + 1)
        break
