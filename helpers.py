from pathlib import Path


def readlines(file):
    for line in Path(file).read_text().splitlines():
        yield line.split()


def read_intlines(file):
    for line in readlines(file):
        yield int(line)


def read_splitlines(file, sep=None):
    for line in readlines(file):
        yield line.split(sep)
