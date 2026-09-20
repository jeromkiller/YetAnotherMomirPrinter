from . import MtgCard
import requests
import time
from PIL import Image, ImageFile
from . import exceptions
import random
from enum import Enum, Flag, auto

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
global randomized_message_bag
randomized_message_bag: list[str] = list()

with open("404Messages.txt") as messages:
    for line in messages.readlines():
        card_not_found_messages.append(line)

def getCardNotFoundMessage(cmc: int):
    global randomized_message_bag
    if not randomized_message_bag:
        randomized_message_bag = list(card_not_found_messages)
        random.shuffle(randomized_message_bag)

    random_line = randomized_message_bag.pop(0)
    random_line = random_line.replace("[x]", str(cmc))
    return random_line

class CardTypes(Flag):
    @staticmethod
    def try_create(values: str | list[str]) -> CardTypes:
        if isinstance(values, str):
            values = values.lower()
            return CardTypes[values]

        card_types = CardTypes(0)
        for value in values:
            value = value.lower()
            card_types |= CardTypes[value]
        return card_types
    
    @staticmethod
    def create(values: str | list[str]) -> CardTypes:
        if isinstance(values, str):
            values = values.lower()
            return CardTypes[values]
    
        card_types = CardTypes(0)
        for value in values:
            value = value.lower()
            try:
                card_type = CardTypes[value]
                card_types |= card_type
            except KeyError:
                continue
        return card_types

    creature = auto()
    planeswalker = auto()
    artifact = auto()
    enchantment = auto()
    battle = auto()

class Formats(Enum):
    @staticmethod
    def try_create(value: str) -> Formats:
        return Formats[value.lower()]

    all = auto()
    standard = auto()
    modern = auto()
    legacy = auto()
    pauper = auto()

class searchParams():
    def __init__(self, mana: int = 1, legality: Formats = Formats.all, mtg_sets: list[str] = list(), card_types: CardTypes = CardTypes.creature) -> None:
        self.mana_value: int = mana
        self.legality: Formats = legality
        self.mtg_sets: list[str] = [s.lower() for s in mtg_sets]
        self.types: CardTypes = card_types
        self.ignore_list: set[str] = set()
        self.static_params: list[str] = ["game:paper", "lang:en", "not:meld_result", "not:funny"]

    def verify(self) -> tuple[bool, str]:
        reasons: list[str] = list()
        valid: bool = True

        if self.mana_value >= 0:
            valid = False
            reasons.append("Mana Value can't be below zero")
        if self.mana_value <= 20:
            valid = False
            reasons.append("Mana Value can't higher then twenty")

        reason: str = "All good!"
        if not valid:
            reason = ", ".join(reasons) + "."

        return valid, reason
    
    def get_params(self, mana: int | None = None) -> str:
        if mana is not None:
            self.mana_value = mana
        params = list[str]()
        params.append("mv:" + str(self.mana_value))
        if self.mtg_sets:
            set_params = ["set:" + s for s in self.mtg_sets]
            params.append(f"({" or ".join(set_params)})")
        if self.legality is not Formats.all:
            legality_params = ["legal:" + s for s in self.legality.name]
            params.append(f"({" or ".join(legality_params)})")
        if self.ignore_list:
            ignore_params = ["-oracle_id:" + oid for oid in self.ignore_list]
            params.extend(ignore_params)
        if self.types:
            type_params = ["t:" + str(t.name) for t in self.types]
            params.append(f"({" or ".join(type_params)})")
        if CardTypes.battle not in self.types:
            params.append("-t:battle")
        if CardTypes.enchantment not in self.types:
            params.append("-frame:fandfc")
        params.extend(self.static_params)

        output = "+".join(params)
        return output

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

def fetchRandomCard(search_params: searchParams = searchParams()) -> MtgCard.MagicCard:
    print(f"Getting random card with cost {search_params.mana_value}")
    params = search_params.get_params()
    visited: set[str] = set()

    while True:
        card = fetchCard(api_path, params, visited)

        typeline = card.front_face.type.lower()
        card_types = CardTypes.create(list(typeline.split(" ")))

        if card_types & search_params.types:
            break

        # this card isn't a creature on its front side, try again
        print("Error, random card does not match any of the requested types on its front face")
        search_params.ignore_list.add(card.front_face.oracle_id)
        params = search_params.get_params()
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
