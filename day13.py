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
        """Compare self <= other."""
        if isinstance(self.val, int) and isinstance(other.val, int):
            return self.val <= other.val
        elif isinstance(self.val, int) and isinstance(other.val, list):
            newself = Element([self.val])
            return newself <= other
        elif isinstance(self.val, list) and isinstance(other.val, int):
            newother = Element([other.val])
            return self <= newother
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
            return len(self.val) <= len(other.val)

    def __lt__(self, other) -> bool:
        """Compare self < other.

        (self < other) means that !(other <= self) so we can reuse the __le__ operator.
        """
        return not other <= self

    def __gt__(self, other) -> bool:
        """Compare self > other.

        (self > other) means that !(self <= other) so we can reuse the __le__ operator.
        """
        return not self <= other

    def __ge__(self, other) -> bool:
        """Compare self >= other.

        (self >= other) means that (other <= self) so we can reuse the __le__ operator.
        """
        return other <= self


n_correct_order = 0

# create divider packets (for part 2)
all_elements: list[Element] = []
for pidx, pair in enumerate(pairs, 1):
    left, right = map(Element, pair)
    all_elements.append(left)
    all_elements.append(right)

    if left <= right:
        n_correct_order += pidx


print(f"Part 1: {n_correct_order}")

# For part 2, we don't need to sort the elements. We just need to know how many
# elements are smaller than the dividers.
div2 = Element([[2]])
div6 = Element([[6]])
idx2 = sum(1 for el in all_elements if el < div2) + 1 # +1 for 1-based indexing
idx6 = sum(1 for el in all_elements if el < div6) + 2 # +1 extra for div2

print(f"Part 2: {idx2 * idx6}")
