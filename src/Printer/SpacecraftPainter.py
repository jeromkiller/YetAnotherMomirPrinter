from .PainterBase import *
from ..MomirVig.MtgCard import SpacecraftFace, SpacecraftPart

class SpaceCraftPainter(PainterBase):
    def __init__(self, canvas_size: tuple[int, int]):
        super().__init__(canvas_size)
        self.text_offset = 0

    def paint_card(self, face:SpacecraftFace):
        self._paintArtistCredit(face.image_credit)
        self._paintImage(face.image)

        self._paintCost(face.cost)
        self._paintTitle(face.name)
        self._paintTypeline(face.type)

        num_parts = len(face.spacecraft_parts)
        oracle_height = int(self.TextRegion.AreaHeight / num_parts)
        
        stats_height = self.TextRegion.HeightOffset + (oracle_height * (num_parts - 1)) + ((oracle_height / 2) - (self.StatsRegion.AreaHeight / 2))
        self.StatsRegion.AreaHeight = int(stats_height)
        self._paintStats(face.stats, self.StatsRegion.AreaHeight)

        self._paintSpacecraftOracle(face.spacecraft_parts)

    def _paintSpacecraftOracle(self, sections: list[str | SpacecraftPart]):
        num_parts = len(sections)
        oracle_height = int(self.TextRegion.AreaHeight / num_parts)

        for i, section in enumerate(sections):
            section_height = self.TextRegion.HeightOffset + (oracle_height * i)
            if isinstance(section, SpacecraftPart):
                self.text_offset = 33
                self._paint_station_orb(section_height, section.station)
                self._paintWrappedText((self.text_offset, section_height), section.oracle, self._normal_text_size(), oracle_height)
                self.draw.line(((0, section_height - 2), (self.canvas_size[0], section_height - 2)))
            else:
                self._paintWrappedText((self.text_offset, section_height), section, self._normal_text_size(), oracle_height)

            
    def _paint_station_orb(self, height: int, cost: str):
        # experimental use of text anchors, I should probably implement this more broadly
        radius = 15
        origin = (radius, height + radius)
        wrapped = self._wrapAndResizeText(origin, cost, self._normal_text_size(), self._normal_text_size(), Decoration.BOLD)
        self.draw.text(origin, wrapped, anchor="mm")
        self.draw.circle(origin, radius)
        self._reserveBoundingBox((0, height + radius, radius * 2, height + (radius * 2)))