from . import PrinterDevice
from .TextDecorators import Decoration

class BufferPrinter(PrinterDevice.Printer):
    def __init__(self, width: int = 42):
        super().__init__(width)
        self.buffer: list[str] = [""]

    def clear_buffer(self):
        self.buffer.clear()

    def get_buffer(self):
        return self.buffer

    def _write(self, data):
        pass

    def _text(self, text: str, decoration: Decoration | None = None):
        for char in text:
            if char == "\n":
                self.buffer.append("")
            else:
                self.buffer[-1] += char

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
        self.clear_buffer()
