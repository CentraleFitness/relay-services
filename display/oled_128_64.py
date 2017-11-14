from display.dummy import Dummy
from display.gcontainer import GContainer

from PIL import Image, ImageDraw

class Oled_128_64(object):
    """description of class"""

    def __init__(self, i2c_bus=1, i2c_address=0x3c, *args, **kwargs):
        self.display = None
        self.image = Image.new('1', (128, 64), color=1)
        self.draw = ImageDraw.Draw(self.image)
        self.content = GContainer()

    def display_content(self):
        self.image.show(title="Debug")
