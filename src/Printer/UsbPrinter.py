import usb.core
import usb.util
from . import PrinterDevice
from .constants import *

vid = 0x04b8
did = 0x0e02
interface=0
n_ep=0x82
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

    def _write(self, data: str):
        data = data.replace("—", "-")
        self.device.write(out_ep, data)

    def _cut(self):
        #self._write(FEED_AND_CUT_PARTIAL) # doesn't work??
        self._write("\n\n\n\n\n\n")
        self._write(CUT_PARTIAL)

    def _image(self, image):
        self._write("----------".center(self.max_text_with))
        self._write("\n\n\n")
        self._write("images not implemented".center(self.max_text_with))
        self._write("\n\n\n")
        self._write("----------".center(self.max_text_with))

    def _reset(self):
        self._write(INITIALIZE)    
