"""Oled.py"""

import Adafruit_GPIO.SPI as SPI
import Adafruit_GPIO.I2C as I2C
import Adafruit_SSD1306
from PIL import Image, ImageDraw

from .oledtext import OledText

BLACK_AND_WHITE = '1'
BLACK = 0
WHITE = 1

class Oled(OledText):
    """Definition of the class"""
    def __init__(self, i2c_bus=1, i2c_address=0x3c, *args, **kwargs):
        OledText.__init__(self)
        self.mode = kwargs.get("mode", "TEXT")
        self.display = Adafruit_SSD1306.SSD1306_128_64(
            rst=1,
            i2c_bus=i2c_bus,
            i2c_address=i2c_address,
            i2c=I2C)
        self.display.begin()
        self.display.clear()
        self.image = Image.new(
            BLACK_AND_WHITE,
            (self.display.width, self.display.height),
            color=BLACK)
        self.draw = ImageDraw.Draw(self.image)

    def _update_content(self) -> None:
        if self.mode == "TEXT":
            self._draw_background()
            for line, text in self.get_lines():
                self.draw.text(
                    (self.toffset, line * self.tspacing),
                    text,
                    font=self.tfont,
                    fill=self.tcolor)
        elif self.mode == "PICTURE":
            raise "Not implemented yet"

    def _update_display(self) -> None:
        self.display.image(self.image)
        self.display.display()

    def _draw_background(self) -> None:
        """Draw a black backgorund to the image, overwriting everything"""
        self.draw.rectangle(
            (0, 0, self.display.width, self.display.height),
            outline=0,
            fill=0)
        
        
    def refresh(self) -> None:
        """
        Add the content descrived by 'mode' in the image
        Then display the image
        """
        self._update_content()
        self._update_display()

    def clear_screen(self) -> None:
        """Set the image as blank"""
        self._draw_background()
        self._update_display()

    def display_text(self, pos: tuple, text: str):
        self.draw.text(pos, text, font=self.tfont, fill=self.tcolor)
