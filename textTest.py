from PIL import Image, ImageFont, ImageDraw, ImageText, ImageOps
from src.Printer import PainterBase

# receipt width is 512px
# magic card 53mm wide and 88mm tall 
# printing the card sideways will make our canvas 308x512px, this can actually be a little wider if we want to
width = 380     # Soft cap, can be grown or shrunk slightly to make the width fit better in a sleeve
height = 512    # hard cap for my brand of printer
im = Image.new("1", (width, height), color=1)

painter = PainterBase.PainterBase((width, height))
blocker = (150, 25, 180, 100)
painter.draw.rectangle(blocker)
painter.obscured_areas.append(blocker)
blocker = (100, 80, 280, 180)
painter.draw.rectangle(blocker)
painter.obscured_areas.append(blocker)
painter._paintText((0, 0), "Long piece of text that may or may not fit on here. Thus it should probably get wrapped around any obstructions it might encounter", 20, None)
#painter.draw.text((0, 0), ImageText.Text("Long piece of text that may or may not fit on here"))

painter.canvas.save("textTest.png", "PNG")
# now the real test begins
#from src.Printer import BitmapPrinter
#from src.MomirVig.GetRandomCard import *
#bmpp = BitmapPrinter.BitmapPrinter((width, height))
#card = fetchCard("https://api.scryfall.com/cards/19529b2f-03f0-469d-92d4-e2a2a933d5dc", "", set())
##card.face.oracle[0] = "`Pursuant to subsection 3.1(4) of Richard's Rules of Order, at the beginning of the upkeep of each participant in this game of the Magic: The Gathering® trading card game (hereafter known as \"PLAYER\"), that PLAYER performs all actions in the sequence of previously added actions (hereafter known as \"ACTION QUEUE\"), in the order those actions were added, then adds another action to the end of the ACTION QUEUE. All actions must be simple physical or verbal actions that a player can perform while sitting in a chair, without jeopardizing the health and security of said PLAYER.\nWhen any PLAYER does not perform all the prescribed actions in the correct order, sacrifice this enchantment and said PLAYER discards their complement of cards in hand (hereafter known as \"HAND\").`"
#im = bmpp.paint_card(card)
#im.save("standardTest.png", "PNG")
#
#card2 = fetchCard("https://api.scryfall.com/cards/33a8e5b9-6bfb-4ff2-a16d-3168a5412807", "", set())
#im2 = bmpp.paint_card(card2)
#im2.save("standardTest.png", "PNG")

if False:
    from src.Printer import UsbPrinter
    im = im.convert("L")
    im = ImageOps.invert(im)
    im = im.convert("1")
    im = im.rotate(90, expand=True)
    printer = UsbPrinter.UsbPrinter()
    printer._reset()
    printer.buffered_image(im)
    printer.cut()

    im = im2
    im = im.convert("L")
    im = ImageOps.invert(im)
    im = im.convert("1")
    im = im.rotate(90, expand=True)
    printer._reset()
    printer.buffered_image(im)
    printer.cut()

