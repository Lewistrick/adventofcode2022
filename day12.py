# Day: 2022-12-12

from collections import defaultdict
from helpers import DIRS4, read_grid
import numpy as np
import matplotlib.pyplot as plt
from loguru import logger
import sys

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

    expand = defaultdict(set)  # for each distance, the positions to expand from
    expand[0].add(finish)

    while expand:
        # get the smallest distance and remove it from the expand dict
        dist = min(expand.keys())
        positions = expand.pop(dist)

        # for each position, expand to all neighbours
        for xold, yold in positions:
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

                expand[dist + 1].add((xnew, ynew))
                seen.add((xnew, ynew))
                distgrid[ynew][xnew] = dist + 1

    return distgrid, seen


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

distgrid, tiles_seen = get_dist_grid(intgrid, endpos)

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

# find the distances to all of these positions
lowpos_values = [distgrid[y][x] for y, x in lowpos]
lowpos_values_filter = [v for v in lowpos_values if v > 0]
print(f"Part 2: {min(lowpos_values_filter)}")
