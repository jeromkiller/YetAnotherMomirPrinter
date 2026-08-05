from PIL import Image
from ..MomirVig.MtgCard import *
from .StandardPainter import StandardPainter
from .FlipPainter import FlipPainter
from .LevelerPainter import LevelerPainter
from .SagaPainter import SagaPainter
from .SagaCreaturePainter import SagaCreaturePainter
from .PreparedPainter import PreparedPainter
from .PrototypePainter import PrototypePainter

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
        return self.paint_face(card.front_face)
    

    def paint_face(self, face: CardFace) -> Image.Image:
        if isinstance(face, DefaultFace):
            painter = StandardPainter(self.canvas_size)
            painter.paint_card(face)
            return painter.canvas
        elif isinstance(face, LevelerFace):
            painter = LevelerPainter(self.canvas_size)
            painter.paint_card(face)
            return painter.canvas
        elif isinstance(face, FlipFace):
            painter = FlipPainter(self.canvas_size)
            painter.paint_card(face)
            return painter.canvas
        elif isinstance(face, SagaCreatureFace):
            painter = SagaCreaturePainter(self.canvas_size)
            painter.paint_card(face)
            return painter.canvas
        elif isinstance(face, SagaFace):
            painter = SagaPainter(self.canvas_size)
            painter.paint_card(face)
            return painter.canvas
        elif isinstance(face, PrepareFace):
            painter = PreparedPainter(self.canvas_size)
            painter.paint_card(face)
            return painter.canvas
        elif isinstance(face, PrototypeFace):
            painter = PrototypePainter(self.canvas_size)
            painter.paint_card(face)
            return painter.canvas
        
        raise TypeError
        
