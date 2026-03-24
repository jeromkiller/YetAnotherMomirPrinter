from src.Printer import UsbPrinter, TerminalPrinter
from src.Printer.constants import *
from src.MomirVig import exceptions
from src.MomirVig.GetRandomCard import *
import argparse

if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        prog="Yet another Momir Printer",
        description="A tool print randomized magic cards"
    )
    parser.add_argument("cmc", type=int, help="Mana cost of the desired card")
    parser.add_argument("-t", "--terminal", action='store_true', default=False, help="Print to terminal instead of Printer")
    args = parser.parse_args()
    
    if args.terminal:
        printer = TerminalPrinter.TerminalPrinter()
    else:
        printer = UsbPrinter.UsbPrinter()
        if printer == None:
            print("Printer not connected")
            exit()
    card = fetchRandomCard(args.cmc)
    printer.print_card(card)
    for extra in card.extras:
        printer.print_card(extra)