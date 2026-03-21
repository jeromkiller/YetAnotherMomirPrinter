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

def fetch(uri: str, visited: set[str]):
    # limit rate ourselves to 10 fetches per second
    time_stamp = time.time()
    time_delta = time_stamp - lastFetchTimestamp
    if time_delta < 0.1:
        time.sleep(0.1 - time_delta)

    if uri in visited:
        return None
    
    print(f"fetched: {uri}")
    visited.add(uri)
    return requests.get(uri, headers=headers)


def fetchCard(uri: str, visited: set[str] = set()) -> MtgCard.MagicCard:
    response = fetch(uri, visited)
    assert response

    if response.status_code != 200:
        print(f"something went wrong: {response.status_code}")
        exit()

    print(f"fetched: {response.json().get("scryfall_uri", "")}")
    card_json = response.json()
    card = MtgCard.MagicCard(card_json)
    card.setImage(fetchArt(card.face.image_url))
    card.extras = fetchExtras(card_json, visited)

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

def fetchExtras(card_json, visited: set[str]) -> list[MtgCard.MagicCard]:
    extras = list[MtgCard.MagicCard]()
    for part in card_json.get("all_parts", {}):
        if part["component"] != "token":
            continue

        token_uri = part["uri"]
        token_data = fetch(token_uri, visited)
        if token_data is None:
            continue
        if token_data.status_code != 200:
            continue

        token = MtgCard.MagicCard(token_data.json())
        token.setImage(fetchArt(token.face.image_url))
        extras.append(token)
    return extras
