from helpers import readlines

lines = readlines("day04.txt")

cratelines = []
for line in lines:
    if not line.strip():
        break
    cratelines.append(line)

# the last line should be removed
counts = cratelines.pop()
ncrates = int(counts.strip()[-1])

stacks = [[] for _ in range(ncrates)]
for line in cratelines:
    # read line per 4 characters
    for i in range(0, len(line), 4):
        crate = line[i : i + 4]
        if crate == "    ":  # empty crate
            continue
        letter = crate[1]
        # prepend the letter on the crate
        stacks[i // 4].append(letter)

# invert the stacks
for stack in stacks:
    stack.reverse()

# for i, stack in enumerate(stacks, 1):
#     print(i, "".join(stack))
# print()

# read the remaining lines
for line in lines:
    words = line.split()
    n, src, tgt = map(int, words[1::2])
    # move n crates from src to tgt
    # print(line)
    stacks[src - 1], move = stacks[src - 1][:-n], stacks[src - 1][-n:]

    # comment this line for part 2
    # move.reverse()

    # print(f"Moving {move} from {src} to {tgt}")
    stacks[tgt - 1].extend(move)

    # for i, stack in enumerate(stacks, 1):
    #     print(i, "".join(stack))
    # print()

tops = [stack[-1] for stack in stacks]
print("".join(tops))
