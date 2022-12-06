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
