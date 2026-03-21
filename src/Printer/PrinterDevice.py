from ..MomirVig.MtgCard import MagicCard
from PIL.ImageFile import ImageFile

LEFT = 0
CENTER = 1
RIGHT = 2

class Printer():
    def __init__(self, text_width: int):
        self.max_text_with = text_width

    def _write(self, data: bytes):
        pass

    def _text(self, text: str):
        pass

    def _image(self, image: ImageFile):
        pass

    def _inline_image(self, image: ImageFile, justify_right: bool = False):
        pass

    def _cut(self):
        pass

    def _reset(self):
        pass
    
    def cut(self):
        self._cut()

    def writeLine(self, text: str | None = None):
        if text is None:
            text = ""
        
        for line in self.breakText(text):
            self._text(line)
            self._text("\n")

    def print_card(self, card: MagicCard):
        self._reset()
        if card.face.layout == "normal":
            self._print_normal_card(card)
        else:
            print("not implemented")
            pass

        self.cut()
    
    def _print_normal_card(self, card: MagicCard):
        # card title
        title, remainder = self.textSpan(card.face.name, card.face.cost, True)
        self.writeLine(title)
        self.writeLine(remainder)

        # image
        if card.image is not None:
            self._image(card.image)
        else:
            self._text("----------".center(self.max_text_with))
            self._text("\n\n\n")
            self._text("No Image".center(self.max_text_with))
            self._text("\n\n\n")
            self._text("----------".center(self.max_text_with))
            self.writeLine()

        # type line
        self.writeLine(card.face.type)
        self.writeLine()

        # oracle text
        self.writeLine(card.face.oracle[0])

        # stats & credit
        self.writeLine()
        line, remainder = self.textSpan(card.face.image_credit, card.face.stats[0], True)
        self.writeLine(line)
        self.writeLine(remainder)
        self.writeLine()

    def textSpan(self, left_text: str, right_text: str, right_priority: bool = False) -> tuple[str, str]:
        line: str
        remainder: str
        if not right_priority:
            max_length = self.max_text_with - (len(left_text) + 1)
            right_part, remainder = self.breakLine(right_text, max_length)
            spacing = self.max_text_with - len(left_text)
            line = left_text + right_part.rjust(spacing)
        else:
            max_length = self.max_text_with - (len(right_text) + 1)
            left_part, remainder = self.breakLine(left_text, max_length)
            spacing = self.max_text_with - len(left_part)
            line = left_part + right_text.rjust(spacing)

        return line, remainder

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


    def newLine(self):
        self._text("\n")