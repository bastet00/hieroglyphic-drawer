from PIL import Image, ImageDraw
from abc import ABC
from drawers.vertical import VerticalDraw
from drawers.compose import ComposeDraw
from drawers.compose_up import ComposeUpDraw
from drawers.ampersand import AmpersandDraw
from drawers.stand_alone import StandAloneDraw
from drawers.common import CommonDraw


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

    def get_drawers(self):
        drawers = {}
        for cls in self.__class__.mro():
            if cls not in (Draw, DrawWrapper, object, CommonDraw, ABC):
                class_draw_type = cls.get_class_draw_type()
                drawers[class_draw_type] = cls
        return drawers

    def get_image_instance(self, image_width):
        h = self.max_block_height
        print(f"Image instance: Width:{image_width}-Height:{h} ")
        image = Image.new("RGB", (image_width, h), color="white")
        draw = ImageDraw.Draw(image)
        return draw, image
