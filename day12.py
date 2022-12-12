# Day: 2022-12-12

import sys

import matplotlib.pyplot as plt
import numpy as np
from loguru import logger

from helpers import DIRS4, read_grid

logger.remove()
logger.add(sys.stdout, level="DEBUG")

Position = tuple[int, int]
Grid = list[list[int]]

PLOT = False


def get_dist_grid(
    grid: Grid,
    finish: Position,
    seen: set[Position] | None = None,
):
    """Fill a grid with shortest distances to the finish.

    Args:
        grid (list[list[int]]): The grid (height map) to search in.
        finish (tuple[int, int]): The target position.
        seen (set[tuple[int, int]], optional): The positions visted. Defaults to None.
    """
    if seen is None:
        seen = set()

    # create a zeroes grid to fill with distances
    distgrid = np.zeros((len(grid), len(grid[0])), dtype=int)

    x0, y0 = finish
    seen.add(finish)

    expand = [finish]

    while expand:
        xold, yold = expand.pop(0)
        # get the distance from the finish
        dist = distgrid[yold][xold]

        # for each position, expand to all neighbours
        for dx, dy in DIRS4:
            xnew, ynew = xold + dx, yold + dy
            if (xnew, ynew) in seen:
                continue
            if not (0 <= xnew < len(grid[0]) and 0 <= ynew < len(grid)):
                continue

            highval = grid[yold][xold]
            lowval = grid[ynew][xnew]

            # highval can be at most 1 higher than lowval
            if highval > lowval + 1:
                continue

            expand.append((xnew, ynew))
            seen.add((xnew, ynew))
            distgrid[ynew][xnew] = dist + 1

    return distgrid


startpos = None
endpos = None
strgrid = read_grid("day12.txt")

intgrid = []
currow = []
for y, row in enumerate(strgrid):
    for x, c in enumerate(row):
        if c == "S":
            startpos = (x, y)
            currow.append(0)
        elif c == "E":
            endpos = (x, y)
            currow.append(25)
        else:
            # we know that it's a lowercase letter so we can convert it to an int
            currow.append(ord(c) - ord("a"))
    intgrid.append(currow)
    currow = []

distgrid = get_dist_grid(intgrid, endpos)

if PLOT:
    # plot grid as image
    plt.imshow(distgrid, cmap="hot", interpolation="nearest")

    # show the letters on the grid
    for y, row in enumerate(strgrid):
        for x, c in enumerate(row):
            plt.text(x, y, c, color="blue", ha="center", va="center")

    plt.show()

part1 = distgrid[startpos[1]][startpos[0]]
print(f"Part 1: {part1}")

# find all positions with 'a'
lowpos = np.argwhere(np.array(strgrid) == "a")

# find the distances to all of these positions (if they are reachable)
lowpos_values = [distgrid[y][x] for y, x in lowpos if distgrid[y][x] > 0]
print(f"Part 2: {min(lowpos_values)}")
