import usb.core
import usb.util
from . import PrinterDevice
from .TextDecorators import Decoration
from .constants import *
from ..MomirVig import ProcessImage 
from PIL.ImageFile import ImageFile
import numpy as np

vid = 0x04b8
did = 0x0e02
interface=0
in_ep=0x82
out_ep=0x01

class UsbPrinter(PrinterDevice.Printer):
    def __init__(self, vendorId: int = vid, deviceId: int = did):
        super().__init__(42)
        self.vendorId = vendorId
        self.deviceId = deviceId
        self.device = None

        self.open()

    def __del__(self):
        usb.util.dispose_resources(self.device)
        self.device = None

    def open(self):
        self.device = usb.core.find(idVendor=self.vendorId, idProduct=self.deviceId)
        if self.device is None:
            print("USB printer not connected")
            return

        if self.device.is_kernel_driver_active(0):
            try:
                print("Device driver already active, disabeling...")
                self.device.detach_kernel_driver(0)
            except usb.core.USBError as e:
                print("Could not detach kernel driver: %s", str(e))

            try:
                self.device.set_configuration()
                self.device.reset()
            except usb.core.USBError as e:
                    print("Could not reset device: %s", str(e))
            
            self._reset()

    def _write(self, data: bytes):
        self.device.write(out_ep, data, 0)

    def _text(self, text: str, decoration: Decoration | None = None):
        data = text.replace("—", "-")
        self.set_decoration(decoration)
        self._write(data)

    def _cut(self):
        #self._write(FEED_AND_CUT_PARTIAL) # doesn't work??
        self._write(b"\n\n\n\n\n\n")
        self._write(CUT_FULL)

    def _image(self, image: ImageFile):
        self.buffered_image(image)


    def _inline_image(self, image: ImageFile, justify_right: bool = False):
        self._write(SET_IMAGE_SPACING)
        line = self.column_image(image, max_height=24)[0]
        data_len: int = len(line)
        nL = int(data_len % 256)
        nH = int(data_len / 256)
        if justify_right:
            pass    # todo implement
        
        self._write(START_BIT_IMAGE)
        self._write(nL.to_bytes())
        self._write(nH.to_bytes())
        self._write(line)
        self._write(RESET_LINE_SPACING)


    def column_image(self, image: ImageFile, max_width: int | None = None, max_height: int | None = None) -> list[bytearray]:
        dithered = ProcessImage.DitherImage(image, max_width, max_height, negative=True)
        return ProcessImage.toPrintStrings(dithered, 24)


    def buffered_image(self, image: ImageFile):
        dithered = ProcessImage.DitherImage(image, max_width=512, negative=True)
        
        flatrow = dithered.flatten('C')
        byte_data = bytearray(np.packbits(flatrow))

        height = dithered.shape[0]
        width = dithered.shape[1]
        xL = int(width % 256)
        xH = int(width / 256)
        yL = int(height % 256)
        yH = int(height / 256)
        k = int(((xL + xH *256) + 7) /8) * (yL + yH * 256)
        num_bytes = int((height * width) / 8) + 10
        pL = int(num_bytes % 256)
        pH = int(num_bytes / 256)

        b = START_BUFFERED_IMAGE
        b += pL.to_bytes()
        b += pH.to_bytes()
        b += b"\x30\x70"
        b += b"\x30"  # monochrome mode
        b += b"\x01\x01\x31"
        b += xL.to_bytes()
        b += xH.to_bytes()
        b += yL.to_bytes()
        b += yH.to_bytes()
        b += byte_data
        self._write(b)

        # then print it
        self._write(PRINT_BUFFERED_IMAGE)

    def _reset(self):
        self._write(INITIALIZE)    

    def set_decoration(self, decoration: Decoration | None = None):
        if decoration is None:
            self._write(SELECT_PRINT_MODE + b"\x00")
            return
        
        flags = 0
        if Decoration.BOLD in decoration:
            flags |= 1 << 3
        if Decoration.UNDERLINE in decoration:
            flags |= 1 << 7
        self._write(SELECT_PRINT_MODE + flags.to_bytes())


        