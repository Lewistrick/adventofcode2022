import matplotlib.pyplot as plt
import networkx as nx
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
        # logger.debug(f"Created valve {name} ({pressure=}, {tunnels=}")
        return cls(name, pressure, tunnels)


def is_dead_end(source: str, target: str, valves: dict[str, Valve], opened: set[str]):
    """Check if the path from source to target is a dead end.

    A dead end is a path that only contains open valves and ends in a valve that has
    no tunnels except the source.
    """
    while True:
        # get target tunnels
        target_tunnels = [t for t in valves[target].tunnels if t != source]

        # if this valve has more than one tunnel, it's not a dead end
        if len(target_tunnels) > 1:
            return False

        if not target_tunnels:
            if valves[target].pressure == 0:
                return True
            elif target in opened:
                return True
            return False

        # go to next valve
        source = target
        target = target_tunnels[0]


valves: dict[str, Valve] = {}
for line in readlines("day16_example.txt"):
    valve = Valve.from_string(line)
    valves[valve.name] = valve

# create graph
graph = nx.DiGraph()
for valve in valves.values():
    for tunnel in valve.tunnels:
        graph.add_edge(valve.name, tunnel)

# set node sizes
max_pressure = max(valve.pressure for valve in valves.values())
node_hues = [valve.pressure / max_pressure for valve in valves.values()]
node_colors = plt.cm.Reds(node_hues)

# draw graph interactively (using matplotlib)
pos = nx.spring_layout(graph)
nx.draw(graph, with_labels=True, pos=pos, node_color=node_colors)
plt.show()
