from helpers import read_splitlines

xh, yh = 0, 0
xt, yt = 0, 0
seen = {(xt, yt)}

lines = read_splitlines("day09.txt")

dirs9 = [
    (0, 0),
    (0, 1),
    (1, 0),
    (0, -1),
    (-1, 0),
    (1, 1),
    (1, -1),
    (-1, 1),
    (-1, -1),
]

knots = [(xt, yt) for _ in range(9)]  # not representing H in this list
seen_lastknot = {knots[-1]}

for line in lines:
    dir, amount = line
    amount = int(amount)

    for _ in range(amount):
        # move H
        if dir == "U":
            yh -= 1
        elif dir == "D":
            yh += 1
        elif dir == "L":
            xh -= 1
        elif dir == "R":
            xh += 1

        # if T and H touch, don't let T move
        for dx, dy in dirs9:
            if (xt + dx, yt + dy) == (xh, yh):
                break
        else:
            # move T towards H
            if xh > xt:
                xt += 1
            elif xh < xt:
                xt -= 1

            if yh > yt:
                yt += 1
            elif yh < yt:
                yt -= 1

        currknot = (xh, yh)  # head
        for kidx, knot in enumerate(knots):
            for dx, dy in dirs9:
                if (knot[0] + dx, knot[1] + dy) == currknot:
                    break
            else:
                # move knot towards currknot
                if currknot[0] > knot[0]:
                    knot = (knot[0] + 1, knot[1])
                elif currknot[0] < knot[0]:
                    knot = (knot[0] - 1, knot[1])

                if currknot[1] > knot[1]:
                    knot = (knot[0], knot[1] + 1)
                elif currknot[1] < knot[1]:
                    knot = (knot[0], knot[1] - 1)

            knots[kidx] = knot

            currknot = knot

        seen_lastknot.add(currknot)  # part 2
        seen.add((xt, yt))  # part 1

part1 = len(seen)
print(part1)
part2 = len(seen_lastknot)
print(part2)
