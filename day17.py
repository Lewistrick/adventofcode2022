# Day: 2022-12-17

from helpers import readchars
from tqdm import tqdm
from loguru import logger
from sys import stdout
import time

dirs = readchars("day17.txt")
# dirs = ">>><<><>><<<>><>>><<<>>><<<><<<>><>><<>>"  # example input
assert all(d in "><" for d in dirs)
block_order = "-+LIO"
DEBUG = False

if not DEBUG:
    logger.remove()
    logger.add(stdout, level="INFO")


def get_startpos(block, highest_y):
    maxy = max(highest_y)
    if block == "-":
        x_values = [2, 3, 4, 5]
        y_values = [maxy + 4 for _ in range(4)]
    elif block == "+":
        x_values = [3, 2, 3, 4, 3]
        y_values = [maxy + n + 4 for n in [2, 1, 1, 1, 0]]
    elif block == "L":  # actually _|
        x_values = [4, 4, 2, 3, 4]
        y_values = [maxy + n + 4 for n in [2, 1, 0, 0, 0]]
    elif block == "I":
        x_values = [2, 2, 2, 2]
        y_values = [maxy + n + 4 for n in range(4)]
    elif block == "O":
        x_values = [2, 3, 2, 3]
        y_values = [maxy + n + 4 for n in [0, 0, 1, 1]]

    return x_values, y_values


def overlaps(highest_y, xs, ys):
    for x, y in zip(xs, ys):
        curry = highest_y[x]
        if y == curry or y < 0:
            return True
    return False


def push(xs, dir, width):
    if dir == ">" and max(xs) < width - 1:
        new_xs = [x + 1 for x in xs]
    elif dir == "<" and min(xs) > 0:
        new_xs = [x - 1 for x in xs]
    else:
        new_xs = xs.copy()
    return new_xs


def solve1(width=7, nblocks=2022):
    highest_y = [-1 for _ in range(width)]

    dir_idx = 0
    for block_n in tqdm(range(nblocks), ascii=".#", desc="Dropping blocks"):
        block = block_order[block_n % len(block_order)]
        xs, ys = get_startpos(block, highest_y)

        if DEBUG:
            print()
            print(f"Before dropping block #{block_n} ({block}):")
            for y in range(max(ys), min(highest_y) - 1, -1):
                print(f"{y:5d}|", end="")
                for x in range(width):
                    if y <= highest_y[x]:
                        print("#", end="")
                    elif (x, y) in zip(xs, ys):
                        print("@", end="")
                    else:
                        print(".", end="")
                print(f"|")
            print(f"     +{'-' * width}+")
            input("$")

        logger.debug("-" * 80)
        logger.debug(f"Block #{block_n} ({block}) at {list(zip(xs, ys))}")
        while True:
            # first push
            new_xs = push(xs, dirs[dir_idx], width)
            if xs == new_xs:
                logger.debug(f"Could not push {dirs[dir_idx]} (at side of board)")
                pass
            elif not overlaps(highest_y, new_xs, ys):
                xs = new_xs
                logger.debug(f"After push {dirs[dir_idx]}: {list(zip(xs, ys))}")
            else:
                logger.debug("Could not push (against other block)")

            # update push direction
            dir_idx = (dir_idx + 1) % len(dirs)

            # then fall
            new_ys = [y - 1 for y in ys]
            if overlaps(highest_y, xs, new_ys):
                break
            else:
                ys = new_ys
                logger.debug(f"After fall v: {list(zip(xs, ys))}")

        # the block has landed, update highest_y
        for x, y in zip(xs, ys):
            highest_y[x] = max(highest_y[x], y)

        logger.debug(f"After {block_n} blocks: {highest_y}")

    solution = max(highest_y)
    logger.info(f"Solution: {solution}")
    return solution


# part 1
print(solve1())  # too high: 3186
