import helpers

lines = helpers.readlines("day05.txt")
stacks = [[] for _ in range(9)]
for line in lines:
    if line.strip().startswith("1"):
        break

    # read in groups of 4 characters
    for i in range(0, len(line), 4):
        stack = line[i : i + 4]
        # if the 2nd character is a letter, add it to the stack
        if stack[1].isalpha():
            stacks[i // 4].append(stack[1])

next(lines)  # empty line

# read the rest of the input
for line in lines:
    n_move, s_from, s_to = map(int, line.split()[1::2])
    s_from, s_to = s_from - 1, s_to - 1  # fix index
    to_move, stacks[s_from] = stacks[s_from][:n_move], stacks[s_from][n_move:]

    # The line below is the difference between part 1 and 2.
    # For part 2, it should be commented out.
    # to_move.reverse()

    stacks[s_to] = to_move + stacks[s_to]

print("".join(stack[0] for stack in stacks))
