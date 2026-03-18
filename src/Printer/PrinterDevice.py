from ..MomirVig.MtgCard import MagicCard
from PIL.ImageFile import ImageFile

LEFT = 0
CENTER = 1
RIGHT = 2

class Printer():
    def __init__(self, text_width: int):
        self.max_text_with = text_width

    def _write(self, data: str):
        pass

    def _image(self, image: ImageFile):
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
            self._write(line)
            self._write("\n")

    def print_card(self, card: MagicCard):
        self._reset()
        if card.face.layout == "normal":
            self._print_normal_card(card)
        else:
            print("not implemented")
            pass
    
    def _print_normal_card(self, card: MagicCard):
        # card title
        title, remainder = self.textSpan(card.face.name, card.face.cost, True)
        self.writeLine(title)
        self.writeLine(remainder)

        # image
        if card.image is not None:
            self._image(card.image)
        else:
            self._write("----------".center(self.max_text_with))
            self._write("\n\n\n")
            self._write("No Image".center(self.max_text_with))
            self._write("\n\n\n")
            self._write("----------".center(self.max_text_with))
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

        if len(line) <= text_width:
            return line, ""
        
        new_line: str = ""
        remainder: str = ""

        # break line on spaces
        for word in line.split(" "):
            # break long words
            if len(word) > text_width:
                if len(new_line):
                    break
                new_line = word[:text_width - 1]
                new_line += "-"
                return new_line, line[len(new_line) - 1:]

            if len(word) + len(new_line) + 1 > text_width:
                break

            if len(new_line) > 0:
                new_line += " "

            new_line += word

        remainder = line[len(new_line) + 1:]
        return new_line, remainder


    def breakText(self, text: str, text_width: int = -1) -> list[str]:
        if text_width < 0:
            text_width = self.max_text_with
        
        if len(text) < text_width:
            return [text]
        
        lines = list[str]()
        broken_line, remainder = self.breakLine(text)
        lines.append(broken_line)
        while len(remainder):
            broken_line, remainder = self.breakLine(remainder)
            lines.append(broken_line)
        return lines


    def newLine(self):
        self._write("\n")