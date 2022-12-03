from helpers import readlines


def letterval(letter):
    return ord(letter) - 38 if letter.isupper() else ord(letter) - 96


lines = list(readlines("day03.txt"))

part1 = 0
for line in lines:
    left, right = line[: len(line) // 2], line[len(line) // 2 :]
    overlap = set(left) & set(right)
    common = overlap.pop()  # there is always exactly one
    part1 += letterval(common)

part2 = 0
for line1, line2, line3 in zip(lines[::3], lines[1::3], lines[2::3]):
    overlap = set(line1) & set(line2) & set(line3)
    common = overlap.pop()  # there is always exactly one
    part2 += letterval(common)


print(part1)
print(part2)
