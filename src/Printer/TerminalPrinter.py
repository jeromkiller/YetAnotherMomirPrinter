from . import PrinterDevice

class TerminalPrinter(PrinterDevice.Printer):
    def __init__(self, width: int = 42):
        super().__init__(width)

    def _write(self, data: str):
        print(data, end="")

    def _cut(self):
        self._write("\n--------- cutline ---------")
