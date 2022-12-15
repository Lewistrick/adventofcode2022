# Day: 2022-12-15

from loguru import logger
from helpers import readlines
import re
from tqdm import tqdm

USE_EXAMPLE = False

file = "day15.txt" if not USE_EXAMPLE else "day15_example.txt"

sensors = []
beacons = []
distances = []
for line in readlines(file):
    sx, sy, bx, by = map(int, re.findall(r"(\-?\d+)", line))
    sensors.append((sx, sy))
    beacons.append((bx, by))
    distances.append(abs(sx - bx) + abs(sy - by))


def find_distress_beacon(sensors, beacons, distances, target_y):
    x_ranges = []
    for (sx, sy), (bx, by), dist in zip(sensors, beacons, distances):
        # Part 1
        dist_tgt = abs(sy - target_y)
        if dist_tgt > dist:
            continue

        # find the range of x values that are within the distance to the target
        rest_dist = dist - dist_tgt
        newrange = (sx - rest_dist, sx + rest_dist)

        if newrange[0] == newrange[1] == bx:
            continue

        if by == target_y:
            if newrange[0] == bx:
                newrange = (bx + 1, newrange[1])
            elif newrange[1] == bx:
                newrange = (newrange[0], bx - 1)

        if newrange[0] > newrange[1]:
            continue

        x_ranges.append(newrange)

    x_ranges.sort()

    # merge overlapping ranges
    merged = []
    for x1, x2 in x_ranges:
        if not merged or merged[-1][1] < x1 - 1:
            merged.append((x1, x2))
        else:
            merged[-1] = (merged[-1][0], max(merged[-1][1], x2))

    return merged


# part 1
target_y = 2000000 if not USE_EXAMPLE else 10
merged = find_distress_beacon(sensors, beacons, distances, target_y)
part1 = 0
for x1, x2 in merged:
    rlen = x2 - x1 + 1
    part1 += rlen

logger.success(f"Part 1: {part1}")  # 4725496

lim_low = 0
lim_high = 4000000 if not USE_EXAMPLE else 20
x_multiplier = 4000000
for target_y in tqdm(range(lim_low, lim_high), ascii=".#", desc="Checking y_tgt"):
    merged = find_distress_beacon(sensors, beacons, distances, target_y)
    # limit the merged ranges between lim_low and lim_high
    new_merged = []
    for x1, x2 in merged:
        if x1 > lim_high:
            continue
        if x2 < lim_low:
            continue
        new_merged.append((max(x1, lim_low), min(x2, lim_high)))

    if len(new_merged) == 1:
        x1, x2 = new_merged[0]
        if x1 == lim_low and x2 == lim_high:
            continue
        else:
            logger.warning("Should not happen 1")
            breakpoint()
    elif len(new_merged) > 2:
        logger.warning("Should not happen 2")
        breakpoint()
    else:
        (x1, x2), (x3, x4) = new_merged
        if x3 == x2 + 2:
            part2_x = x2 + 1
            part2_y = target_y
            part2 = part2_x * x_multiplier + part2_y

            if (part2_x, part2_y) in beacons:
                continue

            logger.success(f"Part 2: {part2}")  # 12051287042458
            break
        else:
            logger.warning("Should not happen 3")
            breakpoint()
