from PIL import Image, ImageFile
from .exceptions import CardNotCreatureException, CardNotParsableException
from dataclasses import dataclass
from typing import TypeAlias
import re

class CardFace():
    @staticmethod
    def get_face(json, card_part_offset: int):
        face = json
        if "card_faces" in json:
            face = json["card_faces"][card_part_offset]
        return face

    def __init__(self, json, card_part_offset: int):
        face = self.get_face(json, card_part_offset)

        self.image_url: str = ""
        if "image_uris" in face:
            self.image_url = face.get("image_uris", json.get("image_uris", {})).get("art_crop", None)
        else:
            self.image_url = json.get("image_uris", json.get("image_uris", {})).get("art_crop", None)

        self.image_credit: str = ""
        if "artist" in face:
            self.image_credit: str = face.get("artist", "")
        else:
            self.image_credit: str = json.get("artist", "")

        self.image: None | ImageFile.ImageFile | Image.Image = None

        self.identity: str = "".join(map(str, json.get("color_identity", [])))

class DefaultFace(CardFace):
    def __init__(self, json, card_part_offset: int):
        super().__init__(json, card_part_offset)
        face = self.get_face(json, card_part_offset)

        self.name: str = face.get("name", "")
        self.cost: str = face.get("mana_cost", "")
        self.colors: str = "".join(map(str, face.get("colors", [])))
        self.type: str = face.get("type_line", "")
        self.oracle: str = face.get("oracle_text", "")
        self.stats: str = ""
        if "power" in face and "toughness" in face:
            self.stats = f"{face.get("power", "")}/{face.get("toughness", "")}"

@dataclass(frozen=True)
class level_block():
    level: str
    oracle: str
    stats: str

class LevelerFace(CardFace):
    def __init__(self, json, card_part_offset: int):
        super().__init__(json, card_part_offset)
        face = self.get_face(json, card_part_offset)

        self.name: str = face.get("name", "")
        self.cost: str = face.get("mana_cost", "")
        self.colors: str = "".join(map(str, face.get("colors", [])))
        self.type: str = face.get("type_line", "")
        self.levels: list[level_block] = list()

        oracle = ""
        level = ""
        stats = f"{face.get("power", "")}/{face.get("toughness", "")}"
        for part in face.get("oracle_text", "").split("\n"):
            if "LEVEL" in part:
                self.levels.append(level_block(level, oracle, stats))
                oracle = ""
                stats = ""
                level = part
            elif stats == "":
                stats = part
            elif oracle == "":
                oracle = part
            else:
                oracle += "\n" + part
        self.levels.append(level_block(level, oracle, stats))

class FlipSide():
    def __init__(self, part):
        self.name: str = part.get("name", "")
        self.cost: str = part.get("mana_cost", "")
        self.oracle: str = part.get("oracle_text")
        self.type: str = part.get("type_line", "")
        self.stats = ""
        if "power" in part and "toughness" in part:
            self.stats = f"{part.get("power", "")}/{part.get("toughness", "")}"

class FlipFace(CardFace):
    def __init__(self, json, card_part_offset: int):
        super().__init__(json, card_part_offset)
        self.colors: str = "".join(map(str, json.get("colors", [])))
        self.up_side: FlipSide = FlipSide(self.get_face(json, card_part_offset))
        self.down_side: FlipSide = FlipSide(self.get_face(json, card_part_offset + 1))

@dataclass(frozen=True)
class SagaSection():
    levels: list[str]
    oracle: str

class SagaFace(CardFace):
    def __init__(self, json, card_part_offset: int):
        super().__init__(json, card_part_offset)
        face = self.get_face(json, card_part_offset)
        self.name: str = face
        self.name: str = face.get("name", "")
        self.cost: str = face.get("mana_cost", "")
        self.colors: str = "".join(map(str, face.get("colors", [])))
        self.type: str = face.get("type_line", "")

        oracle_parts = json["oracle_text"].split("\n")
        self.explainer: str = oracle_parts[0]

        i = 0
        self.saga_sections: list[SagaSection] = list()
        new_oracle = "" 
        for i, part in enumerate(oracle_parts):
            if i == 0:
                new_oracle = part
                continue
            if "•" not in part:
                sections = list(new_oracle.split(" — ", 1))
                if len(sections) == 1:
                    self.explainer = sections[0]
                else:
                    levels: list[str] = list(sections[0].split(", "))
                    oracle: str = sections[1]
                    self.saga_sections.append(SagaSection(levels, oracle))
                new_oracle = ""
            if new_oracle:
                new_oracle += "\n" + part
            else:
                new_oracle += part

        sections = list(new_oracle.split(" — ", 1))
        if len(sections) > 2:
            levels: list[str] = list(sections[0].split(", "))
            oracle: str = sections[1]
            self.saga_sections.append(SagaSection(levels, oracle))

class SagaCreatureFace(SagaFace):
    def __init__(self, json, card_part_offset: int):
        super().__init__(json, card_part_offset)
        face = self.get_face(json, card_part_offset)
        oracle_parts = list(face["oracle_text"].split("\n"))
        self.oracle: str = oracle_parts[-1]
        self.stats: str = ""
        if "power" in face and "toughness" in face:
            self.stats = f"{face.get("power", "")}/{face.get("toughness", "")}"

class PrototypeFace(CardFace):
    def __init__(self, json, card_part_offset: int):
        super().__init__(json, card_part_offset)
        face = self.get_face(json, card_part_offset)

        self.name: str = face.get("name", "")
        self.cost: str = face.get("mana_cost", "")
        self.colors: str = "".join(map(str, face.get("colors", [])))
        self.type: str = face.get("type_line", "")
        self.stats: str = ""
        if "power" in face and "toughness" in face:
            self.stats = f"{face.get("power", "")}/{face.get("toughness", "")}"

        oracle_parts = face.get("oracle_text", "").split("\n", 1)

        prototype_section = oracle_parts[0]
        prototype_split = prototype_section.split(" — ", 1)
        prototype_cost_parts = prototype_split[0].split(" ")
        prototype_stats_parts = prototype_split[1].split(" ")

        self.prototype_cost: str = prototype_cost_parts[-1]
        self.prototype_stats: str = prototype_stats_parts[0]
        self.prototype_oracle: str = " ".join(prototype_cost_parts[:-1]) + " " + " ".join(prototype_stats_parts[1:])

        self.oracle: str = oracle_parts[1]
class DualSpellFace(CardFace):
    def __init__(self, json, card_part_offset: int):
        super().__init__(json, card_part_offset)
        self.spell_1: DefaultFace = DefaultFace(json, card_part_offset)
        self.spell_2: DefaultFace = DefaultFace(json, card_part_offset + 1)

class AdventureFace(DualSpellFace):
    def __init__(self, json, card_part_offset: int):
        super().__init__(json, card_part_offset)

class PrepareFace(DualSpellFace):
    def __init__(self, json, card_part_offset: int):
        super().__init__(json, card_part_offset)

@dataclass(frozen=True)
class PlaneswalkerAbilityBlock():
    cost: int
    oracle: str

class PlaneswalkerFace(CardFace):
    def __init__(self, json, card_part_offset: int):
        super().__init__(json, card_part_offset)
        face = self.get_face(json, card_part_offset)

        self.name: str = face.get("name", "")
        self.cost: str = face.get("mana_cost", "")
        self.colors: str = "".join(map(str, face.get("colors", [])))
        self.type: str = face.get("type_line", "")
        self.loyalty: str = face.get("loyalty", "")

        self.abilities: list[str | PlaneswalkerAbilityBlock] = list()
        for line in face.get("oracle_text", "").split("\n"):
            starting_number_list = re.findall(r"^[+−-]?\d+: ", line)
            if starting_number_list:
                starting_number = starting_number_list[0]
                oracle = line.strip(starting_number)
                starting_number = starting_number.replace("−", "-")
                self.abilities.append(PlaneswalkerAbilityBlock(int(starting_number.strip(": ")), oracle))
            else:
                self.abilities.append(line)

class SplitSide():
    def __init__(self, face, has_reminder_text: bool = False):
        self.name: str = face.get("name", "")
        self.cost: str = face.get("mana_cost", "")
        self.colors: str = "".join(map(str, face.get("colors", [])))
        self.type: str = face.get("type_line", "")
        if has_reminder_text:
            self.oracle: str = "\n".join(face.get("oracle_text", "").split("\n")[:-1])
        else:
            self.oracle: str = face.get("oracle_text", "")

class SplitFace(CardFace):
    def __init__(self, json, card_part_offset: int):
        super().__init__(json, card_part_offset)
        face_1 = self.get_face(json, card_part_offset)
        face_2 = self.get_face(json, card_part_offset + 1)
        self.left_side: SplitSide = SplitSide(face_1)
        self.right_side: SplitSide = SplitSide(face_2)

class AftermathFace(SplitFace):
    def __init__(self, json, card_part_offset: int):
        super().__init__(json, card_part_offset)

class ReminderSplitFace(SplitFace):
    def __init__(self, json, card_part_offset: int):
        super().__init__(json, card_part_offset)
        self.reminder: str = self.left_side.oracle.split("\n")[-1]
        self.left_side.oracle = "\n".join(self.left_side.oracle.split("\n")[:-1])
        self.right_side.oracle = "\n".join(self.right_side.oracle.split("\n")[:-1])

class FuseFace(ReminderSplitFace):
    def __init__(self, json, card_part_offset: int):
        super().__init__(json, card_part_offset)

class RoomFace(ReminderSplitFace):
    def __init__(self, json, card_part_offset: int):
        super().__init__(json, card_part_offset)
        self.right_side.type = ""

class BattleFace(CardFace):
    def __init__(self, json, card_part_offset: int):
        super().__init__(json, card_part_offset)
        face = self.get_face(json, card_part_offset)

        self.name: str = face.get("name", "")
        self.cost: str = face.get("mana_cost", "")
        self.colors: str = "".join(map(str, face.get("colors", [])))
        self.type: str = face.get("type_line", "")
        self.oracle: str = face.get("oracle_text", "")
        self.defense: str = face.get("defense", "")

class MagicCard():
    def __init__(self, json):
        # figure out the card type
        self.layout = json["layout"]

        # treat these special kinds of cards as regular for now
        if self.layout in ["host", "token", "mutate", "meld", "double_faced_token", "emblem"]:
            self.layout = "normal"

        self.front_face, offset = self.create_face(json, 0)
        self.back_face: CardFace | None = None
        if self.layout in ["transform", "modal_dfc", "battle"]:
            self.back_face, offset = self.create_face(json, offset)

        self.extras = list[MagicCard]()

    @staticmethod
    def create_face(json, card_part_offset: int) -> tuple[CardFace, int]:
        layout = json["layout"]
        # treat these special kinds of cards as regular for now
        if layout in ["host", "token", "mutate", "meld", "double_faced_token", "emblem"]:
            layout = "normal"

        face = CardFace.get_face(json, card_part_offset)
        type = face["type_line"]
        keywords = json.get("keywords", [])
        if layout == "transform":
            if "Saga" in type:
                layout = "saga"
            elif "Battle" in type:
                layout = "battle"
            else:
                layout = "normal"
        
        if layout == "normal":
            if "Spacecraft" in type or "Planet" in type:
                layout = "unsupported"
            elif "Planeswalker" in type:
                layout = "planeswalker"

        # some un cards have more than 2 faces, currently unsupported
        if len(json.get("name", "").split("//")) > 2:
            raise CardNotParsableException(json.get("name", "Unknown Cardname"), json.get("id", "Unknown card_id"))

        if layout == "normal":
            return DefaultFace(json, card_part_offset), card_part_offset+ 1
        elif layout == "leveler":
            return LevelerFace(json, card_part_offset), card_part_offset + 1
        elif layout == "flip":
            return FlipFace(json, card_part_offset), card_part_offset + 2
        elif layout == "saga":
            if "Creature" in type:
                return SagaCreatureFace(json, card_part_offset), card_part_offset + 1
            else:
                return SagaFace(json, card_part_offset), card_part_offset + 1
        elif layout == "adventure":
            return AdventureFace(json, card_part_offset), card_part_offset + 2
        elif layout == "prepare":
            return PrepareFace(json, card_part_offset), card_part_offset + 2
        elif layout == "prototype":
            return PrototypeFace(json, card_part_offset), card_part_offset + 1
        elif layout == "planeswalker":
            return PlaneswalkerFace(json, card_part_offset), card_part_offset + 1
        elif layout == "split":    # triple faced card is not parsable right now
            if "Aftermath" in keywords:
                return AftermathFace(json, card_part_offset), card_part_offset + 2
            elif "Fuse" in keywords:
                return FuseFace(json, card_part_offset), card_part_offset + 2
            elif "Room" in type:
                return RoomFace(json, card_part_offset), card_part_offset + 2
            else:
                return SplitFace(json, card_part_offset), card_part_offset + 2
        elif layout == "battle":
            return BattleFace(json, card_part_offset), card_part_offset + 1
        
        raise CardNotParsableException(json.get("name", "Unknown Cardname"), json.get("id", "Unknown card_id"))

    def setImage(self, image: ImageFile.ImageFile):
        self.front_face.image = image

    def setImage2(self, image: ImageFile.ImageFile):
        if self.back_face:
            self.back_face.image = image

    def addExtraCard(self, extra: 'MagicCard'):
        self.extras.append(extra)

    

