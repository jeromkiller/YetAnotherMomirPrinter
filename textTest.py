from PIL import Image, ImageFont, ImageDraw, ImageText, ImageOps

# receipt width is 512px
# magic card 53mm wide and 88mm tall 
# printing the card sideways will make our canvas 308x512px, this can actually be a little wider if we want to
width = 380     # Soft cap, can be grown or shrunk slightly to make the width fit better in a sleeve
height = 512    # hard cap for my brand of printer
im = Image.new("1", (width, height), color=1)

d = ImageDraw.Draw(im)
#t = "{2}: This creature gains your choice of banding, bushido 1, double strike, fear, flying, first strike, haste, landwalk of your choice, protection from a color of your choice, provoke, rampage 1, shadow, or trample until end of turn.\n{2}: This creature becomes the colors of your choice until end of turn.\n{2}: This creature becomes the creature type of your choice until end of turn.\n{2}: This creature's expansion symbol becomes the symbol of your choice until end of turn.\n{2}: This creature's art becomes by the artist of your choice until end of turn.\n{2}: This creature gets +2/-2 or -2/+2 until end of turn.\n{2}: Untap this creature."
t = "{2}: This creature gains your choice of banding other longer text"

#font = ImageFont.truetype("Font/Swansea-q3pd.ttf", size=20)
font = ImageFont.truetype("Font/SwanseaBold-D0ox.ttf", size=20)
text = ImageText.Text(t, mode="1", font=font)
i = 0
extra = text.wrap(width, height=20)
d.text((0,0), text)
d.text((0, 20), text)

print(text.get_bbox())

d.line([(0,0), (width - 1, 0), (width -1, height -1), (0, height-1), (0,0)])


# now the real test begins
from src.Printer import BitmapPrinter
from src.MomirVig.GetRandomCard import *
bmpp = BitmapPrinter.BitmapPrinter((width, height))
card = fetchCard("https://api.scryfall.com/cards/19529b2f-03f0-469d-92d4-e2a2a933d5dc", "", set())
#card.face.oracle[0] = "`Pursuant to subsection 3.1(4) of Richard's Rules of Order, at the beginning of the upkeep of each participant in this game of the Magic: The Gathering® trading card game (hereafter known as \"PLAYER\"), that PLAYER performs all actions in the sequence of previously added actions (hereafter known as \"ACTION QUEUE\"), in the order those actions were added, then adds another action to the end of the ACTION QUEUE. All actions must be simple physical or verbal actions that a player can perform while sitting in a chair, without jeopardizing the health and security of said PLAYER.\nWhen any PLAYER does not perform all the prescribed actions in the correct order, sacrifice this enchantment and said PLAYER discards their complement of cards in hand (hereafter known as \"HAND\").`"
im = bmpp.paint_card(card)
im.save("standardTest.png", "PNG")

card2 = fetchCard("https://api.scryfall.com/cards/33a8e5b9-6bfb-4ff2-a16d-3168a5412807", "", set())
im2 = bmpp.paint_card(card2)
im2.save("standardTest.png", "PNG")

if True:
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

