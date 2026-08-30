from flask import Flask, request, abort
from escpos import printer
from src.MomirVig import exceptions
from src.MomirVig.GetRandomCard import *
from src.Printer.BitmapPrinter import BitmapPrinter
import NetworkSetup


width = 380     # Soft cap, can be grown or shrunk slightly to make the width fit better in a sleeve
height = 512    # hard cap for my brand of printer

vid = 0x04b8
pid = 0x0e02

app = Flask("YetAnotherMomirPrintServer")
cardBuilder = BitmapPrinter((width, height))
pos = printer.Usb(vid, pid)

def error_message(message: str):
    return {"message": message}

def card_to_response(card: MtgCard.MagicCard) -> dict:
    card_response = {
        "name": card.front_face.name,
        "oracle_id": card.front_face.oracle_id
    }
    extras: list[dict] = list()
    for extra in card.extras:
        name = extra.front_face.name
        type = extra.front_face.type
        stats = extra.front_face.stats

        if type:
            extra_name = type
        else:
            extra_name = name
        if stats:
            extra_name += " " + stats

        extra_card = {
            "name": name,
            "type": type,
            "stats": stats,
            "extra_name": extra_name,
            "oracle_id": extra.front_face.oracle_id
        }

        extras.append(extra_card)

    return {"card": card_response, "extras": extras}

@app.route("/api/print/named/<name>", methods=['POST'])
def print_named_card(name: str):
    if not name:
        abort(400, error_message("Can't print a card without knowing it's name"))

    count: int = int(request.args.get("count", 1))
    if count <= 0:
        abort(400, error_message("Can't print a negative amount of cards"))
    try:
        card = fetchNamedCard(name)
        image = cardBuilder.paint_card(card)
        image = image.rotate(90, expand=True)
        for _ in range(count):
            pos.image(image)
            pos.cut()
    except Exception as e:
        return abort(500, error_message("Internal Server Error: " + str(e)))

    return card_to_response(card), 200

@app.route("/api/print/random/<int:cmc>", methods=['POST'])
def print_random_card(cmc: int | None = None):
    if cmc is None or cmc < 0 or cmc > 20:
        abort(400, error_message("CMC must be between 0 and 20"))

    try:
        card = fetchRandomCard(cmc)
        image = cardBuilder.paint_card(card)
        image = image.rotate(90, expand=True)
        pos.image(image)
        pos.cut()
    except exceptions.CardNotFoundException:
        errorLine = getCardNotFoundMessage(cmc)
        pos.text(errorLine)
        pos.cut()
        return error_message(f"No applicable creature found for {cmc} mana"), 404
    except Exception as e:
        print(e.with_traceback)
        abort(500, error_message("Internal Server Error: " + str(e)))

    return card_to_response(card), 200

@app.route("/api/print/oid/<oracle_id>", methods=['POST'])
def print_card_by_id(oracle_id: str):
    if not oracle_id:
        abort(400, error_message("Oracle id cannot be empty"))

    try:
        card = fetchCardByOracleId(oracle_id)
        image = cardBuilder.paint_card(card)
        image = image.rotate(90, expand=True)
        pos.image(image)
        pos.cut()
    except Exception as e:
        abort(500, error_message("Internal Server Error: " + str(e)))

    return card_to_response(card) , 200

@app.route("/api/status")
def get_status():
    if not pos.is_online():
        return {"online": False, "paper": "unknown"}
    
    statuses = ["No Paper", "Ending", "Plenty"]
    paper_status: int = pos.paper_status()
    if paper_status >= len(statuses):
        abort(500)

    return {"online": True, "paper": statuses[paper_status]}



@app.route("/settings/ssids")
def get_available_ssids():
    connected_ssid = NetworkSetup.getConnectedSSID()
    local_nonconnected_ssids = NetworkSetup.getUnconnectedSSIDs()
    return {
        "connected_to": connected_ssid,
        "available": local_nonconnected_ssids
        }, 200

@app.route("/settings/changeNetwork", methods=['POST'])
def change_ssid():   # todo settings to body
    json = request.get_json()
    ssid = json.get("ssid", "")
    passwd = json.get("password", "")
    hidden = json.get("hidden", "") == "true"

    if not ssid:
        abort(400, error_message("SSID cannot be empty"))

    NetworkSetup.changeNetwork(ssid, passwd, hidden)
    return "", 204
