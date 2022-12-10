# Day: 2022-12-10

from helpers import readlines

lines = readlines("day10.txt")

X = 1
cycles = []
for lidx, line in enumerate(lines):
    if line.strip() == "noop":
        cycles.append(X)
    elif line.startswith("addx"):
        addval = int(line.split()[1])
        cycles += [X, X]
        X += addval

part1 = sum(idx * cycles[idx - 1] for idx in range(20, len(cycles), 40))
print(part1)

# part 2
lines = []
currline = ""
for idx, value in enumerate(cycles):
    if idx % 40 in range(value - 1, value + 2):
        currline += "██"  # using 2 characters reads easier
    else:
        currline += "  "
    if idx % 40 == 39:
        lines.append(currline)
        currline = ""

print("\n".join(lines))
