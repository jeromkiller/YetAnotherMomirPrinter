from PIL import Image, ImageFile
from .exceptions import CardNotCreatureException

class CardFace():
    def __init__(self, json):
        face = json
        self.layout: str = json["layout"]
        # only take the front face of transform cards
        if "card_faces" in json and json["layout"] not in ["flip", "prepare", "adventure", "split"]:
            face = json["card_faces"][0]
            card_type = face["type_line"]
            if "Creature" in card_type:
                self.layout = "normal"

        if self.layout in ["host", "token", "mutate", "prototype", "meld", "double_faced_token", "emblem"]:
            self.layout = "normal"
        
        card_type = face["type_line"]
        if "Saga" in card_type and "Creature" in card_type:
            self.layout = "saga_creature"
        elif "Saga" in card_type:
            self.layout = "saga"

        # todo add creature only restriction if running in momir mode
        #if "Creature" not in card_type and "Token" not in card_type:
        #    raise CardNotCreatureException(json.get("name", "unknown"), json.get("oracle_id"))
        
        self.name: str = face.get("name", "")
        self.cost: str = face.get("mana_cost", "")
        self.identity: str = "".join(map(str, face.get("colors", [])))
        self.image_url: str = face.get("image_uris", json.get("image_uris", {})).get("art_crop", None)
        self.image_credit: str = face.get("artist", "")
        self.type: str = face.get("type_line", "")

        self.oracle = list[str]()
        self.stats = list[str]()
        if self.layout == "flip":
            self.oracle = [f["oracle_text"] for f in json["card_faces"]]
            self.stats = [f"{f.get("power", "")}/{f.get("toughness", "")}" for f in json["card_faces"]]
        if self.layout == "prepare":
            self.oracle = [f["oracle_text"] for f in json["card_faces"]]
            self.stats = [f"{face.get("power", "")}/{face.get("toughness", "")}"]
        elif self.layout == "saga" or self.layout == "saga_creature":
            oracle_parts = json["oracle_text"].split("\n")
            i = 0
            new_oracle = "" 
            for i, part in enumerate(oracle_parts):
                if i == 0:
                    new_oracle = part
                    continue
                if "•" not in part:
                    self.oracle.append(new_oracle)
                    new_oracle = ""
                if new_oracle:
                    new_oracle += "\n" + part
                else:
                    new_oracle += part

            self.oracle.append(new_oracle)
            # saga creatures only flavor text in their textbox need a extra newline at the end so it gets split into an empty string
            if self.layout == "saga_creature" and "—" in oracle_parts[-1]:
                self.oracle.append("")
            self.stats = [f"{face.get("power", "")}/{face.get("toughness", "")}"]
        elif self.layout == "leveler":
            oracle_parts = face["oracle_text"].split("\n")
            i = 0
            new_oracle = ""
            while i < len(oracle_parts):
                if i == 0:
                    self.stats.append(f"{face.get("power", "")}/{face.get("toughness", "")}")
                    new_oracle += oracle_parts[i]
                    i += 1
                    continue
                part = oracle_parts[i]
                if "LEVEL" in part:
                    self.oracle.append(new_oracle)
                    new_oracle = part
                    self.stats.append(oracle_parts[i + 1])
                    i += 2
                else:
                    new_oracle += "\n" + oracle_parts[i]
                    i += 1
            self.oracle.append(new_oracle)
        else:
            self.oracle = [face.get("oracle_text", "")]
            self.stats = [f"{face.get("power", "")}/{face.get("toughness", "")}"]

    def getFlipName(self, index: int):
        return list(self.name.split(" // "))[index]
    
    def getFlipType(self, index: int):
        return list(self.type.split(" // "))[index]
    
    def getFlipCost(self, index: int):
        return list(self.cost.split(" // "))[index]

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
        self.image: None | ImageFile.ImageFile | Image.Image = None
        self.extras = list[MagicCard]()
    
    def print_card(self):
        pass

    def setImage(self, image: ImageFile.ImageFile):
        self.image = image

    def addExtraCard(self, extra: 'MagicCard'):
        self.extras.append(extra)

    

