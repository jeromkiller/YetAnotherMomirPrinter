from escpos.printer import Usb
from src.MomirVig import exceptions
from src.MomirVig.GetRandomCard import *
from src.Printer.BitmapPrinter import BitmapPrinter
from PIL.Image import Image
import argparse

# receipt width is 512px
# magic card 53mm wide and 88mm tall 
# printing the card sideways will make our canvas 308x512px, this can actually be a little wider if we want to
width = 380     # Soft cap, can be grown or shrunk slightly to make the width fit better in a sleeve
height = 512    # hard cap for my brand of printer
vid = 0x04b8
pid = 0x0e02

def get_momir_card(cmc: int, as_image: bool):
    printer = None
    if not as_image:
        printer = Usb(vid, pid)
        if printer == None:
            print("printer not connected")
            as_image = True

    card = fetchRandomCard(cmc)
    
    images = list[Image]()
    painter = BitmapPrinter((width, height))
    images.append(painter.paint_card(card))

    for extra in card.extras:
        painter = BitmapPrinter((width, height))
        images.append(painter.paint_card(extra))

    
    for i, image in enumerate(images):
        if as_image:
            image.save(f"card_{i}.png", "PNG")
        else:
            if printer == None:
                break
            image = image.rotate(90, expand=True)
            printer.image(image)
            printer.cut()


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        prog="Yet another Momir Printer",
        description="A tool print randomized magic cards"
    )
    parser.add_argument("cmc", type=int, help="Mana cost of the desired card")
    parser.add_argument("-i", "--image", action='store_true', default=False, help="Save the card as an image file")
    args = parser.parse_args()

    get_momir_card(args.cmc, args.image)
