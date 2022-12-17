# Day: 2022-12-17

from helpers import readchars
from tqdm import tqdm
from loguru import logger
from sys import stdout

# dirs = readchars("day17.txt")
dirs = ">>><<><>><<<>><>>><<<>>><<<><<<>><>><<>>"  # example input
assert all(d in "><" for d in dirs)
block_order = "-+LIO"
DEBUG = True

if not DEBUG:
    logger.remove()
    logger.add(stdout, level="INFO")


def get_startpos(block, grid, min_y, start_x=2):
    # put three empty rows at the top of the grid
    width = len(grid[0])
    empty_row = ["." for _ in range(width)]
    grid = [empty_row, empty_row, empty_row] + grid
    if block == "-":
        xs = [2, 3, 4, 5]
        ys = [0, 0, 0, 0]
    elif block == "+":
        xs = [3, 2, 3, 4, 3]
        ys = [2, 1, 1, 1, 0]
    elif block == "L":  # actually _|
        xs = [4, 4, 2, 3, 4]
        ys = [2, 1, 0, 0, 0]
    elif block == "I":
        xs = [2, 2, 2, 2]
        ys = [3, 2, 1, 0]
    elif block == "O":
        xs = [2, 3, 2, 3]
        ys = [1, 1, 0, 0]

    return [x for x in xs], [y + min_y for y in ys]


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
    row = ["." for _ in range(width)]
    grid = [row]
    min_y = 0
    dir_idx = 0
    for block_n in tqdm(range(nblocks), ascii=".#", desc="Dropping blocks"):
        block = block_order[block_n % len(block_order)]
        # to do: put three empty rows at the top of the grid
        xs, ys = get_startpos(block, grid, min_y)
        # to do: place the block in the grid

        # everything below is unfinished

        print(grid)
        for row in grid:
            print("".join(row))
        input()

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
