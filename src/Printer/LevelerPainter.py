from .PainterBase import *
from ..MomirVig.MtgCard import MagicCard

class LevelerPainter(PainterBase):
    def paint_card(self, card: MagicCard):
        assert card.face.layout == "leveler"

        self._paintArtistCredit(card.face.image_credit)
        self._paintImage(card)

        self._paintCost(card.face.cost)
        self._paintTitle(card.face.name)
        self._paintTypeline(card.face.type)

        num_levels = len(card.face.oracle)
        oracle_height = int(self.TextRegion.AreaHeight / num_levels)

        # print the rest of the textboxes with levels
        first = True
        for i in range(num_levels):
            oracle_parts = card.face.oracle[i].split("\n", 1)
            level = oracle_parts[0]
            oracle = oracle_parts[1] if len(oracle_parts) > 1 else ""
            stats = card.face.stats[i]

            if first:
                level = ""
                oracle = oracle_parts[0]
                first = False
            self._paint_level(level, oracle, stats, self.TextRegion.HeightOffset + oracle_height * i, oracle_height)


    def _paint_level(self, level: str, oracle:str, stats: str, vPos: int, height: int):
        self._paintStats(stats, vPos)

        oracle_offset: int = 0
        if level:
            level_text = ImageText.Text("LEVEL", mode="1")
            level_bbox = self._paintText((2, vPos + 2), level_text)

            arrow_section = (level_bbox[2] + 2, vPos, level_bbox[2] + 17, vPos + height - 2)
            #self.draw.rectangle(arrow_section)
        
            # level arrow space
            self._reserveBoundingBox(arrow_section)
            self._paintWrappedText((2, int(level_bbox[3] + 2)), level.strip("LEVEL "), large_text_size, height - 2 - (int(level_bbox[3]) - vPos), Decoration.BOLD)
            # paint the level arrow box
            self._paint_level_arrow(arrow_section)
            oracle_offset = int(arrow_section[2] + 2)

        self._paintWrappedText((oracle_offset, vPos), oracle, normal_text_size, height)

    def _paint_level_arrow(self, arrow_section: tuple[float, float, float, float]):
        arrow_point_height = arrow_section[1] + ((arrow_section[3] - arrow_section[1]) / 2)
        self.draw.polygon([(0, arrow_section[1]), (arrow_section[0], arrow_section[1]),
                           (arrow_section[2], arrow_point_height),
                           (arrow_section[0], arrow_section[3]), (0, arrow_section[3])])