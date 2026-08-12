from ..MomirVig.MtgCard import MeldFace, MeldPlaneswalkerFace

from .PainterBase import *
from .StandardPainter import StandardPainter
from .PlaneswalkerPainter import PlaneswalkerPainter
from PIL import Image

class MeldPicturePainter(StandardPainter):
    def __init__(self, canvas_size: tuple[int, int]):
        super().__init__(canvas_size)
        self.ImageRegion = CardRegion(self.TitleRegion.get_total_offset(), self.canvas_size[0] - self.TitleRegion.get_total_offset())

    def _huge_text_size(self) -> int:
        return super()._huge_text_size() * 2

    def _large_text_size(self) -> int:
        return super()._large_text_size() * 2
    
    def _normal_text_size(self) -> int:
        return super()._normal_text_size() * 2
    
    def _small_text_size(self) -> int:
        return super()._small_text_size() * 2
    
    def paint_meld_face(self, face: MeldPlaneswalkerFace | MeldFace):
        self._rotate_270()
        self._paintTitle(face.name)
        self._paintImage(face.image)
        self._rotate_90()

    def _paintImage(self, image: Image.Image | None = None):
        if image is not None:
            im = image
            im = ImageOps.fit(im, (self.canvas_size[1], self.ImageRegion.AreaHeight))
            im = im.convert("1")
            self.draw._image.paste(im, (0, self.ImageRegion.HeightOffset))
        rectangle = (0, self.ImageRegion.HeightOffset, 
                     self.canvas_size[0], self.ImageRegion.HeightOffset + self.ImageRegion.AreaHeight)
        self.draw.rectangle(rectangle)
        self._reserveBoundingBox(rectangle)

class MeldTextPainter(PlaneswalkerPainter):
    def __init__(self, canvas_size: tuple[int, int]):
        super().__init__(canvas_size)
        self.TypeRegion.HeightOffset = 0
        self.ArtistRegion = CardRegion(self.canvas_size[0] - self._small_text_size(), self._small_text_size())
        self.StatsRegion = CardRegion(self.canvas_size[0] - self._huge_text_size() + 2, self._huge_text_size())
        self.TextRegion = CardRegion(self.TypeRegion.get_total_offset(), self.ArtistRegion.HeightOffset - self.TypeRegion.get_total_offset())
        
    def _huge_text_size(self) -> int:
        return super()._huge_text_size() * 2

    def _large_text_size(self) -> int:
        return super()._large_text_size() * 2
    
    def _normal_text_size(self) -> int:
        return int(super()._normal_text_size() * 1.5)
    
    def _small_text_size(self) -> int:
        return super()._small_text_size() * 2
    
    def _ability_arrow_size(self) -> int:
        return super()._ability_arrow_size() * 2
    
    def _ability_cost_width(self) -> int:
        return super()._ability_cost_width() * 2
    
    def _ability_cost_height(self) -> int:
        return super()._ability_cost_height() + 4

    def paint_meld_face(self, face: MeldPlaneswalkerFace | MeldFace):
        self._rotate_270()
        self._paintArtistCredit(face.image_credit)
        self._paintTypeline(face.type)

        if isinstance(face, MeldPlaneswalkerFace):
            self._paintLoyalty("  " + face.loyalty + "  ")
            self._paintPlaneswalkerAbilities(face.abilities)
        elif isinstance(face, MeldFace):
            self._paintStats(face.stats, self.StatsRegion.HeightOffset)
            self._paintOracle(face.oracle)
        self._rotate_90()


class MeldPainter():
    def __init__(self, canvas_size: tuple[int, int]):
        self.canvas_size = canvas_size

    def paint_card(self, face: MeldFace | MeldPlaneswalkerFace, front_side_name: str) -> Image.Image:
        painter: PainterBase | None = None
        if face.text_side == front_side_name:
            painter = MeldTextPainter(self.canvas_size)
        else: 
            painter = MeldPicturePainter(self.canvas_size)
        assert painter

        painter.paint_meld_face(face)
        return painter.canvas

