# Day: 2022-12-13

from pathlib import Path

# type hints for nested lists of ints
IntOrList = int | list[int]
NestedIntList = IntOrList | list[IntOrList]

pairs = Path("day13.txt").read_text().split("\n\n")
pairs = [pair.split("\n") for pair in pairs]
pairs: list[tuple[NestedIntList]] = [(eval(pair[0]), eval(pair[1])) for pair in pairs]


class Element:
    __slots__ = ("val",)

    def __init__(self, val):
        self.val: NestedIntList = val

    def __le__(self, other) -> bool:
        if isinstance(self.val, int) and isinstance(other.val, int):
            return self.val <= other.val
        elif isinstance(self.val, int) and isinstance(other.val, list):
            newself = Element([self.val])
            return newself <= other
        elif isinstance(self.val, list) and isinstance(other.val, int):
            newother = Element([other.val])
            return self <= newother
        else:  # both are lists
            for left, right in zip(self.val, other.val):
                left_el = Element(left)
                right_el = Element(right)
                if left_el < right_el:
                    return True
                elif left_el > right_el:
                    return False

            # if we get here, all elements up to here are equal
            # so the shorter list is the smaller one
            return len(self.val) <= len(other.val)

    def __lt__(self, other) -> bool:
        if isinstance(self.val, int) and isinstance(other.val, int):
            return self.val < other.val
        elif isinstance(self.val, int) and isinstance(other.val, list):
            newself = Element([self.val])
            return newself < other
        elif isinstance(self.val, list) and isinstance(other.val, int):
            newother = Element([other.val])
            return self < newother
        else:
            for left, right in zip(self.val, other.val):
                left_el = Element(left)
                right_el = Element(right)
                if left_el < right_el:
                    return True
                elif left_el > right_el:
                    return False

        # if we get here, all elements up to here are equal
        # so the shorter list is the smaller one
        return len(self.val) < len(other.val)

    def __gt__(self, other) -> bool:
        if isinstance(self.val, int) and isinstance(other.val, int):
            return self.val > other.val
        elif isinstance(self.val, int) and isinstance(other.val, list):
            newself = Element([self.val])
            return newself > other
        elif isinstance(self.val, list) and isinstance(other.val, int):
            newother = Element([other.val])
            return self > newother
        else:
            for left, right in zip(self.val, other.val):
                left_el = Element(left)
                right_el = Element(right)
                if left_el > right_el:
                    return True
                elif left_el < right_el:
                    return False

        # if we get here, all elements up to here are equal
        # so the shorter list is the smaller one
        return len(self.val) > len(other.val)


n_correct_order = 0

# create divider packets (for part 2)
div2 = Element([[2]])
div6 = Element([[6]])
all_elements: list[Element] = [div2, div6]
for pidx, pair in enumerate(pairs, 1):
    left, right = map(Element, pair)
    all_elements.append(left)
    all_elements.append(right)

    if left <= right:
        n_correct_order += pidx


print(f"Part 1: {n_correct_order}")

# having Element objects that have < and > operators, we can sort them
all_elements.sort()

# find indices of divider packets (1-indexed)
idx2 = all_elements.index(div2) + 1
idx6 = all_elements.index(div6) + 1

print(f"Part 2: {idx2 * idx6}")
