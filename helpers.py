"""Helpers for AoC 2022.

When run from the command line, it opens the puzzle and the input file for the current
day in a Chrome tab. Make sure you're logged in to AoC first.
"""

BROWSER = '"C:\\Program Files (x86)\\Google\\Chrome\\Application\\chrome.exe"'

from pathlib import Path
import subprocess
import datetime


def readlines(file):
    for line in Path(file).read_text().splitlines():
        yield line.rstrip()


def read_intlines(file):
    for line in readlines(file):
        yield int(line)


def read_splitlines(file, sep=None):
    for line in readlines(file):
        yield line.split(sep)


if __name__ == "__main__":
    # find today's monthday number
    today = datetime.date.today()

    if today.month != 12:
        print("It's not December yet!")
        exit(1)

    baseurl = f"https://adventofcode.com/{today.year}/day/{today.day}"
    # open the puzzle and the input in Chrome tabs (don't wait until they're closed)
    subprocess.Popen(f"{BROWSER} {baseurl}")
    subprocess.Popen(f"{BROWSER} {baseurl}/input")

    # create the file and the input file if they don't exist
    fn = f"day{today.day:02d}.py"
    if not Path(fn).exists():
        with open(fn, "w") as f:
            f.write(f"# Day: {today}\n")
            f.write("\n")
            f.write("from helpers import readlines\n")
            f.write("\n")
            f.write(f"for line in readlines('day{today.day:02d}.txt'):\n")
            f.write("    pass\n")
    fn_input = f"day{today.day:02d}.txt"
    if not Path(fn_input).exists():
        Path(fn_input).touch()

    # open the file in VS Code
    subprocess.Popen(f"code {fn}")

    # open the input file in VS Code
    subprocess.Popen(f"code {fn_input}")

    # create a git branch for the day
    subprocess.Popen(f"git checkout -b day{today.day:02d}")
