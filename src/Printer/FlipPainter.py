from .PainterBase import *
from ..MomirVig.MtgCard import FlipFace, FlipSide

class FlipPainter(PainterBase):
    def __init__(self, canvas_size: tuple[int, int]):
        super().__init__(canvas_size)
        image_height = int(self.canvas_size[0] * 2 / 4)
        text_height = int((self.canvas_size[1] - ((2 * self.TitleRegion.get_total_offset()) + (2 * large_text_size) + image_height + self.ArtistRegion.AreaHeight)) / 2)
        self.TextRegion = CardRegion(self.TitleRegion.get_total_offset(), text_height)
        self.TypeRegion = CardRegion(self.TextRegion.get_total_offset(), large_text_size)
        self.ImageRegion = CardRegion(self.TypeRegion.get_total_offset(), image_height)
        self.StatsRegion.HeightOffset = self.ImageRegion.HeightOffset - self.StatsRegion.AreaHeight

    def paint_card(self, face: FlipFace):
        self._paintArtistCredit(face.image_credit)
        self._paintImage(face.image)

        #self._paintBottom(card.face.image_credit, "")
        self.paint_side(face.up_side)

        # offset the regions
        self.TitleRegion.HeightOffset += self.ArtistRegion.AreaHeight
        self.TextRegion.HeightOffset += self.ArtistRegion.AreaHeight
        self.TypeRegion.HeightOffset += self.ArtistRegion.AreaHeight
        self.StatsRegion.HeightOffset += self.ArtistRegion.AreaHeight

        # paint the reverse side
        self._rotate_180()
        self.paint_side(face.down_side)

        # flip the card back
        self._rotate_180()
        

    def paint_side(self, side: FlipSide):
        self._paintCost(side.cost)
        self._paintTitle(side.name)
        self._paintOracle(side.oracle)
        self._paintStats(side.stats, self.StatsRegion.HeightOffset)
        self._paintTypeline(side.type)
