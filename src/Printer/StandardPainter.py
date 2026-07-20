from .PainterBase import PainterBase
from ..MomirVig.MtgCard import MagicCard

class StandardPainter(PainterBase):
    def paint_card(self, card:MagicCard):
        assert card.face.layout == "normal"
        self._paintTitle(card.face.name, card.face.cost)
        self._paintImage(card)
        self._paintTypeline(card.face.type)

        # oracle text
        self._paintOracle(card.face.oracle[0])

        # stats & credit
        self._paintBottom(card.face.image_credit, card.face.stats[0])
