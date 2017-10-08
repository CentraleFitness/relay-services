"""oledtext.py"""

from PIL import ImageFont
from .utilities.linemanager import LineManager

WHITE = 1

class OledText(LineManager):
    """Definition of the class"""
    def __init__(self):
        LineManager.__init__(self, 6)
        self.tfont = ImageFont.load_default()
        self.tcolor = WHITE
        self.tspacing = 10
        self.toffset = 0

    def load_font(self, font: str, size=10):
        """
        Load a specific font
        params: a path to a font file
        """
        self.tfont = ImageFont.load(font, size)

    def default_font(self):
        """
        Restore the font to system default
        """
        self.tfont = ImageFont.load_default()
