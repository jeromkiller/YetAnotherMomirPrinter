from .PainterBase import *
from .SplitPainter import SplitPainter, SplitFace
from ..MomirVig.MtgCard import ReminderSplitFace
from typing import overload

class ReminderSplitPainter(SplitPainter):
    def __init__(self, canvas_size: tuple[int, int]):
        super().__init__(canvas_size)
        self.ExplainerRegion: CardRegion = CardRegion(0, 0)
    
    @overload
    def paint_card(self, face: ReminderSplitFace): ...

    @overload
    def paint_card(self, face: SplitFace): ...

    def paint_card(self, face: ReminderSplitFace | SplitFace):
        if not isinstance(face, ReminderSplitFace):
            self.paint_card(face)
            return
        
        self._rotate_270()
        self._paint_explainer(face.reminder)
        self._paint_explainer_divider()
        self._rotate_90()
        super().paint_card(face)

    def _paint_explainer(self, text: str):
        self._paintWrappedText((self._get_horizontal_offset(False), self.ExplainerRegion.HeightOffset), text, self._normal_text_size(), self.ExplainerRegion.AreaHeight)

    def _paint_explainer_divider(self):
        pass

    def _paintDividingLine(self):
        pass