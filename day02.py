wins = {"A": "Y", "B": "Z", "C": "X"}
draws = {"A": "X", "B": "Y", "C": "Z"}
losses = {"A": "Z", "B": "X", "C": "Y"}
shape_points = {"A": 1, "B": 2, "C": 3, "X": 1, "Y": 2, "Z": 3}
outcome_points = {"Z": 6, "Y": 3, "X": 0}  # Z=win, Y=draw, X=loss

with open("day02.txt") as lines:
    part1 = 0
    part2 = 0
    for line in lines:
        elf, response = line.strip().split()

        if response == wins[elf]:
            part1 += outcome_points["Z"]
        elif response == draws[elf]:
            part1 += outcome_points["Y"]
        part1 += shape_points[response]

        part2 += outcome_points[response]
        outcome_dict = {"X": losses, "Y": draws, "Z": wins}[response]
        part2 += shape_points[outcome_dict[elf]]


print(part1)  # 8392
print(part2)  # 10116
