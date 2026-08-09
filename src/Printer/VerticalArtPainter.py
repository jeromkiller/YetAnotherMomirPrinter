from PIL.Image import Image
from PIL.ImageFont import FreeTypeFont

from .PainterBase import *

class VerticalImagePainter(PainterBase):
    def __init__(self, canvas_size: tuple[int, int]):
        super().__init__(canvas_size)
        self.leftSideText = False
        saga_text_height = int(self.canvas_size[1] - self.TitleRegion.AreaHeight - self.TypeRegion.AreaHeight - self.ArtistRegion.AreaHeight)
        image_height = saga_text_height
        self.ExplainerRegion = CardRegion(self.TitleRegion.get_total_offset(), saga_text_height)
        self.TextRegion = CardRegion(self.TitleRegion.get_total_offset(), saga_text_height)
        self.ImageRegion = CardRegion(self.TitleRegion.get_total_offset(), image_height)
        self.TypeRegion = CardRegion(self.TextRegion.get_total_offset(), large_text_size)

    def _getImageWidth(self) -> int:
        return int(self.canvas_size[0] / 2)

    def _getImageOffset(self) -> int:
        if self.leftSideText:
            return self._getImageWidth()
        return 0
    
    def _getTextOffset(self) -> int:
        if self.leftSideText:
            return 0
        return self._getImageWidth() + 2

    def _paintImage(self, image: Image.Image | None = None):
        image_start = (self._getImageOffset(), self.ImageRegion.HeightOffset)
        image_size = (self._getImageWidth(), self.ImageRegion.AreaHeight)
        
        if image is not None:
            im = image
            im = ImageOps.fit(im, (image_size))
            im = im.convert("1")
            self.canvas.paste(im, (image_start))
        rectangle = (image_start[0], image_start[1], image_start[0] + image_size[0], image_start[1] + image_size[1])
        self.draw.rectangle(rectangle)
        self._reserveBoundingBox(rectangle)

    def _paintExplainer(self, explainer_text: str):
        explainer_bbox = self._paintWrappedText((self._getTextOffset(), self.ExplainerRegion.HeightOffset), explainer_text, normal_text_size, self.ExplainerRegion.AreaHeight)
        self.TextRegion = CardRegion(int(explainer_bbox[3] + 1), int(self.TypeRegion.HeightOffset - explainer_bbox[3] + 1))

    def _findTextSize(self, text_sections: list[str], horizontal_offset: int) -> int:
        # test wrap the text
        combined_text = "\n---\n".join(text_sections)
        wrapped_text = self._wrapAndResizeText((horizontal_offset, self.TextRegion.HeightOffset), combined_text, normal_text_size, self.TextRegion.AreaHeight)
        assert isinstance(wrapped_text.font, FreeTypeFont)
        return int(wrapped_text.font.size)