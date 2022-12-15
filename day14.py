# Day: 2022-12-14

from helpers import readlines
from itertools import count

filled = set()
minx, maxx, miny, maxy = 1000, 0, 0, 0

for line in readlines("day14.txt"):
    coords = line.split(" -> ")
    prevx, prevy = None, None
    for coord in coords:
        currx, curry = map(int, coord.split(","))
        if not prevx:
            prevx, prevy = currx, curry
            continue

        if prevx == currx:
            ysrc, ydst = sorted((prevy, curry))
            for y in range(ysrc, ydst + 1):
                filled.add((currx, y))
                miny = min(miny, y)
                maxy = max(maxy, y)
        else:
            xsrc, xdst = sorted((prevx, currx))
            for x in range(xsrc, xdst + 1):
                filled.add((x, curry))
                minx = min(minx, x)
                maxx = max(maxx, x)

        prevx, prevy = currx, curry

print(minx, maxx, miny, maxy)

srcx, srcy = 500, 0


def print_map():
    for y in range(miny, maxy + 1):
        for x in range(minx, maxx + 1):
            if (x, y) == (srcx, srcy):
                print("+", end="")
            elif (x, y) in filled:
                print("#", end="")
            else:
                print(".", end="")
        print()


# print_map()
# print()

show_next = 0
for sand_i in count():
    # drop a sand unit
    if sand_i >= show_next:
        print(f"Dropping unit #{sand_i}")
        show_next += sand_i

    x, y = srcx, srcy
    full = False
    while not full:
        if y > maxy:
            full = True
            break
        # try moving down
        elif (x, y + 1) not in filled:
            y += 1
        # try moving down-left
        elif (x - 1, y + 1) not in filled:
            x -= 1
            y += 1
        # try moving down-right
        elif (x + 1, y + 1) not in filled:
            x += 1
            y += 1
        # we're stuck
        else:
            filled.add((x, y))
            break

    if full:
        break

# part 1
print(f"part 1: {sand_i}")

# part 2
maxy += 1
for sand_i in count(sand_i + 1):
    # keep dropping sand units
    if sand_i >= show_next:
        print(f"Dropping unit #{sand_i}")
        show_next += sand_i

    x, y = srcx, srcy
    while True:
        if y == maxy:
            filled.add((x, y))
            break
        # try moving down
        elif (x, y + 1) not in filled:
            y += 1
        # try moving down-left
        elif (x - 1, y + 1) not in filled:
            x -= 1
            minx = min(minx, x)
            y += 1
        # try moving down-right
        elif (x + 1, y + 1) not in filled:
            x += 1
            maxx = max(maxx, x)
            y += 1
        # we're stuck
        else:
            filled.add((x, y))
            break

    # print_map()

    # print(f"Sand grain fell down at ({x}, {y})")

    # check if we're done
    if (srcx, srcy) in filled:
        break

print(f"part 2: {sand_i}")  # 26075 is too high
