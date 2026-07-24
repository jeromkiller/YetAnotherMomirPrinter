from .PainterBase import *
from ..MomirVig.MtgCard import MagicCard

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

    def paint_card(self, card: MagicCard):
        assert card.face.layout == "saga"

        self._paintArtistCredit(card.face.image_credit)

        self._paintCost(card.face.cost)
        self._paintTitle(card.face.name)
        self._paintImage(card)
        self._paintExplainer(card.face.oracle[0])
        self._paintSagaText(card.face.oracle[1:])
        self._paintTypeline(card.face.type)

    def _paintImage(self, card: MagicCard):
        image_start = (int(self.canvas_size[0] / 2), self.ImageRegion.HeightOffset)
        image_size = (int(self.canvas_size[0] / 2), self.ImageRegion.AreaHeight)
        
        if card.image is not None:
            im = card.image
            im = ImageOps.fit(im, (image_size))
            im = im.convert("1")
            self.canvas.paste(im, (image_start))
        rectangle = (image_start[0], image_start[1], image_start[0] + image_size[0], image_start[1] + image_size[1])
        self.draw.rectangle(rectangle)
        self._reserveBoundingBox(rectangle)

    def _paintExplainer(self, explainer_text: str):
        explainer_bbox = self._paintWrappedText((0, self.ExplainerRegion.HeightOffset), explainer_text, normal_text_size, self.ExplainerRegion.AreaHeight)
        self.SagaTextRegion = CardRegion(int(explainer_bbox[3]), int(self.TypeRegion.HeightOffset - explainer_bbox[3]))

    def _paintSagaText(self, saga_text: list[str]):
        saga_steps = list[list[str]]()
        saga_texts = list[str]()
        for t in saga_text:
            if "—" not in t:
                break
            parts = t.split(" — ", 1)
            levels = list(parts[0].split(", "))
            saga_steps.append(levels)
            saga_texts.append(parts[1])
        
        combined_text = "\n---\n".join(saga_texts)
        wrapped_text = self._wrapAndResizeText((27, self.SagaTextRegion.HeightOffset), combined_text, normal_text_size, self.SagaTextRegion.AreaHeight)
        
        # Right now I'm hoping there aren't any sagas that puts me in a situation where text has to shrink to fit.
        # and also individual boxes aren't tall enough to fit its multiple level markers
        height = self.SagaTextRegion.HeightOffset
        for i, text in enumerate(wrapped_text.text.split("---")):
            # paint the text
            wrapped_text.text = text
            text_bbox = self._paintText((27, height), wrapped_text)
            
            #paint the level bubble
            last_level_bubble_height = 0
            for j, level in enumerate(saga_steps[i]):
                bubble_size = large_text_size + 4
                bubble_radius = int(bubble_size / 2)
                bubble_pos = [bubble_radius, (height + bubble_radius + (bubble_size * j))]

                # push the text bubble down a little if we start with a newline
                if text[0] == "\n":
                    font_size = int(wrapped_text.font.size)
                    bubble_pos[1] += font_size
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
            if i < len(saga_steps) - 1:
                self.draw.line((10, height, int(self.canvas_size[0] / 2) - 10, height))

