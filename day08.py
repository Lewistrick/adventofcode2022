"""This was a pain to solve on mobile repl.it. Won't do that again soon.

After line ~20 I had to wait 2-3s for every character I typed.
Luckily, I only made 2 minor bugs in part 2.
"""

# Read the input, save it as a 2D matrix.
# Only realized later that this saves the numbers as strings, but that doesn't matter
# because comparisons work correctly as long as the numbers are of length 1.
grid = []
with open("day08.txt") as lines:
    for line in lines:
        grid.append(list(line.strip()))


def is_visible(grid, y, x):
    """Check if the tree is visible from the edges"""
    val = grid[y][x]
    return (
        all(grid[i][x] < val for i in range(y))  # from top
        or all(grid[i][x] < val for i in range(y + 1, len(grid)))  # from bottom
        or all(grid[y][j] < val for j in range(x))  # from left
        or all(grid[y][j] < val for j in range(x + 1, len(grid[0])))  # from right
    )


# Create a bool-matrix of the same size as the grid, indicating for each tree whether
# it's visible from at least one edge. We start with an all-True matrix.
visible = [[True for _ in range(len(grid))] for _ in range(len(grid[0]))]
# We don't have to check the edges, because they're always visible.
for y in range(1, len(grid) - 1):
    for x in range(1, len(grid[0]) - 1):
        visible[y][x] = is_visible(grid, y, x)

# Count the visible trees
part1 = sum(sum(row) for row in visible)
print(part1)

part2 = 0
for y in range(len(grid)):
    for x in range(len(grid[y])):
        treeval = grid[y][x]
        # Create a list of lists of all the trees in the 4 directions
        dirs = [
            grid[y][:x][::-1],
            grid[y][x + 1 :],
            [grid[i][x] for i in range(y)][::-1],
            [grid[i][x] for i in range(y + 1, len(grid))],
        ]

        # Subscore keeps track of the product of the number of trees in each direction
        subscore = 1
        for dir in dirs:
            # We need to initialize dirscore, because if dir is empty, we don't enter
            # the loop
            dirscore = 1
            # Enumerating the list from 1 counts the first tree as seen.
            for dirscore, val in enumerate(dir, 1):
                if val >= treeval:
                    break
            subscore *= dirscore

        # Update the global score
        part2 = max(part2, subscore)

print(part2)
