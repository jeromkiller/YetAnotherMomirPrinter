from ..MomirVig.MtgCard import MagicCard
from PIL.ImageFile import ImageFile
from .TextDecorators import Decoration

LEFT = 0
CENTER = 1
RIGHT = 2

TITLE_DECOR = Decoration.BOLD
LEVEL_DECOR = Decoration.BOLD
TYPE_DECOR = Decoration.UNDERLINE
STAT_DECOR = Decoration.BOLD | Decoration.UNDERLINE

class Printer():
    def __init__(self, text_width: int):
        self.max_text_with = text_width

    def _write(self, data: bytes):
        pass

    def _text(self, text: str, decoration: Decoration | None = None):
        pass

    def _image(self, image: ImageFile):
        pass

    def _inline_image(self, image: ImageFile, justify_right: bool = False):
        pass

    def _cut(self):
        pass

    def _reset(self):
        pass

    def _start_page_mode(self):
        pass

    def _end_page_mode_upside_down(self):
        pass

    def _end_page_mode_with_image(self, image: ImageFile):
        pass
    
    def cut(self):
        self._cut()

    def writeLine(self, text: str | None = None, decoration: Decoration | None = None):
        if text is None:
            text = ""
        
        for line in self.breakText(text):
            self._text(line, decoration)
            self._text("\n")

    def print_card(self, card: MagicCard):
        self._reset()
        if card.face.layout == "normal":
            self._print_normal_card(card)
        elif card.face.layout == "leveler":
            self._print_leveler_card(card)
        elif card.face.layout == "flip":
            self._print_flip_card(card)
        elif card.face.layout == "saga":
            self._print_saga_creature(card)
        else:
            print("not implemented")
            pass

        self.cut()
    
    def _print_normal_card(self, card: MagicCard):
        assert card.face.layout == "normal"
        self.printCardTitle(card.face.name, card.face.cost)
        self.printCardImage(card)
        self.writeLine()
        self.printTypeLine(card.face.type)

        # oracle text
        self.writeLine(card.face.oracle[0])

        # stats & credit
        self.writeLine()
        remainder = self.textSpan(card.face.image_credit, card.face.stats[0], True, right_decor=STAT_DECOR)
        self.writeLine(remainder)
        self.writeLine()

    def _print_leveler_card(self, card: MagicCard):
        assert card.face.layout == "leveler"
        self.printCardTitle(card.face.name, card.face.cost)
        self.printCardImage(card)
        self.writeLine()
        self.printTypeLine(card.face.type)

        # oracle text & levels
        stat_len = len(max(card.face.stats, key=lambda l: len(l)))
        oracle_width = self.max_text_with - 1 - stat_len
        self.print_columns([card.face.oracle[0], card.face.stats[0]], [oracle_width, stat_len], [None, STAT_DECOR])
        self.writeLine()
        for i in range(1, len(card.face.oracle)):
            oracle_parts = card.face.oracle[i].split("\n", 1)
            oracle_width = self.max_text_with - 2 - 7 - stat_len
            level = oracle_parts[0]
            oracle = oracle_parts[1] if len(oracle_parts) > 1 else ""
            stats = card.face.stats[i]
            self.print_columns([level, oracle, stats], [7, oracle_width, stat_len], [LEVEL_DECOR, None, STAT_DECOR])
            self.writeLine()

        # credits
        self.writeLine(card.face.image_credit)

    def _print_flip_card(self, card: MagicCard):
        assert card.face.layout == "flip"
        # upright part
        self.printCardTitle(card.face.getFlipName(0), card.face.cost)
        self.writeLine(card.face.oracle[0])
        remainder = self.textSpan(card.face.getFlipType(0), card.face.stats[0], True, TYPE_DECOR, STAT_DECOR)
        self.writeLine(remainder, TYPE_DECOR)

        self.printCardImage(card)

        # flipped part
        self._start_page_mode()
        self.printCardTitle(card.face.getFlipName(1), "")
        self.writeLine(card.face.oracle[1])
        remainder = self.textSpan(card.face.getFlipType(1), card.face.stats[1], True, TYPE_DECOR, STAT_DECOR)
        self.writeLine(remainder, TYPE_DECOR)
        self._end_page_mode_upside_down()

        self.writeLine(card.face.image_credit)

    def _print_saga_creature(self, card: MagicCard):
        assert card.face.layout == "saga"

        self.printCardTitle(card.face.name, card.face.cost)
        self.writeLine(card.face.oracle[0])

        self._start_page_mode()
        for oracle_part in card.face.oracle[1:]:
            if "—" not in oracle_part:
                break
            parts = oracle_part.split(" — ", 1)
            levels = parts[0]
            text = "- " + parts[1]
            self.print_columns([levels, text], [4, 16], [LEVEL_DECOR, None], right_justify_right_column=False)

        self._end_page_mode_with_image(card.image)

        self.printTypeLine(card.face.type)

        if "—" not in card.face.oracle[-1]:
            self.writeLine(card.face.oracle[-1])
            self.writeLine()

        remainder = self.textSpan(card.face.image_credit, card.face.stats[0], True, right_decor=STAT_DECOR)
        self.writeLine(remainder)
        self.writeLine()


    def printCardTitle(self, card_name: str, cost: str):
        remainder = self.textSpan(card_name, cost, True, TITLE_DECOR)
        self.writeLine(remainder, TITLE_DECOR)

    def printCardImage(self, card: MagicCard, ):
        if card.image is not None:
            self._image(card.image)
        else:
            self._text("----------".center(self.max_text_with))
            self._text("\n\n\n")
            self._text("No Image".center(self.max_text_with))
            self._text("\n\n\n")
            self._text("----------".center(self.max_text_with))
            self.writeLine()

    def printTypeLine(self, typeline: str):
        self.writeLine(typeline, TYPE_DECOR)

    def textSpan(self, left_text: str, right_text: str, right_priority: bool = False,
                 left_decor: Decoration | None = None, right_decor: Decoration | None = None) -> str:
        remainder: str
        if not right_priority:
            max_length = self.max_text_with - (len(left_text) + 1)
            right_part, remainder = self.breakLine(right_text, max_length)
            left_part = left_text
        else:
            max_length = self.max_text_with - (len(right_text) + 1)
            left_part, remainder = self.breakLine(left_text, max_length)
            right_part = right_text

        spacing = self.max_text_with - len(left_part) - len(right_part)
        self._text(left_part, left_decor)
        self._text(" " * spacing)
        self._text(right_part, right_decor)
        return remainder

    def breakLine(self, line: str, text_width: int = -1) -> tuple[str, str]:
        if text_width < 0:
            text_width = self.max_text_with

        # if there is a linebreak in the line, only parse the stuff left from it
        if "\n" in line:
            pre_break, partition, post_break = line.partition("\n")
            broken, remainder = self.breakLine(pre_break, text_width)
            if remainder:
                remainder += partition
            return broken, remainder + post_break

        if len(line) <= text_width:
            return line, ""
        
        # check if we can break exactly at the end of line
        if line[text_width] == " ":
            return line[:text_width], line[text_width + 1:]

        # only parse the part that's relevant to us
        check_line = line[:text_width]

        # remove the last word from the back
        trimmed, _, remainder = check_line.rpartition(" ")

        if trimmed == '':
            # couldn't break on a space
            # break the word instead
            return remainder[:-1] + "-", line[len(remainder) - 1:]

        return trimmed, line[len(trimmed) + 1:]


    def breakText(self, text: str, text_width: int = -1) -> list[str]:
        if text_width < 0:
            text_width = self.max_text_with
        
        if len(text) < text_width:
            return [text]
        
        lines = list[str]()
        broken_line, remainder = self.breakLine(text, text_width)
        lines.append(broken_line)
        while len(remainder):
            broken_line, remainder = self.breakLine(remainder, text_width)
            lines.append(broken_line)
        return lines

    def print_columns(self, texts: list[str], column_widths: list[int], decorations: list[Decoration | None] = list(), right_justify_right_column = True):
        if len(texts) != len(column_widths):
            print("Amount of text and amount of columns should be the same")
            return
        
        if sum(column_widths) + len(column_widths) - 1 > self.max_text_with:
            print("Columns combine to be too wide")
            return

        num_columns = len(texts)
        columns = [self.breakText(texts[i], column_widths[i]) for i in range(len(texts))]
        padded_lines = list[list[str]]()

        total_lines = len(max(columns, key=lambda l: len(l)))
        for line_index in range(total_lines):
            new_line = list[str]()
            for i, col in enumerate(columns):
                
                if len(col) <= line_index:
                    #new_line.append(" " * padding)
                    new_line.append("")
                    continue
                else:
                    line = col[line_index]
                    #padding -= len(line)
                    #new_line.append(line + (" " * padding))
                    new_line.append(line)
            padded_lines.append(new_line)


        for row in padded_lines:
            for i, line in enumerate(row):
                decor = None
                if i < len(decorations):
                    decor = decorations[i]

                if i < num_columns - 1:
                    self._text(line, decor)
                    padding = column_widths[i]
                    padding -= len(line)
                    padding += 1
                    self._text(" " * padding)
                else:
                    if right_justify_right_column:
                        padding = column_widths[i]
                        padding -= len(line)
                        self._text(" " * padding)
                    self._text(line, decor)
                    self.newLine()


    def newLine(self):
        self._text("\n")