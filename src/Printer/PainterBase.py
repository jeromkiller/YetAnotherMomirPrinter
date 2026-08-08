from PIL import Image, ImageFont, ImageDraw, ImageText, ImageOps
from ..MomirVig.MtgCard import MagicCard
from .TextDecorators import Decoration
from dataclasses import dataclass

large_text_size = 20
normal_text_size = 15
tiny_text_size = 10

@dataclass
class CardRegion():
    HeightOffset: int
    AreaHeight: int
    
    def get_total_offset(self) -> int: 
        return self.HeightOffset + self.AreaHeight

class PainterBase():
    def __init__(self, canvas_size: tuple[int, int]):
        self.canvas = Image.new("1", canvas_size, color=1)
        self.canvas_size = (canvas_size[0] - 1, canvas_size[1] - 1)
        self.draw = ImageDraw.Draw(self.canvas)
        self.obscured_areas: list[tuple[float, float, float, float]] = list()

        # fonts
        self.font_large = ImageFont.truetype("Font/SwanseaBold-D0ox.ttf", size=large_text_size)
        self.font_normal = ImageFont.truetype("Font/Swansea-q3pd.ttf", size=normal_text_size)
        self.font_small = ImageFont.load_default()
        self.font_tiny = ImageFont.truetype("Font/Swansea-q3pd.ttf", size=tiny_text_size)

        # card area sizes
        self.TitleRegion = CardRegion(0, large_text_size)
        # image size is roughly 4:3, 
        image_height = int(self.canvas_size[0] * 3 / 4)
        self.ImageRegion = CardRegion(self.TitleRegion.get_total_offset(), image_height)
        self.TypeRegion = CardRegion(self.ImageRegion.get_total_offset(), large_text_size)
        self.ArtistRegion = CardRegion(self.canvas_size[1] - 10, 10)
        self.StatsRegion = CardRegion(self.canvas_size[1] - large_text_size - 2, large_text_size + 2)
        text_height = self.ArtistRegion.HeightOffset - self.TypeRegion.get_total_offset()
        self.TextRegion = CardRegion(self.TypeRegion.get_total_offset(), text_height)

    def _reset(self):
        self.draw.rectangle([(0, 0), self.canvas_size], fill=1)
        self.obscured_areas = list()

    def _rotate_180(self):
        self.canvas = self.canvas.rotate(180)
        self.draw = ImageDraw.Draw(self.canvas)
        self.obscured_areas = list(map(lambda bbox: (self.canvas_size[0] - bbox[2],
                                                     self.canvas_size[1] - bbox[3],
                                                     self.canvas_size[0] - bbox[0],
                                                     self.canvas_size[1] - bbox[1],), self.obscured_areas))
        
    def _rotate_90(self):
        self.canvas = self.canvas.rotate(90, expand=True)
        self.draw = ImageDraw.Draw(self.canvas)
        self.obscured_areas = list(map(lambda bbox: (bbox[1],
                                                     self.canvas_size[0] - bbox[2],
                                                     bbox[3],
                                                     self.canvas_size[0] - bbox[0],), self.obscured_areas))

    def _rotate_270(self):
        self.canvas = self.canvas.rotate(270, expand=True)
        self.draw = ImageDraw.Draw(self.canvas)
        self.obscured_areas = list(map(lambda bbox: (self.canvas_size[1] - bbox[3],
                                                     bbox[0],
                                                     self.canvas_size[1] - bbox[1],
                                                     bbox[2],), self.obscured_areas))

    def _reserveBoundingBox(self, bbox: tuple[float, float, float, float]):
        self.obscured_areas.append((int(bbox[0]), int(bbox[1]), int(bbox[2]), int(bbox[3])))

    def _paintObscuredAreas(self):
        self.draw.rectangle([(0, 0), self.canvas_size], fill=1)
        for bbox in self.obscured_areas:
            self.draw.rectangle(bbox)

    def _paintWrappedText(self, pos: tuple[int, int], text: str, font_size: int, area_height: int, decor: Decoration | None = None) -> tuple[float, float, float, float]:
        wrapped = self._wrapAndResizeText(pos, text, font_size, area_height, decor)
        return self._paintText(pos, wrapped)

    def _paintText(self, pos: tuple[int, int], text: ImageText.Text) -> tuple[float, float, float, float]:
        self.draw.text(pos, text)
        bbox = text.get_bbox(pos)
        self._reserveBoundingBox(bbox)
        return bbox

    def _paintRightJustifiedText(self, pos: tuple[int, int], text: str, size: int, decor: Decoration | None = None) -> tuple[float, float, float, float]:
        font_path = "Font/Swansea-q3pd.ttf"
        if decor:
            if Decoration.BOLD in decor:
                font_path = "Font/SwanseaBold-D0ox.ttf"
        font = ImageFont.truetype(font_path, size)
        paint_text = ImageText.Text(text, font, "1")
        pos = (self.canvas.width - pos[0] - int(paint_text.get_length()), pos[1])
        return self._paintText(pos, paint_text)

    def _check_obstruction(self, box: tuple[float, float, float, float]) -> bool:
        for obstruction in self.obscured_areas:
            if box[0] <= obstruction[2] and box[2] >= obstruction[0] and \
               box[1] <= obstruction[3] and box[3] >= obstruction[1]:
                return True
        return box[2] > self.canvas.width

    def _wrapText(self, pos: tuple[int, int], string: str, font: ImageFont.BaseImageFont, area_height: int) -> ImageText.Text[str]:
        text_block = ImageText.Text("", font, mode="1")
        text_line = ImageText.Text("", font, mode="1")

        height_offset = pos[1]
        for word in string.split(" "):
            if text_line.text:
                word = " " + word
            text_line.text += word
            line_bbox = text_line.get_bbox((pos[0], height_offset))
            while self._check_obstruction(line_bbox):
                # line too large, or obstructed
                word = word.strip(" ")
                text_line.text = word
                text_block.text += "\n"
                height_offset = text_block.get_bbox(pos)[3] - 1
                if height_offset > pos[1] + area_height:
                    # text block doesn't fit the canvas anymore, we can return now
                    return text_block                
                line_bbox = text_line.get_bbox((pos[0], height_offset))
            else:
                text_block.text += word
        return text_block
    
    def _wrapAndResizeText(self, pos: tuple[int, int], text: str, font_size: int, area_height: int, decor: Decoration | None = None) -> ImageText.Text[str]:
        font_path = "Font/Swansea-q3pd.ttf"
        if decor:
            if Decoration.BOLD in decor:
                font_path = "Font/SwanseaBold-D0ox.ttf"
        
        # try to print the font, shrink if it doesn't fit
        wrapped = None
        for font_size in range(font_size, 9, -1):
            font = ImageFont.truetype(font_path, font_size)
            wrapped = self._wrapText(pos, text, font, area_height)
            if wrapped.get_bbox(pos)[3] < pos[1] + area_height:
                break
        else:
            raise Exception("Text doesn't fit the area") #todo custom exception
        return wrapped

    def _paintTitle(self, card_name: str):
        self._paintWrappedText((0, self.TitleRegion.HeightOffset), card_name, large_text_size, self.TitleRegion.AreaHeight, Decoration.BOLD)

    def _paintCost(self, cost: str):
        self._paintRightJustifiedText((0, self.TitleRegion.HeightOffset), cost, self.TitleRegion.AreaHeight, Decoration.BOLD)

    def _paintStats(self, stats:str, height: int):
        if not stats:
            return
        
        bbox = self._paintRightJustifiedText((5, height), stats, 25, Decoration.BOLD)
        border = (bbox[0] - 4, bbox[1] - 3, bbox[2] + 3, bbox[3] + 3)
        self.draw.rounded_rectangle(border, 6)
        self._reserveBoundingBox(border)

    def _paintImage(self, image: Image.Image | None = None):
        if image is not None:
            im = image
            im = ImageOps.fit(im, (self.canvas_size[0], self.ImageRegion.AreaHeight))
            im = im.convert("1")
            self.draw._image.paste(im, (0, self.ImageRegion.HeightOffset))
        rectangle = (0, self.ImageRegion.HeightOffset, 
                     self.canvas_size[0], self.ImageRegion.HeightOffset + self.ImageRegion.AreaHeight)
        self.draw.rectangle(rectangle)
        self._reserveBoundingBox(rectangle)

    def _paintTypeline(self, typeline: str):
        self._paintWrappedText((0, self.TypeRegion.HeightOffset), typeline, large_text_size, self.TypeRegion.AreaHeight, Decoration.BOLD)

    def _paintOracle(self, text: str):
        self._paintWrappedText((0, self.TextRegion.HeightOffset), text, normal_text_size, self.TextRegion.AreaHeight)

    def _paintArtistCredit(self, credit: str):
        artist_text = ImageText.Text("Artist: " + credit, mode="1")
        self._paintText((0, self.ArtistRegion.HeightOffset), artist_text)
    