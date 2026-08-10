from .PainterBase import *
from .VerticalArtPainter import VerticalImagePainter
from ..MomirVig.MtgCard import ClassFace, ClassSection

class ClassPainter(VerticalImagePainter):
    def __init__(self, canvas_size: tuple[int, int]):
        super().__init__(canvas_size)
        self.leftSideText = False

    def paint_card(self, face: ClassFace):
        self._paintArtistCredit(face.image_credit)

        self._paintCost(face.cost)
        self._paintTitle(face.name)
        self._paintImage(face.image)
        self._paintClassText(face.level_sections)
        self._paintTypeline(face.type)

    def _paintClassText(self, class_stages: list[str | ClassSection]):
        combined_text: list[str] = list()
        for section in class_stages:
            if isinstance(section, ClassSection):
                combined_text.append(section.level)
                combined_text.append(section.oracle)
            else:
                combined_text.append(section)
        
        offset = self._getTextOffset()
        text_size = self._findTextSize(combined_text, offset)

        height: int = self.TextRegion.HeightOffset
        for i, section in enumerate(class_stages):
            if isinstance(section, ClassSection):
                # draw the level separator
                line_height = height - (text_size / 2)
                arrow_width = 20
                line_center = (offset + 7) + (((offset + self._getImageWidth() - 10) - (offset + 7)) / 2)
                line_points = [(offset + 7, line_height), (line_center - (arrow_width / 2), line_height), (line_center, line_height + (arrow_width / 2)), (line_center + (arrow_width / 2), line_height), ((offset + self._getImageWidth() - 10), line_height)]
                start_point = line_points[0]
                for next_point in line_points[1:]:
                    self.draw.line((start_point, next_point))
                    start_point = next_point

                #self.draw.line((offset + 7, height - (text_size / 2), offset + self._getImageWidth() - 10, height - (text_size / 2)))
                self._paintRightJustifiedText((0, height), section.level, text_size, Decoration.BOLD)
                self._paintWrappedText((offset, height), section.cost, text_size, text_size, Decoration.BOLD)
                height += text_size * 2
                self.draw.line((offset + 7, height - (text_size / 2), offset + self._getImageWidth() - 10, height - (text_size / 2)))
                text_bbox = self._paintWrappedText((offset, height), section.oracle, text_size, self.TextRegion.AreaHeight)
                height = int(text_bbox[3]) + text_size
            else:
                if i != 0:
                    self.draw.line((offset + 7, height - (text_size / 2), offset + self._getImageWidth() - 10, height - (text_size / 2)))

                wrapped_text = self._wrapAndResizeText((offset, height), section, text_size, self.TypeRegion.HeightOffset - height)
                text_bbox = self._paintText((offset, height), wrapped_text)
            
                height = int(text_bbox[3]) + text_size
                
