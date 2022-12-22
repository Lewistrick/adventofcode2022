import itertools

from helpers import readlines

DEBUG = False


def show_grid(grid, dir, x, y, comment, nxt):
    print(f"{comment} ({x=} {y=} {dir=}")
    shown_sep = False
    for my, line in enumerate(grid):
        if DEBUG:
            if abs(my - y) > 10:
                if y < 10 and my > len(grid) - 10:
                    pass
                else:
                    if not shown_sep:
                        print("~" * len(line) + "|")
                        shown_sep = True
                    continue

        for mx, ch in enumerate(line):
            if (mx, my) == (x, y):
                match dir:
                    case (1, 0):  # right
                        ch = ">"
                    case (0, 1):  # down
                        ch = "v"
                    case (-1, 0):  # left
                        ch = "<"
                    case (0, -1):  # up
                        ch = "^"
                    case _:
                        raise ValueError(f"Unknown direction: {dir}")
            print(ch, end="")
        print("|")
    if nxt is None:
        print("End of instructions")
    else:
        print(f"Next instruction: {nxt}")
        input("?")


def dir_txt(dx, dy):
    match dx, dy:
        case 1, 0:  # right
            return ">"
        case 0, 1:  # down
            return "v"
        case -1, 0:  # left
            return "<"
        case 0, -1:  # up
            return "^"
        case _:
            raise ValueError(f"Unknown direction: {(dx, dy)}")


def part1(grid, instructions, pos, dir):
    x, y = pos
    dx, dy = dir
    # show_grid(grid, (dx, dy), x, y, f"initial grid", instructions[0])
    for instruction, nxt in zip(instructions, instructions[1:] + [None]):
        match instruction:
            case int():
                # we handle this below, so do nothing here
                pass
            case "L":
                dx, dy = dy, -dx
                # show_grid(grid, (dx, dy), x, y, f"after turning left", nxt)
                continue
            case "R":
                dx, dy = -dy, dx
                # show_grid(grid, (dx, dy), x, y, f"after turning right", nxt)
                continue
            case _:
                raise ValueError(f"Unknown instruction: '{instruction}'")

        # mypy knows that instruction is an int here
        for _ in range(instruction):
            if grid[y][x] != ".":
                raise ValueError(f"Moved to a forbidden spot: ({x}, {y})")

            x += dx
            y += dy

            if dx:  # moving horizontally
                row = grid[y]

                # if we're at the left of the grid, wrap around to the right
                if x < 0 or (dx == -1 and row[x] == " "):
                    # get the last position that has a "." or "#"
                    xpos, val = max(
                        (xpos, val) for xpos, val in enumerate(row) if val != " "
                    )
                    if val == "#":
                        # it's a wall, so we can't move; stop this instruction
                        x -= dx
                        break
                    else:
                        # it's a ".", so move there
                        x = xpos

                # if we're at the right of the grid, wrap around to the left
                elif x >= len(row) or (dx == 1 and row[x] == " "):
                    # get the first position that has a "." or "#"
                    xpos, val = min(
                        (xpos, val) for xpos, val in enumerate(row) if val != " "
                    )
                    if val == "#":
                        # it's a wall, so we can't move; stop this instruction
                        x -= dx
                        break
                    else:
                        # it's a ".", so move there
                        x = xpos

                elif row[x] == "#":
                    # we hit a wall, go back and stop this instruction
                    x -= dx
                    break

                elif row[x] == ".":
                    # it's a ".", so move there
                    continue

            elif dy:  # moving vertically
                col = [line[x] for line in grid]

                # if we're at the top of the grid, wrap around to the bottom
                if y < 0 or (dy == -1 and col[y] == " "):
                    # get the last position that has a "." or "#"
                    ypos, val = max(
                        (ypos, val) for ypos, val in enumerate(col) if val != " "
                    )
                    if val == "#":
                        # it's a wall, so we can't move; stop this instruction
                        y -= dy
                        break
                    else:
                        # it's a ".", so move there
                        y = ypos

                # if we're at the bottom of the grid, wrap around to the top
                elif y >= len(grid) or (dy == 1 and col[y] == " "):
                    # get the first position that has a "." or "#"
                    ypos, val = min(
                        (ypos, val) for ypos, val in enumerate(col) if val != " "
                    )
                    if val == "#":
                        # it's a wall, so we can't move; stop this instruction
                        y -= dy
                        break
                    else:
                        # it's a ".", so move there
                        y = ypos

                elif col[y] == "#":
                    # we hit a wall, go back and stop this instruction
                    y -= dy
                    break

                elif col[y] == ".":
                    # it's a ".", so move there
                    continue

        # show the grid and the current position
        # show_grid(grid, (dx, dy), x, y, f"after {instruction}", nxt)

    match (dx, dy):
        case (1, 0):  # right
            dirnum = 0
        case (0, 1):  # down
            dirnum = 1
        case (-1, 0):  # left
            dirnum = 2
        case (0, -1):  # up
            dirnum = 3
        case _:
            raise ValueError(f"Unknown direction: {(dx, dy)}")

    row = y + 1
    col = x + 1
    # show_grid(grid, (dx, dy), x, y, f"final grid", None)
    print(f"Final position: {row=}, {col=} {dirnum=}")
    password = 1000 * row + 4 * col + dirnum
    return password


def part2(grid, instructions, pos, dir):
    print("-" * 80)
    print("Starting part 2")
    print("-" * 80)

    # find the face on the cube for each position
    faces = assign_faces(grid)

    x, y = pos
    dx, dy = dir
    facechange_checked = set()

    for instruction, nxt in zip(instructions, instructions[1:] + [None]):
        face = faces[(x, y)]
        if DEBUG:
            print(f"{x=} {y=} {face=} {instruction=}")
        match instruction:
            case int():
                # we handle this below, so do nothing here
                pass
            case "L":
                dx, dy = dy, -dx
                # show_grid(grid, (dx, dy), x, y, f"after turning left", nxt)
                continue
            case "R":
                dx, dy = -dy, dx
                # show_grid(grid, (dx, dy), x, y, f"after turning right", nxt)
                continue
            case _:
                raise ValueError(f"Unknown instruction: '{instruction}'")

        for _ in range(instruction):
            currface = faces[(x, y)]
            new_x = x + dx
            new_y = y + dy

            # find the face of the new position
            check_face = faces.get((new_x, new_y))
            if check_face == currface:
                # check if wall
                if grid[new_y][new_x] == "#":
                    break
                x, y = new_x, new_y
                continue

            # if we're here, we're moving to another face (this is the tricky part)
            newface, new_dx, new_dy, new_x, new_y = change_face(
                currface, dx, dy, new_x, new_y
            )

            if DEBUG:
                olddir = dir_txt(dx, dy)
                newdir = dir_txt(new_dx, new_dy)

                if newface != currface:
                    print(
                        f"Moving {olddir} from {currface} to {newface} at {x=}, {y=}"
                        f" {new_x=}, {new_y=} {newdir=}"
                    )
                    if (currface, newface) in facechange_checked:
                        print("Already checked this face change")
                    else:
                        # input("Check this face;Press enter to continue...")
                        facechange_checked.add((currface, newface))

            # if the new position is a wall, don't make the move
            if grid[new_y][new_x] == "#":
                break

            # update the position and direction
            x, y = new_x, new_y
            currface = newface
            dx, dy = new_dx, new_dy

    dirnum = [(1, 0), (0, 1), (-1, 0), (0, -1)].index((dx, dy))
    row = y + 1
    col = x + 1
    # show_grid(grid, (dx, dy), x, y, f"final grid", None)
    print(f"Final position: {row=}, {col=} {dirnum=}")
    password = 1000 * row + 4 * col + dirnum
    return password


def change_face(currface, dx, dy, new_x, new_y):
    """Given that we know that we change faces, find the new position and direction.

    Remember that the cube is laid out like this:

     |A|B
     |C|
    D|E|
    F| |

    Args:
        currface (str): The current face (A-F)
        dx (int): The current horizontal direction (1, 0, -1)
        dy (int): The current vertical direction (1, 0, -1)
        new_x (int): The new horizontal position if we wouldn't fall off a face
        new_y (int): The new vertical position if we wouldn't fall off a face

    Returns:
        tuple: (newface, new_dx, new_dy, new_x, new_y), where:
            newface (str): The new face (A-F)
            new_dx (int): The new horizontal direction (1, 0, -1)
            new_dy (int): The new vertical direction (1, 0, -1)
            new_x (int): The new horizontal position
            new_y (int): The new vertical position
    """
    new_dx, new_dy = dx, dy  # some face changes will change the direction
    match currface, dx, dy:
        case "A", 1, 0:  # right
            newface = "B"
        case "A", 0, 1:  # down
            newface = "C"
        case "A", -1, 0:  # left
            newface = "D"
            # Ay = 0..49, Dx = 149..100 => Dy = 149 - Ay
            new_x, new_y = 0, 149 - new_y
            new_dx, new_dy = 1, 0  # new direction is right
        case "A", 0, -1:  # up
            newface = "F"
            # Ax = 50..99, Fy = 150..199 => Fy = 100 + Ax
            new_x, new_y = 0, 100 + new_x
            new_dx, new_dy = 1, 0  # new direction is right

        case "B", 1, 0:  # right
            newface = "E"
            # By = 0..49, Ey = 149..100 => Ey = 149 - By
            new_x, new_y = 99, 149 - new_y
            new_dx, new_dy = -1, 0  # new direction is left
        case "B", 0, 1:  # down
            newface = "C"
            # Bx = 100..149, Cy = 50..99 => Cy = Bx - 50
            new_x, new_y = 99, new_x - 50
            new_dx, new_dy = -1, 0  # new direction is left
        case "B", -1, 0:  # left
            newface = "A"
        case "B", 0, -1:  # up
            newface = "F"
            # Bx = 100..149, Fx = 0..49 => Fx = Bx - 100
            new_x, new_y = new_x - 100, 199
            new_dx, new_dy = 0, -1  # new direction is up

        case "C", 1, 0:  # right
            newface = "B"
            # before, we saw that Cy = Bx - 50, so Bx = Cy + 50
            new_x, new_y = new_y + 50, 49
            new_dx, new_dy = 0, -1  # new direction is up
        case "C", 0, 1:  # down
            newface = "E"
        case "C", -1, 0:  # left
            newface = "D"
            # Cy = 50..99, Dx = 0..49 => Dx = Cy - 50
            new_x, new_y = new_y - 50, 100
            new_dx, new_dy = 0, 1  # new direction is down
        case "C", 0, -1:  # up
            newface = "A"

        case "D", 1, 0:  # right
            newface = "E"
        case "D", 0, 1:  # down
            newface = "F"
        case "D", -1, 0:  # left
            newface = "A"
            # Dy = 149 - Ay => Ay = 149 - Dy
            new_x, new_y = 50, 149 - new_y
            new_dx, new_dy = 1, 0  # new direction is right
        case "D", 0, -1:  # up
            newface = "C"
            # Dx = Cy - 50 => Cy = Dx + 50
            new_x, new_y = 50, new_x + 50
            new_dx, new_dy = 1, 0  # new direction is right

        case "E", 1, 0:  # right
            newface = "B"
            # Ey = 149 - By => By = 149 - Ey
            new_x, new_y = 149, 149 - new_y
            new_dx, new_dy = -1, 0  # new direction is left
        case "E", 0, 1:  # down
            newface = "F"
            # Ex = 50..99, Fy = 150..199 => Fy = 100 + Ex
            new_x, new_y = 49, 100 + new_x
            new_dx, new_dy = -1, 0  # new direction is left
        case "E", -1, 0:  # left
            newface = "D"
        case "E", 0, -1:  # up
            newface = "C"

        case "F", 1, 0:  # right
            newface = "E"
            # Fy = 100 + Ex => Ex = Fy - 100
            new_x, new_y = new_y - 100, 149
            new_dx, new_dy = 0, -1  # new direction is up
        case "F", 0, 1:  # down
            newface = "B"
            # Fx = Bx - 100 => Bx = Fx + 100
            new_x, new_y = new_x + 100, 0
            new_dx, new_dy = 0, 1  # new direction is down
        case "F", -1, 0:  # left
            newface = "A"
            # Fy = 100 + Ax => Ax = Fy - 100
            new_x, new_y = new_y - 100, 0
            new_dx, new_dy = 0, 1  # new direction is down
        case "F", 0, -1:  # up
            newface = "D"

        case _:
            raise ValueError(f"Unknown face: {currface}")

    return newface, new_dx, new_dy, new_x, new_y


def assign_faces(grid):
    """Assign each position on the grid a face.

    Each face is 50x50 and they're laid out like this:
     |A|B
     |C|
    D|E|
    F| |
    """
    faces = {}
    for (y, x) in itertools.product(range(len(grid)), range(len(grid[0]))):
        if grid[y][x] == " ":
            continue
        match x // 50, y // 50:
            case 1, 0:
                faces[(x, y)] = "A"
            case 2, 0:
                faces[(x, y)] = "B"
            case 1, 1:
                faces[(x, y)] = "C"
            case 0, 2:
                faces[(x, y)] = "D"
            case 1, 2:
                faces[(x, y)] = "E"
            case 0, 3:
                faces[(x, y)] = "F"
            case _:
                raise ValueError(f"Unknown face: {(x, y)}")
    return faces


def main():
    grid = []
    lines = readlines("day22.txt")
    maxlen = 0
    for line in lines:
        if not line:
            break
        grid.append(line)
        maxlen = max(maxlen, len(line))

    grid = [line.ljust(maxlen, " ") for line in grid]

    instruction_line = next(lines)
    instructions = []
    curr_n = 0
    for ch in instruction_line:
        if ch in "LR":
            if curr_n:
                instructions.append(curr_n)
                curr_n = 0
            instructions.append(ch)
        elif ch.isdigit():
            curr_n = curr_n * 10 + int(ch)
    if curr_n:
        instructions.append(curr_n)

    dir = (1, 0)  # (x, y) so this means right
    x, y = grid[0].index("."), 0

    # part 1
    print("Part 1:", part1(grid, instructions, (x, y), dir))
    # 122400 is too low
    # 77318 as well, of course
    # 136082 is too high
    # 136054 is correct

    # part 2
    print("Part 2:", part2(grid, instructions, (x, y), dir))
    # 22543 (row=22, col=135, dirnum=3) is too low
    # 36600 (row=36, col=150, dirnum=0) is too low
    # 122153 (row=122, col=38, dirnum=1) is correct


if __name__ == "__main__":
    main()
