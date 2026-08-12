from .PainterBase import *
from ..MomirVig.MtgCard import PrepareFace

class PreparedPainter(PainterBase):
    def __init__(self, canvas_size: tuple[int, int]):
        super().__init__(canvas_size)
        self.PrepareTitleRegion = CardRegion(self.TypeRegion.get_total_offset(), self._normal_text_size())
        self.PrepareTypeRegion = CardRegion(self.PrepareTitleRegion.get_total_offset(), self._normal_text_size())
        
        oracle_text_height = self.ArtistRegion.HeightOffset - self.PrepareTypeRegion.get_total_offset()
        self.PrepareOracle = CardRegion(self.PrepareTypeRegion.get_total_offset(), oracle_text_height)
    
    def paint_card(self, face:PrepareFace):
        self._paintCost(face.spell_1.cost)
        self._paintTitle(face.spell_1.name)
        self._paintImage(face.image)
        self._paintTypeline(face.spell_1.type)
        self._paintStats(face.spell_1.stats, self.StatsRegion.HeightOffset)

        self._paintPrepareCost(face.spell_2.cost)
        self._paintPrepareTitle(face.spell_2.name)
        self._paintPrepareTypeline(face.spell_2.type)
        self._paintPrepareOracle(face.spell_2.oracle)

        self._drawDividerLine()

        self._paintOracle(face.spell_1.oracle)
        self._paintArtistCredit(face.image_credit)

    def _getPrepareHorizontalOffset(self) -> int:
        return int(self.canvas_size[0] / 2)

    def _paintPrepareCost(self, cost: str):
        self._paintRightJustifiedText((0, self.PrepareTitleRegion.HeightOffset), cost, self.PrepareTitleRegion.AreaHeight, Decoration.BOLD)

    def _paintPrepareTitle(self, title: str):
        horizontal_offset = self._getPrepareHorizontalOffset() + 2
        self._paintWrappedText((horizontal_offset, self.PrepareTitleRegion.HeightOffset), title, self.PrepareTitleRegion.AreaHeight, self.PrepareTitleRegion.AreaHeight, Decoration.BOLD)

    def _paintPrepareTypeline(self, type: str):
        horizontal_offset = self._getPrepareHorizontalOffset() + 2
        self._paintWrappedText((horizontal_offset, self.PrepareTypeRegion.HeightOffset), type, self.PrepareTypeRegion.AreaHeight, self.PrepareTypeRegion.AreaHeight, Decoration.BOLD)

    def _paintPrepareOracle(self, oracle: str):
        horizontal_offset = self._getPrepareHorizontalOffset() + 2
        bbox = self._paintWrappedText((horizontal_offset, self.PrepareOracle.HeightOffset), oracle, self._normal_text_size(), self.PrepareOracle.AreaHeight)
        self._reserveBoundingBox((horizontal_offset, self.PrepareOracle.HeightOffset, bbox[2], self.PrepareOracle.HeightOffset + self.PrepareOracle.AreaHeight))

    def _drawDividerLine(self):
        horizontal_offset = self._getPrepareHorizontalOffset()
        self.draw.line((horizontal_offset, self.PrepareTitleRegion.HeightOffset, horizontal_offset, self.PrepareOracle.HeightOffset + self.PrepareOracle.AreaHeight))
        self._reserveBoundingBox((horizontal_offset - 2, self.PrepareTitleRegion.HeightOffset, horizontal_offset + 2, self.PrepareOracle.HeightOffset + self.PrepareOracle.AreaHeight))