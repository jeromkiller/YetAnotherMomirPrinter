from . import PrinterDevice

class BufferPrinter(PrinterDevice.Printer):
    def __init__(self, width: int = 42):
        super().__init__(width)
        self.buffer = list[str]()

    def clear_buffer(self):
        self.buffer.clear()

    def get_buffer(self):
        return self.buffer

    def _write(self, data: str):
        self.buffer.append(data)

    def _cut(self):
        self._write("\n--------- cutline ---------")
