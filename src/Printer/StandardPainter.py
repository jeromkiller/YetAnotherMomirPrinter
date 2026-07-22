from .PainterBase import PainterBase
from ..MomirVig.MtgCard import MagicCard

class StandardPainter(PainterBase):
    def paint_card(self, card:MagicCard):
        assert card.face.layout == "normal"

        # paint elements in reverse
        self._paintCost(card.face.cost)
        self._paintTitle(card.face.name)
        self._paintImage(card)
        self._paintTypeline(card.face.type)
        self._paintOracle(card.face.oracle[0])
        self._paintArtistCredit(card.face.image_credit)
        self._paintStats(card.face.stats[0], self.canvas.height - 23)

        # oracle text

        # stats & credit
        #self._paintBottom(card.face.image_credit, card.face.stats[0])
