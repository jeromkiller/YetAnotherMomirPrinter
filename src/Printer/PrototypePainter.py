from .PainterBase import *
from ..MomirVig.MtgCard import MagicCard

class PrototypePainter(PainterBase):
    def __init__(self, canvas_size: tuple[int, int]):
        super().__init__(canvas_size)
        self.prototypeExplainerSection = CardRegion(self.TypeRegion.get_total_offset(), normal_text_size * 3)
        self.prototypeCostSection = CardRegion(self.TypeRegion.get_total_offset(), normal_text_size)
        self.prototypeStatSection = CardRegion(self.prototypeExplainerSection.get_total_offset() - self.StatsRegion.AreaHeight, self.StatsRegion.AreaHeight)
        self.dividerLine = CardRegion(self.prototypeExplainerSection.get_total_offset(), 3)
        self.TextRegion = CardRegion(self.dividerLine.get_total_offset(), self.TextRegion.AreaHeight - self.prototypeExplainerSection.AreaHeight)

    def paint_card(self, card: MagicCard):
        assert card.face.layout == "prototype"

        self._paintArtistCredit(card.face.image_credit)
        self._paintCost(card.face.cost)
        self._paintTitle(card.face.name)
        self._paintImage(card)
        self._paintTypeline(card.face.type)

        self._paintStats(card.face.stats[0], self.prototypeStatSection.HeightOffset)
        self._paint_prototype_cost(card.face.oracle[1])
        self._paint_prototype_oracle(card.face.oracle[0])

        self.draw.line((0, self.dividerLine.HeightOffset, self.canvas_size[0], self.dividerLine.HeightOffset))

        self._paintStats(card.face.stats[1], self.StatsRegion.HeightOffset)
        self._paintOracle(card.face.oracle[2])

    def _paint_prototype_cost(self, cost: str):
        bbox = self._paintRightJustifiedText((0, self.prototypeCostSection.HeightOffset + 1), cost, self.prototypeCostSection.AreaHeight, Decoration.BOLD)
        self.draw.rectangle((bbox[0] - 1, bbox[1] - 3, self.canvas_size[0], bbox[3] + 2))
        self._reserveBoundingBox((bbox[0] - 1, bbox[1] - 3, self.canvas_size[0], bbox[3] + 2))


    def _paint_prototype_oracle(self, text: str):
        self._paintWrappedText((0, self.prototypeExplainerSection.HeightOffset), text, normal_text_size, self.prototypeExplainerSection.AreaHeight)
