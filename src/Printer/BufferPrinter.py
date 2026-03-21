from . import PrinterDevice

class BufferPrinter(PrinterDevice.Printer):
    def __init__(self, width: int = 42):
        super().__init__(width)
        self.buffer = list[str]()

    def clear_buffer(self):
        self.buffer.clear()

    def get_buffer(self):
        return self.buffer

    def _write(self, data):
        self.buffer.append(data)

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
        self.clear_buffer()
