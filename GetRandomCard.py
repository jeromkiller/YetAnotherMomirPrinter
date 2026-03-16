import requests
import ProcessImage

import matplotlib.image as img
import numpy as np
from PIL import Image

momir_path = "https://api.scryfall.com/cards/random?q=type:creature+mv:" # mana value 1 for test
headers = {"User-Agent": "MomirTest/0.1",
           "Accept": "*/*"}    

# cards with issues:
#   transforming cards, example:
#   - https://scryfall.com/card/vow/101/concealing-curtains-revealing-eye

class CardData:
    def __init__(self, json, skipImage = False):
        self.name = json.get("name", "")
        self.cost = json.get("mana_cost", "")
        self.image_url = json["image_uris"]["art_crop"]
        self.image = np.array([])
        self.type = json.get("type_line", "")
        self.oracle = json.get("oracle_text", "")
        self.power = json.get("power", "")
        self.toughness = json.get("toughness", "")

        if not skipImage:
            self.image = self.get_image()
        
    def get_image(self):
        if self.image.size > 0:
            return self.image

        request = requests.get(self.image_url, headers=headers, stream=True)
        im = np.array(Image.open(request.raw))
        return ProcessImage.DitherImage(im)


def fetchRandomCard(cost: int) -> CardData:
    response = requests.get(f"{momir_path}{cost}", headers=headers)
    if response.status_code != 200:
        print(f"something went wrong: {response.status_code}")
        exit()

    card = CardData(response.json())
    return card

if __name__ == "__main__":
    card = fetchRandomCard(1)
    print(card.name)
    img.imsave("random.png", card.image, cmap="gray")   
