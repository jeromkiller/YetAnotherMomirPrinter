from .PainterBase import PainterBase
from ..MomirVig.MtgCard import DefaultFace

class StandardPainter(PainterBase):
    def paint_card(self, face:DefaultFace):
        self._paintCost(face.cost)
        self._paintTitle(face.name)
        self._paintImage(face.image)
        self._paintTypeline(face.type)
        self._paintStats(face.stats, self.StatsRegion.HeightOffset)
        self._paintOracle(face.oracle)
        self._paintArtistCredit(face.image_credit)
