from PIL import Image, ImageDraw
from ..MomirVig.MtgCard import *
from .StandardPainter import StandardPainter
from .FlipPainter import FlipPainter
from .LevelerPainter import LevelerPainter
from .SagaPainter import SagaPainter
from .SagaCreaturePainter import SagaCreaturePainter
from .PreparedPainter import PreparedPainter
from .PrototypePainter import PrototypePainter
from .AdventurePainter import AdventurePainter
from .PlaneswalkerPainter import PlaneswalkerPainter
from .SplitPainter import SplitPainter
from .FusePainter import FusePainter
from .RoomPainter import RoomPainter
from .AftermathPainter import AftermathPainter
from .BattlePainter import BattlePainter
from .CasePainter import CasePainter

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
        canvas = self.paint_face(card.front_face)
        if card.back_face:
            front_face = canvas
            back_face = self.paint_face(card.back_face)
            canvas = Image.new("1", (self.canvas_size[0] * 2 + 40, self.canvas_size[1]), color=1) #canvas.crop((0, 0, card_width * 2 + 40, canvas.height)
            canvas.paste(front_face, (0, 0))
            canvas.paste(back_face, (canvas.width - back_face.width, 0))
            draw = ImageDraw.Draw(canvas)
            draw.line([(front_face.width + 20, 0), (front_face.width + 20, front_face.height)])

        return canvas

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
        elif isinstance(face, CaseFace):
            painter = CasePainter(self.canvas_size)
            painter.paint_card(face)
            return painter.canvas
        elif isinstance(face, PrepareFace):
            painter = PreparedPainter(self.canvas_size)
            painter.paint_card(face)
            return painter.canvas
        elif isinstance(face, AdventureFace):
            painter = AdventurePainter(self.canvas_size)
            painter.paint_card(face)
            return painter.canvas
        elif isinstance(face, PrototypeFace):
            painter = PrototypePainter(self.canvas_size)
            painter.paint_card(face)
            return painter.canvas
        elif isinstance(face, PlaneswalkerFace):
            painter = PlaneswalkerPainter(self.canvas_size)
            painter.paint_card(face)
            return painter.canvas
        elif isinstance(face, SplitFace):
            if isinstance(face, AftermathFace):
                painter = AftermathPainter(self.canvas_size)
                painter.paint_card(face)
                return painter.canvas
            elif isinstance(face, FuseFace):
                painter = FusePainter(self.canvas_size)
                painter.paint_card(face)
                return painter.canvas
            elif isinstance(face, RoomFace):
                painter = RoomPainter(self.canvas_size)
                painter.paint_card(face)
                return painter.canvas
            else:
                painter = SplitPainter(self.canvas_size)
                painter.paint_card(face)
                return painter.canvas
        elif isinstance(face, BattleFace):
            painter = BattlePainter(self.canvas_size)
            painter.paint_card(face)
            return painter.canvas
        
        raise TypeError
        
