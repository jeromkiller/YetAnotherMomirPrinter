from PIL import Image, ImageFont, ImageDraw, ImageText, ImageOps, ImageFile
from ..MomirVig.MtgCard import MagicCard

large_text_size = 20
normal_text_size = 15
tiny_text_size = 10

class CardRegion():
    def __init__(self, HeightOffset: int, AreaHeight: int):
        self.HeightOffset = HeightOffset
        self.AreaHeight = AreaHeight
    
    def get_total_offset(self) -> int: 
        return self.HeightOffset + self.AreaHeight

class PainterBase():
    def __init__(self, canvas_size: tuple[int, int]):
        self.canvas = Image.new("1", canvas_size, color=1)
        self.canvas_size = (canvas_size[0] - 1, canvas_size[1] - 1)
        self.draw = ImageDraw.Draw(self.canvas)

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
        self.BottomRegion = CardRegion(self.canvas_size[1] - (large_text_size + 4), large_text_size + 4)
        text_height = self.BottomRegion.HeightOffset - self.TypeRegion.get_total_offset()
        self.TextRegion = CardRegion(self.TypeRegion.get_total_offset(), text_height)

    def _reset(self):
        self.draw.rectangle([(0, 0), self.canvas_size], fill=1)

    def _paintTitle(self, card_name: str, cost:str):
        card_width = self.canvas_size[0]
        cost_text = ImageText.Text(cost, self.font_large, "1", direction="rtl")
        cost_bb = cost_text.get_bbox()
        name_text = ImageText.Text(card_name, self.font_large, "1")
        name_width = int(card_width - cost_bb[2])
        name_text.wrap(name_width, self.TitleRegion.AreaHeight)

        self.draw.text((0, self.TitleRegion.HeightOffset), name_text)
        self.draw.text((card_width - cost_bb[2], self.TitleRegion.HeightOffset), cost_text)

    def _paintImage(self, card: MagicCard):
        if card.image is not None:
            # For now just put a rectangle in of the right size
            im = card.image
            im = ImageOps.fit(im, (self.canvas_size[0], self.ImageRegion.AreaHeight))
            im = im.convert("1")
            self.draw._image.paste(im, (0, self.ImageRegion.HeightOffset))
        self.draw.rectangle([(0, self.ImageRegion.HeightOffset),
                              (self.canvas_size[0], self.ImageRegion.HeightOffset + self.ImageRegion.AreaHeight)])

    def _paintTypeline(self, typeline: str):
        type_text = ImageText.Text(typeline, self.font_large, "1")
        type_text.wrap(self.canvas_size[0], self.TypeRegion.AreaHeight)
        self.draw.text((0, self.TypeRegion.HeightOffset), type_text)

    def _paintOracle(self, text: str):
        textbox_text = ImageText.Text(text, self.font_normal, "1")
        extra = textbox_text.wrap(self.canvas_size[0], self.TextRegion.AreaHeight)
        if extra:
            textbox_text = ImageText.Text(text, self.font_small, "1")
            extra = textbox_text.wrap(self.canvas_size[0], self.TextRegion.AreaHeight)
        if extra:
            textbox_text = ImageText.Text(text, self.font_tiny, "1")
            textbox_text.wrap(self.canvas_size[0], self.TextRegion.AreaHeight)
        self.draw.text((0, self.TextRegion.HeightOffset), textbox_text)

    def _paintBottom(self, image_credit: str, stats: str):
        if len(stats) > 0:
            stats_text = ImageText.Text(stats, self.font_large, "1")
            stats_bbox = stats_text.get_bbox()
            pt_box = (stats_bbox[2] + 20, self.BottomRegion.AreaHeight)
            pt_origin = (self.canvas_size[0] - pt_box[0], self.BottomRegion.HeightOffset)
            pt_other_corner = (pt_origin[0] + pt_box[0], pt_origin[1] + pt_box[1])
            self.draw.rounded_rectangle((pt_origin, pt_other_corner), 6)
            self.draw.text((pt_origin[0] + 10, pt_origin[1] + 3), stats_text)

        artist_text = ImageText.Text("Artist: " + image_credit, self.font_small, "1")
        artist_bbox = artist_text.get_bbox()
        self.draw.text((0, self.canvas_size[1] - artist_bbox[3]), artist_text)

    