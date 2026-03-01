from os import listdir, path
from typing import get_args

from lib.competition import Competition
from lib.topic import ContestLevel

def find_available_years(search_path="data") -> list[int]:
    dirs = [d for d in listdir(search_path) if path.isdir(path.join(search_path, d))]
    years = []
    for d in dirs:
        if d.isdigit():
            years.append(int(d))
    return years

def collect_competitions(year: int, debug=False):
    C = []
    for level in get_args(ContestLevel):
        fp = f"./data/{year}/{level.lower()}.json"
        if path.exists(fp) is False:
            print(f"Unable to find [{fp}] !")
            continue
        print(f"Reading data from {year} {level}...")
        c = Competition.from_file(year, level, fp)
        if debug:
            print(f"{c.year} {c.level}")
            for q in c.questions:
                print(q)
        C.append(c)
    return C