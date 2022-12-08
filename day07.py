# Day: 2022-12-07

from helpers import readlines
from loguru import logger


class Directory:
    def __init__(self, name):
        self.name = name
        self.size = 0
        self.parent = None
        self.files = []
        self.subdirs = {}  # name -> Directory

    def add_subdir(self, name):
        # logger.debug(f"adding subdir {name} to {self.name}")
        subdir = Directory(name)
        subdir.parent = current_dir
        current_dir.subdirs[name] = subdir
        # logger.debug(f"subdirs of {self.name}:")
        # for subdir in self.subdirs.values():
        # logger.debug(f"- {subdir.name}")

    def increase_size(self, size):
        # logger.debug(f"- old size of {self.name}: {self.size}, adding {size}")
        self.size += size
        # logger.debug(f"- new size of {self.name}: {self.size}")
        if self.parent:
            self.parent.increase_size(size)

    def find_small_subdirs(self, maxsize=100000):
        smallsubdirs = set()
        for subdir in self.subdirs.values():
            if subdir.size <= maxsize:
                smallsubdirs.add(subdir)
            smallsubdirs |= subdir.find_small_subdirs(maxsize)
        return smallsubdirs

    def find_dir_sizes(self) -> dict[str, int]:
        sizes = {self.name: self.size}
        for subdir in self.subdirs.values():
            sizes.update(subdir.find_dir_sizes())
        return sizes


lines = list(readlines("day07.txt"))
lines.pop(0)

current_dir = Directory("/")  # line 1

list_mode = False
for i, line in enumerate(lines):
    if line.startswith("$"):
        command = line[2:]
        if command.startswith("cd"):
            dirname = command[3:].strip()
            if dirname == "..":
                # logger.debug("going up")
                current_dir = current_dir.parent
            elif dirname in current_dir.subdirs:
                # logger.debug(f"going into {dirname}")
                current_dir = current_dir.subdirs[dirname]
        elif command == "ls":
            # logger.debug("listing")
            list_mode = True
        else:
            raise ValueError("Unknown command: " + command)
    elif list_mode:
        sizeordir, name = line.split()
        if sizeordir == "dir":
            # logger.debug(f"adding subdir {name}")
            current_dir.add_subdir(name)
            # current_dir = current_dir.subdirs[name]
        elif sizeordir.isdigit():
            size = int(sizeordir)
            # logger.debug(f"adding file {name} {size=}")
            current_dir.increase_size(size)
            current_dir.files.append(name)
        else:
            raise ValueError("Wrong line (1): " + line)

        if i == len(lines) - 1 or lines[i + 1].startswith("$"):
            list_mode = False
    else:
        raise ValueError("Wrong line (2): " + line)

# go to parent
while current_dir.parent:
    current_dir = current_dir.parent

# find all subdirs with size <= 100000
smalldirs = current_dir.find_small_subdirs()

# total size of all small subdirs
part1 = sum([d.size for d in smalldirs])
print(part1)

# find the space to free up
total_space = 70000000
needed = 30000000
unused = total_space - current_dir.size  # we're still in the root dir
to_free = needed - unused
sizes = current_dir.find_dir_sizes()

for dirname, dirsize in sorted(sizes.items(), key=lambda x: x[1]):
    if dirsize >= to_free:
        part2 = dirsize

print(part2)
