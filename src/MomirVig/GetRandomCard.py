from . import MtgCard
import requests
import time
from PIL import Image, ImageFile
from . import exceptions
import random

# edge cases:
# - 0 cost cards with the creature filter includes lands that transform into creatures
#   removing filtering out lands will also remove the dryad arbour
#   Asmoranomardicadaistinaculdacar may be included in the 0 cost cards dispite her only be castable through an alternate cost
# - some transforming cards with non-creature fronts and creature backs are included
#   frame:fandfc can be filtered out for

api_path = "https://api.scryfall.com/cards/random" # mana value 1 for test
headers = {"User-Agent": "YetAnotherMomirPrinter/0.1",
           "Accept": "*/*"}    

# rate limit ourselves to 2 fetches per second
delay = 0.5
global lastFetchTimestamp
lastFetchTimestamp = time.time()


card_not_found_messages: list[str] = list()
with open("404Messages.txt") as messages:
    for line in messages.readlines():
        card_not_found_messages.append(line)

def getCardNotFoundMessage(cmc: int):
    random_line = random.choice(card_not_found_messages)
    random_line.replace("[x]", str(cmc))
    return random_line

class searchParams():
    def __init__(self, mana: int = 0, legalities: list[str] = list(), mtg_sets: list[str] = list()) -> None:
        self.mana_value: int = mana
        self.legalities: list[str] = legalities
        self.mtg_sets: list[str] = mtg_sets
        self.ignore_list: set[str] = set()
        self.static_params: list[str] = ["type:creature", "game:paper", "lang:en","-frame:fandfc", "not:meld_result", "-t:battle", "not:funny"]
    
    def get_params(self, mana: int | None = None) -> str:
        if mana is not None:
            self.mana_value = mana
        params = list[str]()
        params.append("mv:" + str(self.mana_value))
        if self.mtg_sets:
            set_params = ["set:" + s for s in self.mtg_sets]
            params.append(f"({" or ".join(set_params)})")
        if self.legalities:
            legality_params = ["legal:" + s for s in self.legalities]
            params.append(f"({" or ".join(legality_params)})")
        if self.ignore_list:
            ignore_params = ["-oracle_id:" + oid for oid in self.ignore_list]
            params.extend(ignore_params)
        params.extend(self.static_params)

        output = "+".join(params)
        return output

search_params = searchParams(legalities = ["modern"])

def fetch(uri: str, params: str, visited: set[str]):
    # rate limit ourselves to 2 fetches per second
    global lastFetchTimestamp
    time_stamp = time.time()
    time_delta = time_stamp - lastFetchTimestamp
    if time_delta < delay:
        time.sleep(delay - time_delta)

    if uri in visited:
        return None
    
    if params:
        uri += "?q=" + params
    print(f"fetched: {uri}")
    visited.add(uri)
    response = requests.get(uri, headers=headers)
    lastFetchTimestamp = time.time()
    return response


def fetchCard(uri: str, params: str, visited: set[str]) -> MtgCard.MagicCard:
    card_json = fetchObject(uri, params, visited)

    card = MtgCard.MagicCard(card_json)
    if card_json.get("layout", "") == "meld":
        result_uri: str | None = None
        for part in card_json.get("all_parts", []):
            if part.get("component", "") == "meld_result":
                result_uri = part["uri"]
        assert result_uri
        card_json = fetchObject(result_uri, "", set())
        card.addSecondFace(card_json)
    
    
    if card.front_face.image_url:
        card.setImage(fetchArt(card.front_face.image_url))
    if card.back_face and card.back_face.image_url:
        card.setImage2(fetchArt(card.back_face.image_url))
    card.extras = fetchExtras(card_json, visited)
    return card

def fetchObject(uri: str, params: str, visited: set[str]):
    response = fetch(uri, params, visited)
    assert response is not None

    if response.status_code == 404:
        raise exceptions.CardNotFoundException()
    elif response.status_code == 503:
        raise exceptions.UnhandledStatusCodeException(response.reason, response.status_code)
    elif response.status_code != 200:
        raise exceptions.UnhandledStatusCodeException(response.json().get("details", "Unknown"), response.status_code)

    print(f"Got card: {response.json().get("scryfall_uri", "")}")
    return response.json()

def fetchRandomCard(cost: int) -> MtgCard.MagicCard:
    print(f"Getting random card with cost {cost}")
    params = search_params.get_params(mana=cost)
    visited: set[str] = set()
    card = fetchCard(api_path, params, visited)
    while "Creature" not in card.front_face.type:
        # this card isn't a creature on its front side, try again
        print("Error, random card is not a creature on its front face")
        search_params.ignore_list.add(card.front_face.oracle_id)
        params = search_params.get_params(mana=cost)
        card = fetchCard(api_path, params, visited)
    return card


def fetchNamedCard(name: str) -> MtgCard.MagicCard:
    print(f"fetching card with name: {name}")
    path = "https://api.scryfall.com/cards/named"
    return fetchCard(f"{path}?exact={name}", "", set())

def fetchCardByOracleId(oracle_id: str) -> MtgCard.MagicCard:
    print(f"fetching card with oracle id: {oracle_id}")
    # use the random endpoint to return the first result
    path = "https://api.scryfall.com/cards/random"
    return fetchCard(f"{path}?q=oracle_id:{oracle_id}", "", set())

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
        token_data = fetch(token_uri, "", visited)
        if token_data is None:
            continue
        if token_data.status_code != 200:
            continue

        token = MtgCard.MagicCard(token_data.json())
        if token.front_face.image_url:
            token.setImage(fetchArt(token.front_face.image_url))
        if token.back_face and token.back_face.image_url:
            token.setImage2(fetchArt(token.back_face.image_url))
        extras.append(token)
    return extras
