from PIL import Image, ImageFont, ImageDraw, ImageText, ImageOps
from src.Printer import PainterBase

# receipt width is 512px
# magic card 53mm wide and 88mm tall 
# printing the card sideways will make our canvas 308x512px, this can actually be a little wider if we want to
width = 380     # Soft cap, can be grown or shrunk slightly to make the width fit better in a sleeve
height = 512    # hard cap for my brand of printer
im = Image.new("1", (width, height), color=1)

# let's try turning this into an animate GIF

#def easeOutSine(t):
#    import math
#    return math.sin(t * math.pi / 2)
#
#imlist = list[Image.Image]()
#duration = 25
#for frame in range(duration):
##for x in range(400, 150, -10):
#    painter = PainterBase.PainterBase((width, height))
#    x = 380
#    ease = easeOutSine(frame/duration)
#    ease_offset = ease * 230
#    x -= ease_offset
#    x2 = x + 30
#    
#    blocker1 = (x, 25, x2, 100)
#    painter.draw.rectangle(blocker1)
#    painter.obscured_areas.append(blocker1)
#    painter._paintWrappedText((0, 0), "Long piece of text that may or may not fit on here. Thus it should probably get wrapped around any obstructions it might encounter", 20, None)
#    imlist.append(painter.canvas)
#
#for frame in range(duration):
#    painter = PainterBase.PainterBase((width, height))
#    x = 380
#    ease = easeOutSine(frame/duration)
#    ease_offset = ease * 260
#    x -= ease_offset
#    x2 = x + 180
#    blocker1 = (150, 25, 180, 100)
#    blocker2 = (x, 80, x2, 180)
#    painter.draw.rectangle(blocker1)
#    painter.draw.rectangle(blocker2)
#    painter.obscured_areas.append(blocker1)
#    painter.obscured_areas.append(blocker2)
#    painter._paintWrappedText((0, 0), "Long piece of text that may or may not fit on here. Thus it should probably get wrapped around any obstructions it might encounter", 20, None)
#    imlist.append(painter.canvas)
#
#duration = 15
#for frame in range(duration):
#    painter = PainterBase.PainterBase((width, height))
#    y = 520
#    ease = easeOutSine(frame/duration)
#    ease_offset = ease * 350
#    y -= ease_offset
#
#    blocker1 = (150, 25, 180, 100)
#    blocker2 = (120, 80, 300, 180)
#    blocker3 = (5, y, 300, 520)
#    painter.draw.rectangle(blocker1)
#    painter.draw.rectangle(blocker2)
#    painter.draw.rectangle(blocker3)
#    painter.obscured_areas.append(blocker1)
#    painter.obscured_areas.append(blocker2)
#    painter.obscured_areas.append(blocker3)
#    painter._paintWrappedText((0, 0), "Long piece of text that may or may not fit on here. Thus it should probably get wrapped around any obstructions it might encounter", 20, None)
#    imlist.append(painter.canvas)
#
#for y in range(10):
#    painter = PainterBase.PainterBase((width, height))
#    blocker1 = (150, 25, 180, 100)
#    blocker2 = (120, 80, 300, 180)
#    blocker3 = (5, 170, 300, 500)
#    painter.draw.rectangle(blocker1)
#    painter.draw.rectangle(blocker2)
#    painter.draw.rectangle(blocker3)
#    painter.obscured_areas.append(blocker1)
#    painter.obscured_areas.append(blocker2)
#    painter.obscured_areas.append(blocker3)
#    painter._paintWrappedText((0, 0), "Long piece of text that may or may not fit on here. Thus it should probably get wrapped around any obstructions it might encounter", 20, None)
#    imlist.append(painter.canvas)
#
#duration = 25
#for frame in range(duration):
#    painter = PainterBase.PainterBase((width, height))
#    x = 120
#    x2 = 150
#    ease = easeOutSine(frame * 3/duration)
#    ease_offset = ease * 30
#    x -= ease_offset
#    x2 -= ease_offset
#    blocker1 = (x2, 25, x2 + 30, 100)
#    blocker2 = (x, 80, x + 180, 180)
#    blocker3 = (5, 170, 300, 500)
#    painter.draw.rectangle(blocker1)
#    painter.draw.rectangle(blocker2)
#    painter.draw.rectangle(blocker3)
#    painter.obscured_areas.append(blocker1)
#    painter.obscured_areas.append(blocker2)
#    painter.obscured_areas.append(blocker3)
#    painter._paintWrappedText((0, 0), "Long piece of text that may or may not fit on here. Thus it should probably get wrapped around any obstructions it might encounter", 20, None)
#    imlist.append(painter.canvas)

#res = list(map(lambda im: im.convert("L"), imlist))
#res[0].save("textTest.gif", "GIF", save_all=True, append_images=res, duration=60, loop=0, optimize=False, transparency=1)
#blocker1 = (150, 25, 180, 100)
#blocker2 = (100, 80, 280, 180)
#blocker3 = (5, 170, 300, 500)
#painter.draw.rectangle(blocker3)
#painter.obscured_areas.append(blocker3)
#painter._paintText((0, 0), "Long piece of text that may or may not fit on here. Thus it should probably get wrapped around any obstructions it might encounter", 20, None)
#painter.draw.text((0, 0), ImageText.Text("Long piece of text that may or may not fit on here"))

#painter.canvas.save("textTest.png", "PNG")
# now the real test begins
from src.Printer import BitmapPrinter
from src.MomirVig.GetRandomCard import *
bmpp = BitmapPrinter.BitmapPrinter((width, height))
#card = fetchCard("https://api.scryfall.com/cards/19529b2f-03f0-469d-92d4-e2a2a933d5dc", "", set())
##card.face.oracle[0] = "`Pursuant to subsection 3.1(4) of Richard's Rules of Order, at the beginning of the upkeep of each participant in this game of the Magic: The Gathering® trading card game (hereafter known as \"PLAYER\"), that PLAYER performs all actions in the sequence of previously added actions (hereafter known as \"ACTION QUEUE\"), in the order those actions were added, then adds another action to the end of the ACTION QUEUE. All actions must be simple physical or verbal actions that a player can perform while sitting in a chair, without jeopardizing the health and security of said PLAYER.\nWhen any PLAYER does not perform all the prescribed actions in the correct order, sacrifice this enchantment and said PLAYER discards their complement of cards in hand (hereafter known as \"HAND\").`"
#im = bmpp.paint_card(card)
#im.save("standardTest.png", "PNG")

# normal:   19529b2f-03f0-469d-92d4-e2a2a933d5dc
# split:    73636ca0-2309-4bb3-9300-8bd0c0bb5b31
# leveler:  8b76ba96-9630-44fb-849e-3c3848c03876
# saga_1:   47c8262c-e0c6-4c1a-b1c1-3b5fe5252a9c
# saga_2:   5e14692f-f1c3-4d7f-8baf-3248621e36fb
# read_ahead_saga: 49aa8d4c-04e9-4f38-9786-2c9ad735dd72
# saga_creature: 95318d85-4a08-47ac-a43d-ea83c0bea81c
card2 = fetchCard("https://api.scryfall.com/cards/95318d85-4a08-47ac-a43d-ea83c0bea81c", "", set())
im2 = bmpp.paint_card(card2)
im2.save("standardTest.png", "PNG")
im = im2

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

    #im = im2
    #im = im.convert("L")
    #im = ImageOps.invert(im)
    #im = im.convert("1")
    #im = im.rotate(90, expand=True)
    #printer._reset()
    #printer.buffered_image(im)
    #printer.cut()

