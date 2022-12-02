with open("day02.txt") as lines:
    part1 = 0
    part2 = 0
    for line in lines:
        elf, response = line.strip().split()
        draw1 = (
            (elf == "A" and response == "X")
            or (elf == "B" and response == "Y")
            or (elf == "C" and response == "Z")
        )
        win1 = (
            (elf == "A" and response == "Y")
            or (elf == "B" and response == "Z")
            or (elf == "C" and response == "X")
        )
        score1 = 3 * draw1 + 6 * win1
        if response == "X":
            score1 += 1
        elif response == "Y":
            score1 += 2
        elif response == "Z":
            score1 += 3
        part1 += score1

        score2 = 0
        if response == "X":  # lose
            if elf == "A":  # rock
                score2 += 3  # play scissors
            elif elf == "B":  # paper
                score2 += 1  # play rock
            elif elf == "C":  # scissors
                score2 += 2  # play paper
        elif response == "Y":  # draw
            score2 += 3
            if elf == "A":  # rock
                score2 += 1  # play rock
            elif elf == "B":  # paper
                score2 += 2  # play paper
            elif elf == "C":  # scissors
                score2 += 3  # play scissors
        elif response == "Z":  # win
            score2 += 6
            if elf == "A":  # rock
                score2 += 2  # play paper
            elif elf == "B":  # paper
                score2 += 3  # play scissors
            elif elf == "C":  # scissors
                score2 += 1  # play rock
        part2 += score2


print(part1)
print(part2)
