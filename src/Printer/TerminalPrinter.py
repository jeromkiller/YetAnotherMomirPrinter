from . import PrinterDevice
from .TextDecorators import Decoration

class TerminalPrinter(PrinterDevice.Printer):
    def __init__(self, width: int = 42):
        super().__init__(width)

    def _write(self, data):
        print(data, end="")

    def _text(self, text: str, decoration: Decoration | None = None):
        self.print_decoration(decoration)
        print(text, end="")

    def _cut(self):
        self._text("\n--------- cutline ---------\n")

    def _image(self, image):
        self._text("----------".center(self.max_text_with))
        self._text("\n\n\n")
        self._text("No Image".center(self.max_text_with))
        self._text("\n\n\n")
        self._text("----------".center(self.max_text_with))
        self.writeLine()

    def _reset(self):
        self._text("\n\033[0m")

    def print_decoration(self, decoration: Decoration | None = None):
        if decoration is None:
            print("\u001b[22m", end="")
            print("\u001b[24m", end="")
            return

        if Decoration.BOLD in decoration:
            print("\u001b[1m", end="")
        else:
            print("\u001b[22m", end="")
        
        if Decoration.UNDERLINE in decoration:
            print("\u001b[4m", end="")
        else:
            print("\u001b[24m", end="")
