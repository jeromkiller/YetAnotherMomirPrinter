from PIL import Image

from .PainterBase import *
from ..MomirVig.MtgCard import PlaneswalkerFace, PlaneswalkerAbilityBlock

class PlaneswalkerPainter(PainterBase):
    def __init__(self, canvas_size: tuple[int, int]):
        super().__init__(canvas_size)
        self._ResizeImageRegion(235)
    
    def _ability_arrow_size(self) -> int:
        return 5
    
    def _ability_cost_width(self) -> int:
        return 35
    
    def _ability_cost_height(self) -> int:
        return self._large_text_size() + 4

    def paint_card(self, face:PlaneswalkerFace):
        self._paintCost(face.cost)
        self._paintTitle(face.name)
        self._paintImage(face.image)
        self._paintTypeline(face.type)
        self._paintLoyalty("  " + face.loyalty + "  ")
        self._paintPlaneswalkerAbilities(face.abilities)

        self._paintArtistCredit(face.image_credit)

    def _ResizeImageRegion(self, new_image_height: int):
        self.ImageRegion.AreaHeight = new_image_height
        self.TypeRegion.HeightOffset = self.ImageRegion.get_total_offset()
        self.TextRegion = CardRegion(self.TypeRegion.get_total_offset(), self.ArtistRegion.HeightOffset - self.TypeRegion.get_total_offset())

    def _paintImage(self, image: Image.Image | None = None):
        if image is not None:
            image = ImageOps.contain(image, (self.canvas_size[0], self.canvas_size[1]))
            self._ResizeImageRegion(image.height)
        super()._paintImage(image)

    def _paintPlaneswalkerAbilities(self, abilities: list[str | PlaneswalkerAbilityBlock]):
        ability_height = int(self.TextRegion.AreaHeight / len(abilities))
        first = True
        for i, ability in enumerate(abilities):
            height_offset = ability_height * i + self.TextRegion.HeightOffset
            if isinstance(ability, PlaneswalkerAbilityBlock):
                self._paintLoyaltyAbility(ability, height_offset, ability_height)
            else:
                self._paintWrappedText((0, height_offset), ability, self._normal_text_size(), ability_height)
            
            if first:
                first = False
            else:
                self.draw.line(((0, height_offset - 2), (self.canvas_size[1], height_offset - 2)))

    def _paintLoyaltyAbility(self, ability: PlaneswalkerAbilityBlock, height_offset: int, height: int):
        self._paintAbilityCost(ability.cost, height_offset, height)
        self._paintWrappedText((self._ability_cost_width() + 3, height_offset), ability.oracle, self._normal_text_size(), height)

    def _paintAbilityCost(self, cost: int, height_offset: int, ability_height: int):
        if cost > 0:
            self._paintUpArrow(cost, height_offset, ability_height)
        elif cost < 0:
            self._paintDownArrow(cost, height_offset, ability_height)
        else:
            self._paintNoCostArrow(height_offset, ability_height)

    def _paintUpArrow(self, cost: int, height_offset: int, ability_height: int):
        height = ability_height - (self._ability_arrow_size() * 2)
        height = min(self._ability_cost_height(), height)

        box = (0, height_offset + self._ability_arrow_size(), self._ability_cost_width(), height_offset + self._ability_arrow_size() + height)
        self.draw.polygon([(box[0], box[1]), (box[0] + self._ability_cost_width() / 2, height_offset), (box[2], box[1]),
                           (box[2], box[3]), (box[0], box[3])])
        text = self._wrapAndResizeText((0, box[1]), f"+{cost}", height, self._large_text_size(), Decoration.BOLD)
        self._paintCenteredText(text, box)
        
    def _paintDownArrow(self, cost: int, height_offset: int, ability_height: int):
        height = ability_height - (self._ability_arrow_size() * 2)
        height = min(self._ability_cost_height(), height)

        box = (0, height_offset + self._ability_arrow_size(), self._ability_cost_width(), height_offset + self._ability_arrow_size() + height)
        self.draw.polygon([(box[0], box[1]), (box[2], box[1]),
                           (box[2], box[3]), (box[0] + self._ability_cost_width() / 2, box[3] + self._ability_arrow_size()), (box[0], box[3])])
        text = self._wrapAndResizeText((0, box[1]), str(cost), height, self._large_text_size(), Decoration.BOLD)
        self._paintCenteredText(text, box)

    def _paintNoCostArrow(self, height_offset: int, ability_height: int):
        height = ability_height - (self._ability_arrow_size() * 2)
        height = min(self._ability_cost_height(), height)

        box = (0, height_offset + self._ability_arrow_size(), self._ability_cost_width(), height_offset + self._ability_arrow_size() + height)
        self.draw.rectangle(box)

        text = self._wrapAndResizeText((0, box[1]), "0", height, self._large_text_size(), Decoration.BOLD)
        self._paintCenteredText(text, box)

    def _paintCenteredText(self, text: ImageText.Text, outside_bbox: tuple[float, float, float, float]):
        text_bbox = text.get_bbox()
        offsets = self._calcCenteringOffset(text_bbox, outside_bbox)
        self._paintText((int(text_bbox[0] + offsets[0]), int(text_bbox[1] + offsets[1])), text)

    def _calcCenteringOffset(self, text_bbox: tuple[float, float, float, float], box_bbox: tuple[float, float, float, float]) -> tuple[float, float]:
        outside_width = box_bbox[2] - box_bbox[0]
        outside_height = box_bbox[3] - box_bbox[1]
        inside_width = text_bbox[2] - text_bbox[0]
        inside_height = text_bbox[3] - text_bbox[1]
        horizontal_offset = ((outside_width - inside_width) / 2) + box_bbox[0]
        vertical_offset = ((outside_height - inside_height) / 2) + box_bbox[1]
        return horizontal_offset, vertical_offset

    def _paintLoyalty(self, loyalty: str):
        self._paintStats(loyalty, self.StatsRegion.HeightOffset)