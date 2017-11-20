from objects.graphics.gcontainer import GContainer

from PIL import Image, ImageDraw

SCREEN_SIZE = (128, 64)

class Oled_128_64(object):
    """description of class"""

    def __init__(self, i2c_bus=1, i2c_address=0x3c, *args, **kwargs):
        self.display = None
        self.image = None
        self.size = SCREEN_SIZE
        self.content = kwargs.get('content', None)

    def display_content(self) -> None:
        self.image.show()

    def update_content(self) -> None:
        if self.content:
            self.image, _ = self.content.translate()
        else:
            self.image = Image.new('1', self.size, 0)
