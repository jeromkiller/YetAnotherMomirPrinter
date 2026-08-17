from . import MtgCard
import requests
import time
from PIL import Image, ImageFile
from . import exceptions

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


class searchParams():
    def __init__(self, mana: int = 0, legalities: list[str] = list(), mtg_sets: list[str] = list()) -> None:
        self.mana_value: int = mana
        self.legalities: list[str] = legalities
        self.mtg_sets: list[str] = mtg_sets
        self.ignore_list: set[str] = set()
        self.static_params: list[str] = ["type:creature", "game:paper", "lang:en","-frame:fandfc", ]
    
    def get_params(self, mana: int | None = None) -> str:
        if mana is not None:
            self.mana_value = mana
        params = list[str]()
        params.append("mv:" + str(self.mana_value))
        if self.mtg_sets:
            set_params = ["set:" + s for s in self.mtg_sets]
            params.append(f"({" or ".join(set_params)})")
        if self.legalities:
            legality_params = ["legality:" + s for s in self.legalities]
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
    try:
        card = MtgCard.MagicCard(card_json)
        if card_json.get("layout", "") == "meld":
            result_uri: str | None = None
            for part in card_json.get("all_parts", []):
                if part.get("component", "") == "meld_result":
                    result_uri = part["uri"]
            assert result_uri
            card_json = fetchObject(result_uri, "")
            card.addSecondFace(card_json)
    except exceptions.CardNotCreatureException as e:
        print(e)
        search_params.ignore_list.add(e.oracle_id)
        # try again
        return fetchCard(uri, params + "-oracle_id:" + e.oracle_id, visited)
    
    if card.front_face.image_url:
        card.setImage(fetchArt(card.front_face.image_url))
    if card.back_face and card.back_face.image_url:
        card.setImage2(fetchArt(card.back_face.image_url))
    #card.extras = fetchExtras(card_json, visited)
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
    return fetchCard(api_path, params, set())

def fetchNamedCard(name: str) -> MtgCard.MagicCard:
    print(f"fetching card with name: {name}")
    path = "https://api.scryfall.com/cards/named"
    return fetchCard(f"{path}?exact={name}", "", set())


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
        token_data = fetch(token_uri, "",visited)
        if token_data is None:
            continue
        if token_data.status_code != 200:
            continue

        token = MtgCard.MagicCard(token_data.json())
        if token.image_url:
            token.setImage(fetchArt(token.image_url))
        if token.image_url_2:
            token.setImage2(fetchArt(token.image_url_2))
        extras.append(token)
    return extras
