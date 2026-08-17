import argparse
import pathlib
from typing import TypeAlias
import requests

uri = "http://127.0.0.1:5000/print/named/"

DecklistLine: TypeAlias = tuple[int, str]
Board: TypeAlias = list[DecklistLine]

def parse_decklist(path: pathlib.Path) -> tuple[Board, Board]:
    mainboard: Board = Board()
    sideboard: Board = Board()
    fill_sideboard = False
    with open(path) as deck_file:
        for line in deck_file:
            parts = line.split(" ", 1)
            if len(parts) != 2:
                fill_sideboard = True
                continue

            data = (int(parts[0]), parts[1].strip())
            
            if fill_sideboard:
                sideboard.append(data)
            else:
                mainboard.append(data)
    return (mainboard, sideboard)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        prog="Yet another Momir Printer",
        description="A tool print randomized magic cards"
    )
    parser.add_argument("-f", "--file", type=pathlib.Path, help="Decklist file")
    args = parser.parse_args()

    mainboard, sideboard = parse_decklist(args.file)

    for line in list(mainboard + sideboard):
        amount = line[0]
        name = line[1]
        response = requests.post(uri + name, params={"count": amount})
        if response.status_code > 204:
            print("something happened")
            exit()
            
