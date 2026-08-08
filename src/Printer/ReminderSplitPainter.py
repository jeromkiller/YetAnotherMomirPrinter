from .PainterBase import *
from .SplitPainter import SplitPainter, SplitCard
from ..MomirVig.MtgCard import ReminderSplitCard
from typing import overload

class ReminderSplitPainter(SplitPainter):
    def __init__(self, canvas_size: tuple[int, int]):
        super().__init__(canvas_size)
        self.ExplainerRegion: CardRegion = CardRegion(0, 0)
    
    @overload
    def paint_card(self, face: ReminderSplitCard): ...

    @overload
    def paint_card(self, face: SplitCard): ...

    def paint_card(self, face: ReminderSplitCard | SplitCard):
        if not isinstance(face, ReminderSplitCard):
            self.paint_card(face)
            return
        
        self._rotate_270()
        self._paint_explainer(face.reminder)
        self._paint_explainer_divider()
        self._rotate_90()
        super().paint_card(face)

    def _paint_explainer(self, text: str):
        self._paintWrappedText((self._get_horizontal_offset(False), self.ExplainerRegion.HeightOffset), text, normal_text_size, self.ExplainerRegion.AreaHeight)

    def _paint_explainer_divider(self):
        pass

    def _paintDividingLine(self):
        pass