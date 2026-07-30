from .PainterBase import PainterBase
from ..MomirVig.MtgCard import MagicCard

class StandardPainter(PainterBase):
    def paint_card(self, card:MagicCard):
        assert card.face.layout == "normal"

        self._paintCost(card.face.cost)
        self._paintTitle(card.face.name)
        self._paintImage(card)
        self._paintTypeline(card.face.type)
        self._paintStats(card.face.stats[0], self.StatsRegion.HeightOffset)
        self._paintOracle(card.face.oracle[0])
        self._paintArtistCredit(card.face.image_credit)
