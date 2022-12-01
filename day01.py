sums = []
curr_sum = 0
with open("day01.txt") as lines:
    for line in lines:
        if not line.strip():
            sums.append(curr_sum)
            curr_sum = 0
            continue
        curr_sum += int(line)
    sums.append(curr_sum)

sums = sorted(sums)
print(sums)
print("part 1:", sums[-1])
print("part 2:", sum(sums[-3:]))
