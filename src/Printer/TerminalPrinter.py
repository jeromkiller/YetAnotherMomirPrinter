from . import PrinterDevice

class TerminalPrinter(PrinterDevice.Printer):
    def __init__(self, width: int = 42):
        super().__init__(width)

    def _write(self, data: str):
        print(data, end="")

    def _cut(self):
        self._write("\n--------- cutline ---------\n")

    def _image(self, image):
        self._write("----------".center(self.max_text_with))
        self._write("\n\n\n")
        self._write("No Image".center(self.max_text_with))
        self._write("\n\n\n")
        self._write("----------".center(self.max_text_with))
        self.writeLine()

    def _reset(self):
        self._write("\n\033[0m")
