from .PainterBase import *
from .VerticalArtPainter import VerticalImagePainter
from ..MomirVig.MtgCard import CaseFace

class CasePainter(VerticalImagePainter):
    def __init__(self, canvas_size: tuple[int, int]):
        super().__init__(canvas_size)
        self.leftSideText = False

    def paint_card(self, face: CaseFace):
        self._paintArtistCredit(face.image_credit)

        self._paintCost(face.cost)
        self._paintTitle(face.name)
        self._paintImage(face.image)
        self._paintCaseText(face.case_stages)
        self._paintTypeline(face.type)

    def _paintCaseText(self, case_stages: list[str]):
        offset = self._getTextOffset()
        text_size = self._findTextSize(case_stages, offset)

        # Right now I'm hoping there aren't any sagas that puts me in a situation where text has to shrink to fit.
        # and also individual boxes aren't tall enough to fit its multiple level markers
        height = self.TextRegion.HeightOffset
        for i, section in enumerate(case_stages):
            # paint the text
            text = section
            wrapped_text = self._wrapAndResizeText((offset, height), text, text_size, self.TypeRegion.HeightOffset - height)
            text_bbox = self._paintText((offset, height), wrapped_text)
            
            height = text_bbox[3]
            # if this wasn't the last text box draw a vertical line in between the text boxes
            if i < len(case_stages) - 1:
                self.draw.line((offset + 7, height + (text_size / 2), offset + self._getImageWidth() - 10, height + (text_size / 2)))
