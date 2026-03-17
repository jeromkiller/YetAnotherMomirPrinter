from . import MtgCard
from . import ProcessImage
import requests
import time
import matplotlib.image as img
from PIL import Image, ImageFile

# edge cases:
# - 0 cost cards with the creture filter includes lands that transform into creatures
#   removing filtering out lands will also remove the dryad arbour
#   Asmoranomardicadaistinaculdacar may be included in the 0 cost cards dispite her only be castable through an alternate cost
# - some transforming cards with non-creature fronts and creature backs are included
#   frame:fandfc can be filtered out for

momir_path = "https://api.scryfall.com/cards/random?q=type:creature+mv:" # mana value 1 for test
headers = {"User-Agent": "MomirTest/0.1",
           "Accept": "*/*"}    

lastFetchTimestamp = 0.0

def fetchCard(uri: str) -> MtgCard.MagicCard:
    # limit rate ourselves to 10 fetches per second
    time_stamp = time.time()
    time_delta = time_stamp - lastFetchTimestamp
    if time_delta < 0.1:
        time.sleep(0.1 - time_delta)

    response = requests.get(uri, headers=headers)
    if response.status_code != 200:
        print(f"something went wrong: {response.status_code}")
        exit()

    card_json = response.json()
    print(f"fetched: {response.json().get("scryfall_uri", "")}")
    card = MtgCard.MagicCard(card_json)
    card.setImage(fetchArt(card.face.image_url))
    for part in card_json.get("all_parts", {}):
        if part["component"] == "token":
            token_uri = part["uri"]
            if token_uri == uri:
                continue
            card.addExtraCard(fetchCard(part["uri"]))

    return card

def fetchRandomCard(cost: int) -> MtgCard.MagicCard:
    print(f"Getting random card with cost {cost}")
    return fetchCard(f"{momir_path}{cost}")

def fetchArt(uri: str) -> ImageFile.ImageFile:
    print(f"fetcing art: {uri}")
    response = requests.get(uri, headers=headers, stream=True)
    if response.status_code != 200:
        print(f"something went wrong: {response.status_code}")
        exit()
    return Image.open(response.raw)