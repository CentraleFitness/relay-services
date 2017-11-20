from objects.graphics.gcontainer import GContainer

from PIL import Image, ImageDraw

class Oled_128_64(object):
    """description of class"""

    def __init__(self, i2c_bus=1, i2c_address=0x3c, *args, **kwargs):
        self.display = None
        self.image = None
        self.size = (128, 64)
        self.content = GContainer(self.size, (0, 0))

    def display_content(self) -> None:
        self.image.show(title="Debug")

    def update_content(self) -> None:
        self.image, _ = self.content.translate()
