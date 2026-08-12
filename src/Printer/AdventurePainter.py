from .PainterBase import *
from ..MomirVig.MtgCard import AdventureFace

class AdventurePainter(PainterBase):
    def __init__(self, canvas_size: tuple[int, int]):
        super().__init__(canvas_size)
        self.AdventureTitleRegion = CardRegion(self.TypeRegion.get_total_offset(), self._normal_text_size())
        self.AdventureTypeRegion = CardRegion(self.AdventureTitleRegion.get_total_offset(), self._normal_text_size())
        
        oracle_text_height = self.ArtistRegion.HeightOffset - self.AdventureTypeRegion.get_total_offset()
        self.AdventureOracle = CardRegion(self.AdventureTypeRegion.get_total_offset(), oracle_text_height)
    
    def paint_card(self, face:AdventureFace):
        self._paintCost(face.spell_1.cost)
        self._paintTitle(face.spell_1.name)
        self._paintImage(face.image)
        self._paintTypeline(face.spell_1.type)
        self._paintStats(face.spell_1.stats, self.StatsRegion.HeightOffset)
        self._paintOracle(face.spell_1.oracle)

        self._paintAdventureCost(face.spell_2.cost)
        self._paintAdventureTitle(face.spell_2.name)
        self._paintAdventureTypeline(face.spell_2.type)
        self._paintAdventureOracle(face.spell_2.oracle)

        self._drawDividerLine()

        self._paintArtistCredit(face.image_credit)

    def _getAdventureHorizontalOffset(self) -> int:
        return int(self.canvas_size[0] / 2)

    def _paintAdventureCost(self, cost: str):
        horizontal_offset = self._getAdventureHorizontalOffset() + 2
        self._paintRightJustifiedText((horizontal_offset, self.AdventureTitleRegion.HeightOffset), cost, self.AdventureTitleRegion.AreaHeight, Decoration.BOLD)

    def _paintAdventureTitle(self, title: str):
        self._paintWrappedText((0, self.AdventureTitleRegion.HeightOffset), title, self.AdventureTitleRegion.AreaHeight, self.AdventureTitleRegion.AreaHeight, Decoration.BOLD)

    def _paintAdventureTypeline(self, type: str):
        self._paintWrappedText((0, self.AdventureTypeRegion.HeightOffset), type, self.AdventureTypeRegion.AreaHeight, self.AdventureTypeRegion.AreaHeight, Decoration.BOLD)

    def _paintAdventureOracle(self, oracle: str):
        self._paintWrappedText((0, self.AdventureOracle.HeightOffset), oracle, self._normal_text_size(), self.AdventureOracle.AreaHeight)

    def _paintOracle(self, text: str):
        horizontal_offset = self._getAdventureHorizontalOffset() + 2
        bbox = self._paintWrappedText((horizontal_offset, self.TextRegion.HeightOffset), text, self._normal_text_size(), self.TextRegion.AreaHeight)
        self._reserveBoundingBox((horizontal_offset, self.TextRegion.HeightOffset, bbox[2], self.TextRegion.HeightOffset + self.TextRegion.AreaHeight))

    def _drawDividerLine(self):
        horizontal_offset = self._getAdventureHorizontalOffset()
        self.draw.line((horizontal_offset, self.AdventureTitleRegion.HeightOffset, horizontal_offset, self.AdventureOracle.HeightOffset + self.AdventureOracle.AreaHeight))
        self._reserveBoundingBox((horizontal_offset - 2, self.AdventureTitleRegion.HeightOffset, horizontal_offset + 2, self.AdventureOracle.HeightOffset + self.AdventureOracle.AreaHeight))