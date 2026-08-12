from .PainterBase import *
from ..MomirVig.MtgCard import PrototypeFace

class PrototypePainter(PainterBase):
    def __init__(self, canvas_size: tuple[int, int]):
        super().__init__(canvas_size)
        self.prototypeExplainerSection = CardRegion(self.TypeRegion.get_total_offset(), self._normal_text_size() * 3)
        self.prototypeCostSection = CardRegion(self.TypeRegion.get_total_offset(), self._normal_text_size())
        self.prototypeStatSection = CardRegion(self.prototypeExplainerSection.get_total_offset() - self.StatsRegion.AreaHeight, self.StatsRegion.AreaHeight)
        self.dividerLine = CardRegion(self.prototypeExplainerSection.get_total_offset(), 3)
        self.TextRegion = CardRegion(self.dividerLine.get_total_offset(), self.TextRegion.AreaHeight - self.prototypeExplainerSection.AreaHeight)

    def paint_card(self, face: PrototypeFace):
        self._paintArtistCredit(face.image_credit)
        self._paintCost(face.cost)
        self._paintTitle(face.name)
        self._paintImage(face.image)
        self._paintTypeline(face.type)

        self._paintStats(face.prototype_stats, self.prototypeStatSection.HeightOffset)
        self._paint_prototype_cost(face.prototype_cost)
        self._paint_prototype_oracle(face.prototype_oracle)

        self.draw.line((0, self.dividerLine.HeightOffset, self.canvas_size[0], self.dividerLine.HeightOffset))

        self._paintStats(face.stats, self.StatsRegion.HeightOffset)
        self._paintOracle(face.oracle)

    def _paint_prototype_cost(self, cost: str):
        bbox = self._paintRightJustifiedText((0, self.prototypeCostSection.HeightOffset + 1), cost, self.prototypeCostSection.AreaHeight, Decoration.BOLD)
        self.draw.rectangle((bbox[0] - 1, bbox[1] - 3, self.canvas_size[0], bbox[3] + 2))
        self._reserveBoundingBox((bbox[0] - 1, bbox[1] - 3, self.canvas_size[0], bbox[3] + 2))


    def _paint_prototype_oracle(self, text: str):
        self._paintWrappedText((0, self.prototypeExplainerSection.HeightOffset), text, self._normal_text_size(), self.prototypeExplainerSection.AreaHeight)
