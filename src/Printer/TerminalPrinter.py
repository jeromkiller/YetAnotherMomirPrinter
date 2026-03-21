from . import PrinterDevice

class TerminalPrinter(PrinterDevice.Printer):
    def __init__(self, width: int = 42):
        super().__init__(width)

    def _write(self, data):
        print(data, end="")

    def _text(self, text: str):
        self._write(text)

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
