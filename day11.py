# Day: 2022-12-11

import math
import re

from loguru import logger
from pathlib import Path
import sys

Action = tuple[int, int]

# set logger debug level
logger.remove()
logger.add(sink=sys.stdout, level="INFO")

PART2 = True  # if False, calculate part 1


class Monkey:
    def __init__(self, id, items, operation, test, iftrue, iffalse):
        self.id = id
        self.items = list(map(int, items))
        self.operator = operation.split()[-2]
        self.opvalue = operation.split()[-1]
        self.test = test
        self.iftrue = iftrue
        self.iffalse = iffalse
        self.n_inspections = 0

    @classmethod
    def from_lines(cls, lines):
        while not lines[0].strip():
            lines.pop(0)

        id = int(lines[0].strip(":").split()[-1])
        items = re.findall(r"(\d+)", lines[1])
        operation = lines[2].split(":")[1].strip()
        test = int(lines[3].split()[-1])
        iftrue = int(lines[4].split()[-1].strip())
        iffalse = int(lines[5].split()[-1].strip())
        return cls(id, items, operation, test, iftrue, iffalse)

    def do_actions(self) -> list[Action]:
        logger.debug(f"Monkey {self.id}: {self.items}")
        actions = []  # contains (item, target) tuples
        self.n_inspections += len(self.items)
        while self.items:
            value = self.items.pop(0)
            logger.debug(f"Inspecting item with worry level {value}")
            opvalue = value if self.opvalue == "old" else int(self.opvalue)

            before = value
            # do the operation
            if self.operator == "+":
                value += opvalue
            elif self.operator == "*":
                value *= opvalue
            logger.debug(f"- {before} {self.operator} {opvalue} = {value}")

            # monkey gets bored, divide by 3
            if not PART2:
                value = int(value / 3)
            else:
                value %= self.lcm_allmonkeys
            logger.debug(f"- Monkey gets bored. New value: {value}")

            # test if it's divisible by test
            if value % self.test == 0:
                target = self.iftrue
                logger.debug(f"- {value} is divisible by {self.test}.")
            else:
                target = self.iffalse
                logger.debug(f"- {value} is not divisible by {self.test}.")

            logger.debug(f"- Item with value {value} is thrown to monkey {target}")

            actions.append((value, target))
        return actions


monkeys = {}
for text in Path("day11.txt").read_text().split("\n\n"):
    monkey = Monkey.from_lines(text.splitlines())
    monkeys[monkey.id] = monkey

# calculate LCM of all test values
# so the worry levels won't get out of hand
test_values = [monkey.test for monkey in monkeys.values()]
lcm = test_values[0]
for test in test_values[1:]:
    lcm = lcm * test // math.gcd(lcm, test)
logger.info(f"LCM of all test values ({test_values}): {lcm}")

for monkey in monkeys.values():
    monkey.lcm_allmonkeys = lcm

n_rounds = 20 if not PART2 else 10000
for roundno in range(1, n_rounds + 1):
    for id, monkey in monkeys.items():
        actions = monkey.do_actions()
        for value, target in actions:
            monkeys[target].items.append(value)

    if roundno % 1000 == 0 or roundno in (1, 20):
        logger.info(f"After round {roundno}:")
        for id, monkey in monkeys.items():
            logger.info(f"Monkey {id}: {monkey.n_inspections}, {monkey.items}")

ns = [monkey.n_inspections for monkey in monkeys.values()]
n_inspections = sorted(ns)
monkey_business = n_inspections[-1] * n_inspections[-2]
part = 2 if PART2 else 1
logger.info(f"Part {part}: {monkey_business}")
