from . import ProcessImage

import matplotlib.image as img
import numpy as np
from PIL import Image, ImageFile
        
class CardFace():
    def __init__(self, json):
        face = json
        self.layout: str = json["layout"]
        if "card_faces" in json and json["layout"] != "flip":
            face = json["card_faces"][0]
            card_type = face["type_line"]
            if "Saga" in card_type and "Creature" in card_type:
                self.layout = "saga"
            elif "Creature" in card_type:
                self.layout = "normal"
        
        self.name: str = face.get("name", "")
        self.cost: str = face.get("mana_cost", "")
        self.identity: str = "".join(map(str, face.get("colors", [])))
        self.image_url: str = face["image_uris"]["art_crop"]
        self.type: str = face.get("type_line", "")

        self.oracle = list[str]()
        self.stats = list[str]()
        if self.layout == "flip":
            self.oracle = [f["oracle_text"] for f in json["card_faces"]]
            self.stats = [f"{f.get("power", "")}/{f.get("toughness", "")}" for f in json["card_faces"]]
        elif self.layout == "saga":
            self.oracle = [line for line in json["oracle_text"].split("\n")]
            self.stats = [f"{face.get("power", "")}/{face.get("toughness", "")}"]
        else:
            self.oracle = [face.get("oracle_text", "")]
            self.stats = [f"{face.get("power", "")}/{face.get("toughness", "")}"]

    def getFlipName(self, index: int):
        return list(self.name.split(" // "))[index]
    
    def getFlipType(self, index: int):
        return list(self.type.split(" // "))[index]

class NormalFace(CardFace):
    def __init__(self, json):
        super().__init__(json)

class LevelUpFace(CardFace):
    def __init__(self, json):
        super().__init__(json)

class SagaCreatureFace(CardFace):
    def __init__(self, json):
        super().__init__(json)

class FlipFace(CardFace):
    def __init__(self, json):
        super().__init__(json["card_faces"][0])
        secondFace = CardFace(json["card_faces"][1])

class TokenFace(CardFace):
    def __init__(self, json):
        super().__init__(json)

class MagicCard():
    def __init__(self, json):
        self.face = CardFace(json)
        self.image: None | ImageFile.ImageFile = None
        self.extras = list[MagicCard]()
    
    def print_card(self):
        pass

    def setImage(self, image: ImageFile.ImageFile):
        self.image = image

    def addExtraCard(self, extra: 'MagicCard'):
        self.extras.append(extra)

    

