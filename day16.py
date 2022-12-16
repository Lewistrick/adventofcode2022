import itertools
from functools import lru_cache
from queue import PriorityQueue

from loguru import logger

from helpers import readlines


class Valve:
    def __init__(self, name: str, pressure: int, tunnels: list[str]):
        self.name = name
        self.pressure = pressure
        self.tunnels = tunnels
        self.opened = False

    @classmethod
    def from_string(cls, string):
        words = string.split()
        name = words[1]
        pressure = int(words[4].split("=")[1].strip(";"))
        tunnels = {tunnel.strip(",") for tunnel in words[9:]}
        return cls(name, pressure, tunnels)


@lru_cache(maxsize=None)
def is_dead_end(source: str, target: str, opened: tuple[str]):
    """Check if the path from source to target is a dead end.

    A dead end is a path that only contains open valves and ends in a valve that has
    no tunnels except the source.
    """
    # get target tunnels
    targets = {target}
    checked = {source}
    while targets:
        target = targets.pop()
        if target in checked:
            continue
        checked.add(target)

        # if target is not open and has pressure, it's not a dead end
        if target not in opened and valves[target].pressure > 0:
            return False

        for tunnel in valves[target].tunnels:
            t_notopen = tunnel not in opened
            t_pressure = valves[tunnel].pressure > 0
            if t_notopen and t_pressure:
                return False

            if tunnel not in checked:
                targets.add(tunnel)

    return True


valves: dict[str, Valve] = {}
for line in readlines("day16.txt"):
    valve = Valve.from_string(line)
    valves[valve.name] = valve

max_pressure = max(v.pressure for v in valves.values())


# Part 1
# (prio, name, path, opened, sub, total, minute)
# prio: priority of the stack item
# name: name of the valve
# path: list of valves and tunnels we've been through
# opened: set of valves that are opened
# sub: total pressure of opened valves
# total: total amount of pressure released (sum of all opened valves in each minute)
# minute: current minute
#
StackTuple = tuple[float, str, list[str], set[str], int, int, int]
stack: PriorityQueue[StackTuple] = PriorityQueue()
stack.put((0, "AA", ["AA"], set(), 0, 0, 0))

best_solution: int = 0  # highest total release; too low: 1420
best_path = []
best_npaths = 0
n_paths = 0
new_total = 0
correct = 1737
while not stack.empty():
    # queue.get returns the lowest priority item
    prio, name, path, opened, sub, total, minute = stack.get()  # DFS
    valve = valves[name]

    n_paths += 1
    if n_paths <= 1000000 and n_paths % 100000 == 0:
        logger.debug(f"Checked {n_paths} paths, stack size={stack.qsize()}")

    if n_paths >= 1000000:
        logger.debug(f"Checked 1M paths, stack size={stack.qsize()}")
        break

    if minute == 30:
        if new_total > best_solution:
            best_solution = new_total
            best_path = path.copy()
            best_npaths = n_paths
            logger.success(f"Best ({best_solution}): {'-'.join(best_path)}")
        continue

    # release pressure
    new_total = total + sub

    # if all valves are opened, we just stay where we are
    closed_valves = {v for v in valves if valves[v].pressure > 0 and v not in opened}
    if not closed_valves:
        remaining_minutes = 30 - minute
        new_total = total + sub * remaining_minutes
        if new_total > best_solution:
            best_solution = new_total
            best_path = path.copy()
            best_npaths = n_paths
            best_path.append("stay")
            logger.success(f"Best  ({best_solution}): {'-'.join(best_path)}")
        continue

    # possible improvement: if there's one closed valve, find the shortest path to it

    # items with low priority are checked first;
    # comments behind the lines indicate the number of paths to check before finding
    # the best solution for the example input
    # prio = (minute * 100) / (new_total * sub + 1)
    # prio = minute**2.9 / (new_total - sub + 1)  # 24973
    # prio = minute**2.8 / (new_total - sub + 1)  # 13977
    # prio = minute**2.85 / (new_total - sub + 1)  # 10588
    # prio = minute**2.86 / (new_total - sub + 1)  # 10161
    # prio = (minute + 2) ** 3 - (sub - new_total) ** 2  # 34014
    prio = (minute + 2) ** 4 - (sub - new_total) ** 2  # 4603

    # we can either open the valve...
    if name not in opened and valve.pressure > 0:
        # open valve
        new_path = path.copy() + ["open"]  # add "open" to path
        new_open = opened.copy() | {name}  # add valve to opened
        new_sub = sub + valves[name].pressure  # add pressure to sub
        # (name, path, opened, sub, total, minute)
        stack.put((prio, name, new_path, new_open, new_sub, new_total, minute + 1))

        # if the valve has high pressure, don't go through a tunnel
        if valve.pressure > 10:
            continue

    # ...or go through a tunnel
    for tunnel in valve.tunnels:
        # last open index
        loi = 0 if not opened else max(i for i, v in enumerate(path) if v == "open")
        # if we visited this tunnel since the last open, we don't go through it
        if tunnel in path[loi:]:
            continue

        # check if this is a dead end with only open valves
        if is_dead_end(source=name, target=tunnel, opened=tuple(opened)):
            # breakpoint()
            continue

        # if the only tunnel from this valve is the one we came from, and the valve is
        # not open, we don't go back without opening it
        if is_dead_end(tunnel, name, tuple(opened)) and tunnel in opened:
            continue

        new_path = path.copy()
        new_path.append(tunnel)
        new_open = opened.copy()
        # (prio, name, path, opened, sub, total, minute)
        stack.put((prio, tunnel, new_path, new_open, sub, new_total, minute + 1))

logger.info(f"Checked {n_paths} paths")
logger.debug(f"Found after {best_npaths} paths")
# baseline n_paths: 5796256
# after adding closed dead end check: 3969687
# after adding opened dead end check: 3070166
# after adding AA to path: 1177246
# after always opening valve with max pressure: 1153769
# not sure what I did: 207539 (solution found after 108384 paths)
# after adding prio: 207539 (solution found after 79570 paths)
# after optimizing prio: 207539 (solution found after 10161 paths)
# after improving dead end check + prio: 172196 (solution found after 4603 paths)

logger.success(f"Best  ({best_solution}): {'-'.join(best_path)}")
# too low: 1420, 1638
# correct: 1737 (#paths: 207816)

#######################################################################################
# Part 2
# (prio, mypos, elpos, opened, sub, total, timeleft)
# prio: priority of the stack item
# mypos: position of the player
# elpos: position of the elephant
# opened: set of valves that are opened
# sub: total pressure of opened valves
# total: total amount of pressure released (sum of all opened valves in each minute)
# minute: current minute

StackTupleElephant = tuple[float, str, str, set[str], int, int, int]
stack2: PriorityQueue[StackTupleElephant] = PriorityQueue()
stack2.put((0, "AA", "AA", set(), 0, 0, 26))

best_solution2: int = 0
while stack2:
    prio, mypos, elpos, opened, sub, total, timeleft = stack2.get()

    if timeleft == 0:
        if total > best_solution2:
            best_solution2 = total
        continue

    # release pressure
    new_total = total + sub

    # if all valves are opened, we just stay where we are
    closed_valves = {v for v in valves if valves[v].pressure > 0 and v not in opened}
    if not closed_valves:
        new_total = total + sub * timeleft
        if new_total > best_solution2:
            best_solution2 = new_total
        continue

    # possible improvement: if there's one closed valve, find the shortest path to it

    # items with low priority are checked first
    prio = minute - new_total - sub

    # now there are 4 possibilities, opening the valve or walking through a tunnel
    # for the player and the elephant

    # possibility 1: both open a valve
    if (
        (mypos not in opened and valves[mypos].pressure > 0)  # I can open
        and (elpos not in opened and valves[elpos].pressure > 0)  # elephant can open
        and mypos != elpos  # only useful if we're in different positions
    ):
        # open valve
        new_open = opened.copy() | {mypos, elpos}
        new_sub = sub + valves[mypos].pressure + valves[elpos].pressure
        # (prio, mypos, elpos, opened, sub, total, timeleft)
        stack2.put((prio, mypos, elpos, new_open, new_sub, new_total, timeleft - 1))

    # possibility 2+3: one opens a valve, the other walks through a tunnel
    for p1, p2 in zip((mypos, elpos), (elpos, mypos)):
        # p1 opens valve
        new_open = opened.copy() | {p1}
        new_sub = sub + valves[p1].pressure

        # p2 walks through tunnel ## TODO

        # check if this is a dead end with only open valves
        if is_dead_end(source=p2, target=tunnel, opened=tuple(opened)):
            continue
        if is_dead_end(tunnel, p2, tuple(opened)) and tunnel in opened:
            continue

        new_path = path.copy()
        new_path.append(tunnel)
        new_open = opened.copy()
        # (prio, name, path, opened, sub, total, minute)
        stack.put((prio, tunnel, new_path, new_open, sub, new_total, minute + 1))
