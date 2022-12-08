# This was a pain to solve on mobile repl.it.
# After around line 20 I had to wait 2-3s for every character I typed.

grid = []
with open("day08.txt") as lines:
    for line in lines:
        grid.append(list(line.strip()))


def is_visible(grid, y, x):
    val = grid[y][x]
    # Check if the tree is visible from the top, bottom, left or right
    return (
        all(grid[i][x] < val for i in range(y))
        or all(grid[i][x] < val for i in range(y + 1, len(grid)))
        or all(grid[y][j] < val for j in range(x))
        or all(grid[y][j] < val for j in range(x + 1, len(grid[0])))
    )


visible = [[True for _ in range(len(grid))] for _ in range(len(grid[0]))]
for y in range(1, len(grid) - 1):
    for x in range(1, len(grid[0]) - 1):
        visible[y][x] = is_visible(grid, y, x)

part1 = sum(sum(row) for row in visible)
print(part1)

part2 = 0
for y in range(len(grid)):
    for x in range(len(grid[y])):
        t = grid[y][x]
        # Create a list of lists of all the trees in the 4 directions
        dirs = [
            grid[y][:x][::-1],
            grid[y][x + 1 :],
            [grid[i][x] for i in range(y)][::-1],
            [grid[i][x] for i in range(y + 1, len(grid))],
        ]
        subscore = 1
        for d in dirs:
            s = 1
            for s, val in enumerate(d, 1):
                if val >= t:
                    break
            subscore *= s
        part2 = max(part2, subscore)

print(part2)
