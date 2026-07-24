from .SagaPainter import *
from ..MomirVig.MtgCard import MagicCard

class SagaCreaturePainter(SagaPainter):
    def __init__(self, canvas_size: tuple[int, int]):
        super().__init__(canvas_size)
        self.ExplainerRegion.AreaHeight = 60
        self.TextRegion = CardRegion(self.ArtistRegion.HeightOffset - 60, 60)
        self.TypeRegion.HeightOffset = self.TextRegion.HeightOffset - self.TypeRegion.AreaHeight
        saga_text_height = self.TypeRegion.HeightOffset - self.ExplainerRegion.get_total_offset()
        self.SagaTextRegion = CardRegion(self.ExplainerRegion.get_total_offset(), saga_text_height)
        self.ImageRegion = CardRegion(self.SagaTextRegion.HeightOffset, self.SagaTextRegion.AreaHeight)
        
    def paint_card(self, card: MagicCard):
        assert card.face.layout == "saga_creature"

        self._paintArtistCredit(card.face.image_credit)

        self._paintCost(card.face.cost)
        self._paintTitle(card.face.name)
        self._paintImage(card)
        self._paintExplainer(card.face.oracle[0])
        self.SagaTextRegion = CardRegion(self.ImageRegion.HeightOffset, self.ImageRegion.AreaHeight)
        self._paintSagaText(card.face.oracle[1:-1])
        self._paintTypeline(card.face.type)
        self._paintStats(card.face.stats[0], self.StatsRegion.HeightOffset)
        self._paintOracle(card.face.oracle[-1])

    def _paintImage(self, card: MagicCard):      
        if card.image is not None:
            w, h = card.image.size
            crop_top = h * 0.13
            crop_bot = h * 0.11
            card.image = card.image.crop((0, crop_top, w, h - crop_bot))
        super()._paintImage(card)