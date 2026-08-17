from flask import Flask, request, abort
from escpos import printer
from src.MomirVig import exceptions
from src.MomirVig.GetRandomCard import *
from src.Printer.BitmapPrinter import BitmapPrinter


width = 380     # Soft cap, can be grown or shrunk slightly to make the width fit better in a sleeve
height = 512    # hard cap for my brand of printer

vid = 0x04b8
pid = 0x0e02

app = Flask("YetAnotherMomirPrintServer")
cardBuilder = BitmapPrinter((width, height))
pos = printer.Usb(vid, pid)

@app.route("/print/named/<name>", methods=['POST'])
def print_named_card(name: str):
    if not name:
        abort(400)

    count: int = int(request.args.get("count", 1))
    if count <= 0:
        abort(400)
    try:
        card = fetchNamedCard(name)
        image = cardBuilder.paint_card(card)
        image = image.rotate(90, expand=True)
        for _ in range(count):
            pos.image(image)
            pos.cut()
    except:
        abort(500)

    return "", 204

@app.route("/print/random/<int:cmc>", methods=['POST'])
def print_random_card(cmc: int | None = None):
    if not cmc:
        abort(400)

    try:
        card = fetchRandomCard(cmc)
        image = cardBuilder.paint_card(card)
        image = image.rotate(90, expand=True)
        pos.image(image)
        pos.cut()
    except:
        abort(500)

    return "", 204

@app.route("/status")
def get_status():
    if not pos.is_online():
        return {"online": False, "paper": "unknown"}
    
    statuses = ["No Paper", "Ending", "Plenty"]
    paper_status: int = pos.paper_status()
    if paper_status >= len(statuses):
        abort(500)

    return {"online": True, "paper": statuses[paper_status]}

