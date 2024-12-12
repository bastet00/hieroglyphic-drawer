from PIL import Image, ImageDraw, ImageFont
from drawers.drawer import (
    StandAloneDraw,
    ComposeUpDraw,
    VerticalDraw,
    ComposeDraw,
    AmpersandDraw,
)


class DrawWrapper(
    StandAloneDraw, ComposeDraw, ComposeUpDraw, AmpersandDraw, VerticalDraw
):
    pass


class Draw(DrawWrapper):
    def __init__(self, font_size):
        self._blocks = {}
        self.wall_color = "white"
        self.max_block_height = font_size

    def set_blocks(self, block_num, blocks):
        self._blocks[block_num] = blocks

        drawers = {}
        for cls in self.__class__.mro():
            if cls not in (Draw, DrawWrapper, object):
                class_draw_type = cls().__str__()
                drawers[class_draw_type] = cls
        return drawers

    def get_image_instance(self, image_width):
        h = self.max_block_height
        image = Image.new("RGB", (image_width, h), color="white")
        draw = ImageDraw.Draw(image)
        return draw
