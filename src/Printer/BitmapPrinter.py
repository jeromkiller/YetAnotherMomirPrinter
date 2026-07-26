from PIL import Image, ImageFont, ImageDraw, ImageText, ImageOps, ImageFile
from ..MomirVig.MtgCard import MagicCard
from .StandardPainter import StandardPainter
from .FlipPainter import FlipPainter
from .LevelerPainter import LevelerPainter
from .SagaPainter import SagaPainter
from .SagaCreaturePainter import SagaCreaturePainter
from .PreparedPainter import PreparedPainter

large_text_size = 20
normal_text_size = 15
tiny_text_size = 10

class CardRegion():
    def __init__(self, HeightOffset: int, AreaHeight: int):
        self.HeightOffset = HeightOffset
        self.AreaHeight = AreaHeight
    
    def get_total_offset(self) -> int: 
        return self.HeightOffset + self.AreaHeight

class BitmapPrinter():
    def __init__(self, canvas_size: tuple[int, int]):
        self.canvas_size = (canvas_size[0], canvas_size[1])

    def paint_card(self, card: MagicCard) -> Image.Image:
        #self._reset()
        painter = None
        if card.face.layout == "normal":
            painter = StandardPainter(self.canvas_size)
        elif card.face.layout == "leveler":
            painter = LevelerPainter(self.canvas_size)
        elif card.face.layout == "flip":
            painter = FlipPainter(self.canvas_size)
        elif card.face.layout == "saga":
            painter = SagaPainter(self.canvas_size)
        elif card.face.layout == "saga_creature":
            painter = SagaCreaturePainter(self.canvas_size)
        elif card.face.layout == "prepare":
            painter = PreparedPainter(self.canvas_size)

        if painter is None:
            raise TypeError
        
        painter.paint_card(card)
        return painter.canvas
