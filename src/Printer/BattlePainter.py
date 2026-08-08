from PIL.Image import Image

from .PainterBase import *
from ..MomirVig.MtgCard import BattleFace

class BattlePainter(PainterBase):
    def __init__(self, canvas_size: tuple[int, int]):
        super().__init__(canvas_size)
        content_height = int((self.canvas_size[0] - (self.TitleRegion.AreaHeight + self.TypeRegion.AreaHeight)) / 2)
        self.ImageRegion.AreaHeight = content_height
        self.TypeRegion.HeightOffset = self.ImageRegion.get_total_offset()
        self.TextRegion = CardRegion(self.TypeRegion.get_total_offset(), content_height)
        self.StatsRegion.HeightOffset = self.canvas_size[0] - self.StatsRegion.AreaHeight

    def paint_card(self, face: BattleFace):
        self._paintArtistCredit(face.image_credit)
        self._rotate_270()
        self._paintCost(face.cost)
        self._paintTitle(face.name)
        self._paintImage(face.image)
        self._paintTypeline(face.type)
        self._paintStats(f" {face.defense} ", self.StatsRegion.HeightOffset)
        self._paintOracle(face.oracle)
        self._rotate_90()

    def _get_horizontal_offset(self) -> int:
        return self.ArtistRegion.AreaHeight

    def _paintImage(self, image: Image | None = None):
        image_width = self.canvas_size[1] - self.ArtistRegion.AreaHeight
        if image:
            im = ImageOps.fit(image, (image_width, self.ImageRegion.AreaHeight))
            im = im.convert("1")
            self.canvas.paste(im, (self.ArtistRegion.AreaHeight, self.ImageRegion.HeightOffset))
        rectangle = (self.ArtistRegion.AreaHeight, self.ImageRegion.HeightOffset,
                     self.ArtistRegion.AreaHeight + image_width, self.ImageRegion.get_total_offset())
        self.draw.rectangle(rectangle)
        self._reserveBoundingBox(rectangle)

    def _paintTitle(self, card_name: str):
        offset = self._get_horizontal_offset()
        self._paintWrappedText((offset, self.TitleRegion.HeightOffset), card_name, large_text_size, self.TitleRegion.AreaHeight, Decoration.BOLD)


    def _paintTypeline(self, typeline: str):
        offset = self._get_horizontal_offset()
        self._paintWrappedText((offset, self.TypeRegion.HeightOffset), typeline, large_text_size, self.TypeRegion.AreaHeight, Decoration.BOLD)

    def _paintOracle(self, text: str):
        offset = self._get_horizontal_offset()
        bbox = self._paintWrappedText((offset, self.TextRegion.HeightOffset), text, normal_text_size, self.TextRegion.AreaHeight)
        self._reserveBoundingBox((offset, self.TextRegion.HeightOffset, bbox[3], self.TextRegion.get_total_offset()))
