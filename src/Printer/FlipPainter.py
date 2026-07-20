from .PainterBase import *
from ..MomirVig.MtgCard import MagicCard
from PIL import Image, ImageFont, ImageDraw

class FlipPainter(PainterBase):
    def __init__(self, canvas_size: tuple[int, int]):
        super().__init__(canvas_size)
        image_height = int(self.canvas_size[0] * 2 / 4)
        self.BottomRegion = CardRegion(self.canvas_size[1] - 10, 10)
        text_height = int((self.canvas_size[1] - ((2 * self.TitleRegion.get_total_offset()) + (2 * (large_text_size + 4)) + image_height + self.BottomRegion.AreaHeight)) / 2)
        self.TextRegion = CardRegion(self.TitleRegion.get_total_offset(), text_height)
        self.TypeRegion = CardRegion(self.TextRegion.get_total_offset(), large_text_size + 4)
        self.ImageRegion = CardRegion(self.TypeRegion.get_total_offset(), image_height)
        

    def paint_card(self, card: MagicCard):
        assert card.face.layout == "flip"
        self._paintBottom(card.face.image_credit, "")
        self._paintImage(card)
        self.paint_side(card, 0)

        # offset the regions
        self.TitleRegion.HeightOffset += self.BottomRegion.AreaHeight
        self.TextRegion.HeightOffset += self.BottomRegion.AreaHeight
        self.TypeRegion.HeightOffset += self.BottomRegion.AreaHeight

        # paint the reverse side
        self.canvas = self.canvas.rotate(180)
        self.draw = ImageDraw.Draw(self.canvas)
        self.paint_side(card, 1)

        # flip the card back
        self.canvas = self.canvas.rotate(180)
        

    def paint_side(self, card: MagicCard, side: int):
        cost = ""
        if side == 0:
            cost = card.face.cost
        self._paintTitle(card.face.getFlipName(side), cost)
        self._paintTypeline(card.face.getFlipType(side))
        self._paintOracle(card.face.oracle[side])
