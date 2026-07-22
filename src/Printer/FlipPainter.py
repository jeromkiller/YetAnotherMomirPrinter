from .PainterBase import *
from ..MomirVig.MtgCard import MagicCard

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
        self._paintArtistCredit(card.face.image_credit)
        self._paintImage(card)

        #self._paintBottom(card.face.image_credit, "")
        self.paint_side(card, 0)

        # offset the regions
        self.TitleRegion.HeightOffset += self.BottomRegion.AreaHeight
        self.TextRegion.HeightOffset += self.BottomRegion.AreaHeight
        self.TypeRegion.HeightOffset += self.BottomRegion.AreaHeight

        # paint the reverse side
        self._rotate_180()
        self.paint_side(card, 1)

        # flip the card back
        self._rotate_180()
        

    def paint_side(self, card: MagicCard, side: int):
        cost = ""
        if side == 0:
            cost = card.face.cost

        self._paintCost(cost)
        self._paintTitle(card.face.getFlipName(side))
        self._paintOracle(card.face.oracle[side])
        self._paintStats(card.face.stats[0], self.TypeRegion.HeightOffset)
        self._paintTypeline(card.face.getFlipType(side))
