import platform

from PIL import Image, ImageDraw

import Adafruit_GPIO.SPI as SPI
import Adafruit_GPIO.I2C as I2C
import Adafruit_SSD1306

from objects.graphics.gcontainer import GContainer


SCREEN_SIZE = (128, 64)

class Oled_128_64(object):
    """description of class"""

    def __init__(self, i2c_bus=1, i2c_address=0x3c, *args, **kwargs):
        """
        kwargs:
            content: A container
        """
        self.display = Adafruit_SSD1306.SSD1306_128_64(
            rst=1,
            i2c_bus=i2c_bus,
            i2c_address=i2c_address,
            i2c=I2C)
        self.display.begin()
        self.display.clear()
        self.image = None
        self.size = SCREEN_SIZE
        self.content = kwargs.get('content', None)

    def display_content(self) -> None:
        if self.image:
            self.display.image(self.image)
            self.display.display()
        else:
            print("Nothing to display")

    def update_content(self) -> None:
        if self.content:
            self.image, _ = self.content.translate()
        else:
            self.image = Image.new('1', self.size, 0)

    def _change_content(self, new_content) -> None:
        self.content = new_content

    def interact(self, input: str) -> None:
        if input == 'B' and self.content.parent:
            self.content.iter.reset()
            self.content = self.content.parent
        else:
            action = self.content.interact(input)
            if action:
                func, param = action
                func(param)
            # else:
            #     do_nothing()
