from .PainterBase import *
from ..MomirVig.MtgCard import SagaFace, SagaSection
from PIL.ImageFont import FreeTypeFont

class SagaPainter(PainterBase):
    def __init__(self, canvas_size: tuple[int, int]):
        super().__init__(canvas_size)
        self.leftSideText = False
        saga_text_height = int(self.canvas_size[1] - self.TitleRegion.AreaHeight - self.TypeRegion.AreaHeight - self.ArtistRegion.AreaHeight)
        image_height = saga_text_height
        self.ExplainerRegion = CardRegion(self.TitleRegion.get_total_offset(), saga_text_height)
        self.SagaTextRegion = CardRegion(self.TitleRegion.get_total_offset(), saga_text_height)
        self.ImageRegion = CardRegion(self.TitleRegion.get_total_offset(), image_height)
        self.TypeRegion = CardRegion(self.SagaTextRegion.get_total_offset(), large_text_size)

    def paint_card(self, face: SagaFace):
        self._paintArtistCredit(face.image_credit)

        self._paintCost(face.cost)
        self._paintTitle(face.name)
        self._paintImage(face.image)
        self._paintExplainer(face.explainer)
        self._paintSagaText(face.saga_sections)
        self._paintTypeline(face.type)

    def _paintImage(self, image: Image.Image | None = None):
        image_start = (int(self.canvas_size[0] / 2), self.ImageRegion.HeightOffset)
        image_size = (int(self.canvas_size[0] / 2), self.ImageRegion.AreaHeight)
        
        if image is not None:
            im = image
            im = ImageOps.fit(im, (image_size))
            im = im.convert("1")
            self.canvas.paste(im, (image_start))
        rectangle = (image_start[0], image_start[1], image_start[0] + image_size[0], image_start[1] + image_size[1])
        self.draw.rectangle(rectangle)
        self._reserveBoundingBox(rectangle)

    def _paintExplainer(self, explainer_text: str):
        explainer_bbox = self._paintWrappedText((0, self.ExplainerRegion.HeightOffset), explainer_text, normal_text_size, self.ExplainerRegion.AreaHeight)
        self.SagaTextRegion = CardRegion(int(explainer_bbox[3] + 1), int(self.TypeRegion.HeightOffset - explainer_bbox[3] + 1))

    def _paintSagaText(self, sections: list[SagaSection]):
        # test wrap the text
        combined_text = "\n---\n".join([s.oracle for s in sections])
        wrapped_text = self._wrapAndResizeText((27, self.SagaTextRegion.HeightOffset), combined_text, normal_text_size, self.SagaTextRegion.AreaHeight)
        assert isinstance(wrapped_text.font, FreeTypeFont)
        text_size = int(wrapped_text.font.size)

        # Right now I'm hoping there aren't any sagas that puts me in a situation where text has to shrink to fit.
        # and also individual boxes aren't tall enough to fit its multiple level markers
        height = self.SagaTextRegion.HeightOffset
        for i, section in enumerate(sections):
            # paint the text
            text = section.oracle
            wrapped_text = self._wrapAndResizeText((27, height), text, text_size, self.TypeRegion.HeightOffset - height)
            text_bbox = self._paintText((27, height), wrapped_text)
            
            #paint the level bubble
            last_level_bubble_height = 0
            for j, level in enumerate(section.levels):
                bubble_size = large_text_size + 4
                bubble_radius = int(bubble_size / 2)
                bubble_pos = [bubble_radius, (height + bubble_radius + (bubble_size * j))]

                self.draw.circle(bubble_pos, bubble_radius)

                #todo: in the future, see if I can center the bubbles, either by moving the bubble or moving the text block
                
                level_text_height = height + large_text_size + bubble_size * j - 3
                level_text = self._wrapAndResizeText((0, level_text_height), level, large_text_size, large_text_size, Decoration.BOLD)
                level_text_bbox = level_text.get_bbox()
                level_text_pos = (bubble_pos[0] - int((level_text_bbox[2] - level_text_bbox[0]) / 2), bubble_pos[1] - bubble_radius + 4)
                self._paintText(level_text_pos, level_text)
                last_level_bubble_height = bubble_pos[1] + bubble_radius

            height = int(max(text_bbox[3], last_level_bubble_height))
            # if this wasn't the last text box draw a vertical line in between the text boxes
            if i < len(sections) - 1:
                self.draw.line((10, height + (text_size / 2), int(self.canvas_size[0] / 2) - 10, height + (text_size / 2)))
            if (last_level_bubble_height > text_bbox[3]):
                height += text_size

