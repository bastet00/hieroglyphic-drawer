import os
from PIL import Image, ImageDraw, ImageFont
from abc import ABC, abstractmethod, abstractclassmethod


class CommonDraw(ABC):
    symbol_color = "black"
    padding = 10

    def __init__(self):
        self.default_font_size = 100
        self.font = self.font_loader(self.default_font_size)

    @abstractclassmethod
    def get_class_draw_type(cls):
        """
        Class method should return a string,
        matches the handler name,
        which helps to detect the drawing style
        """
        pass

    @abstractmethod
    def calc_dimensions(self, block, max_block_height, font_size=None):
        """
        Each drawing class should calculate its block width and height
        ex. VerticalDraw checks symbols so they don't execed total img height
        @block -> each class recieve its own block to draw
        @max_block_height -> total image height
        @font_size-> recursive call to decrease font size when,
        a block doesn't fit into the default dimensions
        """
        pass

    @abstractmethod
    def draw(self, block, draw, x, img_height):
        """
        @block -> recieve its own block with some additional info,
        ex. dimensions for block,symbols and font size for the block to be used
        @draw -> class instance used to draw the image
        @img_height -> what do you think it would be ?
        """
        pass

    def get_dimensions(self, symbol, font):
        clone = Image.new("RGB", (0, 0), color="white")
        text_clone = ImageDraw.Draw(clone)
        x1, y1, x2, y2 = text_clone.textbbox((0, 0), symbol, font)
        symbol_width = x2 - x1
        symbol_height = y2 - y1
        return symbol_width, symbol_height, y2, y1

    def foobar(self, symbol):
        width, height, y2, y1 = self.get_dimensions(symbol, self.font)
        symbol_dimensions = {
            "symbol": symbol,
            "symbol_width": width,
            "symbol_height": height,
            "y2": y2,
            "y1": y1,
        }
        return symbol_dimensions

    def font_loader(self, font_size):
        custom_font_path = os.path.join(os.path.dirname(__file__), "..", "Gardiner.ttf")
        try:
            return ImageFont.truetype(custom_font_path, font_size)
        except OSError as e:
            print(f"Error loading font: {e}")
            raise

    def set_font_size(self, size):
        self.font = self.font_loader(size)
