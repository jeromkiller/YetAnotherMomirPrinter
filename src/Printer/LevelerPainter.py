from .PainterBase import *
from ..MomirVig.MtgCard import LevelerFace, level_block

class LevelerPainter(PainterBase):
    def paint_card(self, face: LevelerFace):
        self._paintArtistCredit(face.image_credit)
        self._paintImage(face.image)

        self._paintCost(face.cost)
        self._paintTitle(face.name)
        self._paintTypeline(face.type)

        num_levels = len(face.levels)
        oracle_height = int(self.TextRegion.AreaHeight / num_levels)

        # print the rest of the textboxes with levels
        for i, level in enumerate(face.levels):

            self._paint_level(level, self.TextRegion.HeightOffset + oracle_height * i, oracle_height)


    def _paint_level(self, level_block: level_block, vPos: int, height: int):
        self._paintStats(level_block.stats, vPos)

        oracle_offset: int = 0
        level = level_block.level
        if level:
            level_text = ImageText.Text("LEVEL", mode="1")
            level_bbox = self._paintText((2, vPos + 2), level_text)

            arrow_section = (level_bbox[2] + 2, vPos, level_bbox[2] + 17, vPos + height - 2)
        
            # level arrow space
            self._reserveBoundingBox(arrow_section)
            self._paintWrappedText((2, int(level_bbox[3] + 2)), level.strip("LEVEL "), self._large_text_size(), height - 2 - (int(level_bbox[3]) - vPos), Decoration.BOLD)
            # paint the level arrow box
            self._paint_level_arrow(arrow_section)
            oracle_offset = int(arrow_section[2] + 2)

        self._paintWrappedText((oracle_offset, vPos), level_block.oracle, self._normal_text_size(), height)

    def _paint_level_arrow(self, arrow_section: tuple[float, float, float, float]):
        arrow_point_height = arrow_section[1] + ((arrow_section[3] - arrow_section[1]) / 2)
        self.draw.polygon([(0, arrow_section[1]), (arrow_section[0], arrow_section[1]),
                           (arrow_section[2], arrow_point_height),
                           (arrow_section[0], arrow_section[3]), (0, arrow_section[3])])