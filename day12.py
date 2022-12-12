# Day: 2022-12-12

from helpers import DIRS4, read_grid
import numpy as np
import matplotlib.pyplot as plt
from loguru import logger
import sys

logger.remove()
logger.add(sys.stdout, level="DEBUG")

Position = tuple[int, int]
Grid = list[list[int]]


def get_dist_grid(
    grid: Grid,
    finish: Position,
    seen: set[Position] | None = None,
):
    """Fill a grid with shortest distances to the finish.

    Args:
        grid (list[list[int]]): The grid (height map) to search in.
        finish (tuple[int, int]): The ending position.
        seen (set[tuple[int, int]], optional): The positions visted. Defaults to None.
    """
    if seen is None:
        seen = set()

    # create a zeroes grid to fill with distances
    distgrid = np.zeros((len(grid), len(grid[0])), dtype=int)

    xfin, yfin = finish
    distgrid[yfin][xfin] = 0  # the finish is 0 steps away from itself
    seen.add(finish)

    expand = set()
    expand.add(finish)

    while expand:
        currx, curry = expand.pop()
        logger.debug(f"Expanding from ({currx}, {curry})")
        currval = grid[curry][currx]
        for dx, dy in DIRS4:
            x, y = currx + dx, curry + dy
            if (x, y) in seen:
                continue
            # newval should be currval-1 or currval
            newval = grid[y][x]
            if newval == currval - 1 or newval == currval:
                logger.debug(f"Adding ({x}, {y}) to seen")
                distgrid[y][x] = distgrid[curry][currx] + 1
                seen.add((x, y))
                expand.add((x, y))

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
            currow.append(26)
        else:
            # it's a lowercase letter
            currow.append(ord(c) - ord("a"))
    intgrid.append(currow)
    currow = []

distgrid = get_dist_grid(intgrid, endpos)

# plot grid as image
plt.imshow(distgrid, cmap="hot", interpolation="nearest")
plt.show()
