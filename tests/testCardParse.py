import unittest
import json
from src.MomirVig import MtgCard


class TestCardParsing(unittest.TestCase):
    def test_normal(self):
        with open("tests/resources/normalcard.yaml") as file:
            data = json.load(file)
        card = MtgCard.MagicCard(data)
        self.assertEqual(card.face.name, "Wall of Souls")
        self.assertEqual(card.face.layout, "normal")
        self.assertEqual(card.face.type, "Creature — Wall")
        self.assertEqual(len(card.face.oracle), 1)
        self.assertEqual(card.face.stats, ["0/4"])
        self.assertEqual(card.face.image_credit, "John Matson")

    def test_flip(self):
        with open("tests/resources/flipcard.yaml") as file:
            data = json.load(file)
        card = MtgCard.MagicCard(data)
        self.assertEqual(card.face.getFlipName(0), "Akki Lavarunner")
        self.assertEqual(card.face.getFlipName(1), "Tok-Tok, Volcano Born")
        self.assertEqual(card.face.layout, "flip")
        self.assertEqual(card.face.getFlipType(0), "Creature — Goblin Warrior")
        self.assertEqual(card.face.getFlipType(1), "Legendary Creature — Goblin Shaman")
        self.assertEqual(len(card.face.oracle), 2)
        self.assertEqual(card.face.stats, ["1/1", "2/2"])

    def test_dualside_creature(self):
        with open("tests/resources/dualside_creature.yaml") as file:
            data = json.load(file)
        card = MtgCard.MagicCard(data)
        self.assertEqual(card.face.name, "Delver of Secrets")
        self.assertEqual(card.face.layout, "normal")
        self.assertEqual(card.face.type, "Creature — Human Wizard")
        self.assertEqual(len(card.face.oracle), 1)
        self.assertEqual(card.face.stats, ["1/1"])
        self.assertEqual(card.face.image_credit, "Nils Hamm")

    def test_enchantment_creature(self):
        with open("tests/resources/enchantment_creature.yaml") as file:
            data = json.load(file)
        card = MtgCard.MagicCard(data)
        self.assertEqual(card.face.name, "Summon: Good King Mog XII")
        self.assertEqual(card.face.layout, "saga")
        self.assertEqual(card.face.type, "Enchantment Creature — Saga Moogle")
        self.assertEqual(len(card.face.oracle), 5)
        self.assertEqual(card.face.stats, ["4/4"])

    def test_leveler_creature(self):
        with open("tests/resources/leveler_creature.yaml") as file:
            data = json.load(file)
        card = MtgCard.MagicCard(data)
        self.assertEqual(card.face.name, "Guul Draz Assassin")
        self.assertEqual(card.face.layout, "leveler")
        self.assertEqual(card.face.type, "Creature — Vampire Assassin")
        self.assertEqual(len(card.face.oracle), 3)
        self.assertEqual(card.face.stats, ["1/1", "2/2", "4/4"])

if __name__ == '__main__':
    unittest.main()