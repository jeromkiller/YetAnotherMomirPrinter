from .PainterBase import *
from .ReminderSplitPainter import ReminderSplitPainter

class FusePainter(ReminderSplitPainter):
    def __init__(self, canvas_size: tuple[int, int]):
        super().__init__(canvas_size)
        self.ExplainerRegion = CardRegion(self.canvas_size[0] - self._normal_text_size(), self._normal_text_size())
        self.TextRegion.AreaHeight = self.TextRegion.AreaHeight - (self.ExplainerRegion.AreaHeight + 1)

    def _paint_explainer_divider(self):
        line_height = self.ExplainerRegion.HeightOffset - 2
        self.draw.line([(self.ArtistRegion.AreaHeight, line_height), (self.canvas_size[1], line_height)])

    def _paintDividingLine(self):
        self.draw.line(((self._get_horizontal_offset(True) - 1, 0), (self._get_horizontal_offset(True) - 1, self.ExplainerRegion.HeightOffset - 2)))
        self.draw.line(((self._get_horizontal_offset(True) - 1, self.ExplainerRegion.get_total_offset() + 1), (self._get_horizontal_offset(True) - 1, self.canvas_size[0])))
