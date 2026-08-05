from .SagaPainter import *
from ..MomirVig.MtgCard import SagaCreatureFace
from typing import overload

class SagaCreaturePainter(SagaPainter):
    def __init__(self, canvas_size: tuple[int, int]):
        super().__init__(canvas_size)
        self.ExplainerRegion.AreaHeight = 60
        self.TextRegion = CardRegion(self.ArtistRegion.HeightOffset - 60, 60)
        self.TypeRegion.HeightOffset = self.TextRegion.HeightOffset - self.TypeRegion.AreaHeight
        saga_text_height = self.TypeRegion.HeightOffset - self.ExplainerRegion.get_total_offset()
        self.SagaTextRegion = CardRegion(self.ExplainerRegion.get_total_offset(), saga_text_height)
        self.ImageRegion = CardRegion(self.SagaTextRegion.HeightOffset, self.SagaTextRegion.AreaHeight)
   
    @overload
    def paint_card(self, face: SagaCreatureFace): ...

    @overload
    def paint_card(self, face: SagaFace): ...

    def paint_card(self, face: SagaFace | SagaCreatureFace):
        if not isinstance(face, SagaCreatureFace):
            super().paint_card(face)
            return
        
        self._paintArtistCredit(face.image_credit)

        self._paintCost(face.cost)
        self._paintTitle(face.name)
        self._paintImage(face.image)
        self._paintExplainer(face.explainer)
        self.SagaTextRegion = CardRegion(self.ImageRegion.HeightOffset, self.ImageRegion.AreaHeight)
        self._paintSagaText(face.saga_sections)
        self._paintTypeline(face.type)
        self._paintStats(face.stats, self.StatsRegion.HeightOffset)
        self._paintOracle(face.oracle)

    def _paintImage(self, image: Image.Image | None = None):      
        if image is not None:
            w, h = image.size
            crop_top = h * 0.13
            crop_bot = h * 0.11
            image = image.crop((0, crop_top, w, h - crop_bot))
        super()._paintImage(image)