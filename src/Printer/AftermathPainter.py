from PIL.Image import Image

from .PainterBase import *
from ..MomirVig.MtgCard import SplitSide, SplitFace

class AftermathPainter(PainterBase):
    def __init__(self, canvas_size: tuple[int, int]):
        super().__init__(canvas_size)
        old_image_height = self.ImageRegion.AreaHeight
        self.ImageRegion.AreaHeight = int(old_image_height / 2)
        self.TypeRegion.HeightOffset = self.ImageRegion.get_total_offset()
        self.TextRegion = CardRegion(self.TypeRegion.get_total_offset(), old_image_height - self.TypeRegion.get_total_offset())
        self.AftermathTextRegion = CardRegion(self.TypeRegion.get_total_offset(), self.canvas_size[0] - self.TypeRegion.get_total_offset())
        self.rightSideWidth: int = self.canvas_size[1] - self.ArtistRegion.AreaHeight - self.TextRegion.get_total_offset()
        
    def paint_card(self, face: SplitFace):
        self._paintArtistCredit(face.image_credit)

        self._rotate_90()
        self._paintAftermathImage(face.image)
        self._paintAftermathCost(face.right_side.cost)
        self._paintAftermathTitle(face.right_side.name)
        self._paintAftermathType(face.right_side.type)
        self._paintAftermathOracle(face.right_side.oracle)

        self._rotate_270()
        self._paintImage(face.image)
        self._paintCost(face.left_side.cost)
        self._paintTitle(face.left_side.name)
        self._paintTypeline(face.left_side.type)
        self._paintOracle(face.left_side.oracle)
        self._paintDividingLine()

    def _getAftermathOffset(self) -> int:
        return self.TextRegion.get_total_offset() + 3

    def _paintImage(self, image: Image | None = None):
        if image:
            im = image.crop((0, 0, image.width * (3/5), image.height))
            im = ImageOps.fit(im, (self.canvas_size[0], self.ImageRegion.AreaHeight))
            im = im.convert("1")
            self.canvas.paste(im, (0, self.ImageRegion.HeightOffset))
        rectangle = (0, self.ImageRegion.HeightOffset, 
                     self.canvas_size[0], self.ImageRegion.get_total_offset())
        self.draw.rectangle(rectangle)
        self._reserveBoundingBox(rectangle)

    def _paintAftermathImage(self, image: Image | None = None):
        if image:
            im = image.crop((image.width * (3/5), 0, image.width, image.height))
            im = ImageOps.fit(im, (self.rightSideWidth, self.ImageRegion.AreaHeight))
            im = im.convert("1")
            self.canvas.paste(im, (self.TextRegion.get_total_offset(), self.ImageRegion.HeightOffset))
        rectangle = (self.TextRegion.get_total_offset(), self.ImageRegion.HeightOffset, 
                     self.TextRegion.get_total_offset() + self.rightSideWidth, self.ImageRegion.HeightOffset + self.ImageRegion.AreaHeight)
        self.draw.rectangle(rectangle)
        self._reserveBoundingBox(rectangle)

    def _paintAftermathTitle(self, title: str):
        offset = self._getAftermathOffset()
        self._paintWrappedText((offset, self.TitleRegion.HeightOffset), title, self._large_text_size(), self.TitleRegion.AreaHeight, Decoration.BOLD)

    def _paintAftermathCost(self, cost: str):
        offset = self.ArtistRegion.AreaHeight
        self._paintRightJustifiedText((offset, self.TitleRegion.HeightOffset), cost, self.TitleRegion.AreaHeight, Decoration.BOLD)

    def _paintAftermathType(self, typeline: str):
        offset = self._getAftermathOffset()
        self._paintWrappedText((offset, self.TypeRegion.HeightOffset), typeline, self._large_text_size(), self.TypeRegion.AreaHeight, Decoration.BOLD)

    def _paintAftermathOracle(self, text: str):
        offset = self._getAftermathOffset()
        bbox = self._paintWrappedText((offset, self.TextRegion.HeightOffset), text, self._normal_text_size(), self.TextRegion.AreaHeight)
        self._reserveBoundingBox((offset, self.TextRegion.HeightOffset, bbox[3], self.TextRegion.get_total_offset()))

    def _paintDividingLine(self):
        self.draw.line((0, self.TextRegion.get_total_offset(), self.canvas_size[0], self.TextRegion.get_total_offset()))