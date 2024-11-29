import sys
from PIL import Image, ImageDraw, ImageFont

from drawers.drawer import (
    AmpersandDraw,
    ComposeDraw,
    ComposeUpDraw,
    StandAloneDraw,
    VerticalDraw,
)


DRAW_TYPE = {
    "ampersand": AmpersandDraw,
    "compose": ComposeDraw,
    "compose_up": ComposeUpDraw,
    "stand_alone": StandAloneDraw,
    "vertical_draw": VerticalDraw,
}


class Draw:
    def __init__(self):
        self._blocks = {}
        self.wall_color = "white"
        self.max_block_height = 100

    def set_blocks(self, block_num, blocks):
        self._blocks[block_num] = blocks

    def drawer_capture(self, draw_type):
        try:
            return DRAW_TYPE[draw_type]
        except KeyError:
            sys.tracebacklimit = 0
            raise KeyError(f"Couldn't find a class to draw {draw_type}")

    def get_block_info(self):
        per_block_width = []
        block_height = []
        block_font_size = []
        for block_num, block in self._blocks.items():
            draw_class = self.drawer_capture(block["draw_type"])()
            new_info, width, height, font_size = draw_class.calc_dimensions(
                block, self.max_block_height
            )
            block_height.append(height)
            per_block_width.append(width)
            self._blocks[block_num]["draw_info"] = new_info
            block_font_size.append(font_size)
        return per_block_width, block_height, block_font_size

    def draw(self):
        per_block_width, per_block_height, block_font_size = self.get_block_info()
        w = sum(per_block_width)
        h = self.max_block_height
        image = Image.new("RGB", (w, h), color="white")
        draw = ImageDraw.Draw(image)
        x = 0
        print("Generating an image with", w, h)
        for block_num, block in self._blocks.items():
            draw_class = self.drawer_capture(block["draw_type"])()
            if isinstance(draw_class, StandAloneDraw):
                draw_class.draw(block, draw, x, h)
            else:
                draw_class.draw(
                    block,
                    draw,
                    x,
                    per_block_width[block_num],
                    per_block_height[block_num],
                    block_font_size[block_num],
                    h,
                )
            x += per_block_width[block_num]

        image.save("output.png")
