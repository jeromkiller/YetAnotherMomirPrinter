from PIL import Image

from .PainterBase import *
from ..MomirVig.MtgCard import SplitSide, SplitFace

class SplitPainter(PainterBase):
    def __init__(self, canvas_size: tuple[int, int]):
        super().__init__(canvas_size)
        self.ImageRegion.AreaHeight = int(self.ImageRegion.AreaHeight / 1.7)
        self.TypeRegion.HeightOffset = self.ImageRegion.get_total_offset()
        text_height = canvas_size[0] - self.TypeRegion.get_total_offset()
        self.TextRegion = CardRegion(self.TypeRegion.get_total_offset(), text_height)

    def paint_card(self, face: SplitFace):
        self._paintArtistCredit(face.image_credit)

        self._rotate_270()
        self._paintImage(face.image)
        self._paint_side(face.right_side, True)
        self._paint_side(face.left_side, False)
        self._paintDividingLine()
        self._rotate_90()
    
    def _paint_side(self, side: SplitSide, right_side: bool):
        self._paintSplitCost(side.cost, right_side)
        self._paintSplitTitle(side.name, right_side)
        self._paintSplitTypeline(side.type, right_side)
        self._paintSplitOracle(side.oracle, right_side)

    def _get_horizontal_offset(self, right_side: bool) -> int:
        if right_side:
            return int((self.canvas_size[1] - self.ArtistRegion.AreaHeight) / 2) + self.ArtistRegion.AreaHeight + 1
        else:
            return self.ArtistRegion.AreaHeight

    def _paintSplitCost(self, cost:str, right_side: bool):
        if right_side:
            offset = 0
        else:
            offset = self._get_horizontal_offset(True)
        self._paintRightJustifiedText((offset, self.TitleRegion.HeightOffset), cost, self.TitleRegion.AreaHeight, Decoration.BOLD)

    def _paintSplitTitle(self, card_name: str, right_side: bool):
        offset = self._get_horizontal_offset(right_side)
        self._paintWrappedText((offset, self.TitleRegion.HeightOffset), card_name, self._large_text_size(), self.TitleRegion.AreaHeight, Decoration.BOLD)

    def _paintImage(self, image: Image.Image | None = None):
        if not image:
            self._paintSplitImage(None, False)
            self._paintSplitImage(None, True)
            return
        
        new_image_width = int(image.width / 2)
        left_img = image.crop((0, 0, new_image_width, image.height))
        right_img = image.crop((new_image_width, 0, image.width, image.height))
        self._paintSplitImage(left_img, False)
        self._paintSplitImage(right_img, True)

    def _paintSplitImage(self, image: Image.Image | None = None, right_side: bool = False):
        offset = self._get_horizontal_offset(right_side)
        if image is not None:
            im = image
            im = ImageOps.fit(im, (int((self.canvas_size[1] - self.ArtistRegion.AreaHeight) / 2), self.ImageRegion.AreaHeight))
            im = im.convert("1")
            self.draw._image.paste(im, (offset, self.ImageRegion.HeightOffset))
        rectangle = (offset, self.ImageRegion.HeightOffset, 
                     self.canvas_size[1], self.ImageRegion.HeightOffset + self.ImageRegion.AreaHeight)
        self.draw.rectangle(rectangle)
        self._reserveBoundingBox(rectangle)

    def _paintSplitTypeline(self, typeline: str, right_side: bool):
        offset = self._get_horizontal_offset(right_side)
        self._paintWrappedText((offset, self.TypeRegion.HeightOffset), typeline, self._large_text_size(), self.TypeRegion.AreaHeight, Decoration.BOLD)

    def _paintSplitOracle(self, text: str, right_side: bool):
        offset = self._get_horizontal_offset(right_side)
        bbox = self._paintWrappedText((offset, self.TextRegion.HeightOffset), text, self._normal_text_size(), self.TextRegion.AreaHeight)
        self._reserveBoundingBox((offset, self.TextRegion.HeightOffset, bbox[3], self.TextRegion.get_total_offset()))

    def _paintDividingLine(self):
        self.draw.line(((self._get_horizontal_offset(True) - 1, 0), (self._get_horizontal_offset(True) - 1, self.canvas_size[0])))