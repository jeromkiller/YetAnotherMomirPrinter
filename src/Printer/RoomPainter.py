from .PainterBase import *
from .ReminderSplitPainter import ReminderSplitPainter

class RoomPainter(ReminderSplitPainter):
    def __init__(self, canvas_size: tuple[int, int]):
        super().__init__(canvas_size)
        self.ExplainerRegion = CardRegion(self.TypeRegion.get_total_offset(), normal_text_size * 2)
        self.TextRegion = CardRegion(self.ExplainerRegion.get_total_offset() + 2, self.canvas_size[0] - (self.ExplainerRegion.get_total_offset() + 2))

    def _paint_explainer_divider(self):
        #top_line_height = self.ExplainerRegion.HeightOffset - 2
        bottom_line_height = self.ExplainerRegion.get_total_offset()

        #self.draw.line([(self.ArtistRegion.AreaHeight, top_line_height), (self.canvas_size[1], top_line_height)])
        self.draw.line([(self.ArtistRegion.AreaHeight, bottom_line_height), (self.canvas_size[1], bottom_line_height)])

    def _paintDividingLine(self):
        self.draw.line(((self._get_horizontal_offset(True) - 1, 0), (self._get_horizontal_offset(True) - 1, self.ImageRegion.get_total_offset())))
        self.draw.line(((self._get_horizontal_offset(True) - 1, self.ExplainerRegion.get_total_offset() + 1), (self._get_horizontal_offset(True) - 1, self.canvas_size[0])))
