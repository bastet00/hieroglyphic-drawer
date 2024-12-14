from .common import CommonDraw


"""
    Drawing block that contains & special character
"""


class AmpersandDraw(CommonDraw):
    def __init__(self):
        super().__init__()

    @classmethod
    def get_class_draw_type(cls):
        return "ampersand"

    def calc_dimensions(self, block, max_block_height, font_size=None):
        if font_size is None:
            font_size = max_block_height

        blocks = block["draw_info"]
        widths = []
        heights = []
        self.set_font_size(font_size)
        symbol_dimensions = []

        for idx, symbol in enumerate(blocks):
            symbol_dimensions.append(self.foobar(symbol["symbol"]))
            widths.append(symbol_dimensions[idx]["symbol_width"])
            heights.append(symbol_dimensions[idx]["symbol_height"])

        total_height = max(heights)
        total_width = widths[0] + int(widths[1] // 1.40)
        print(total_width)
        print(symbol_dimensions)
        if total_height > max_block_height - self.padding:
            new_font_size = font_size - 5
            return self.calc_dimensions(
                block, max_block_height, font_size=new_font_size
            )
        return symbol_dimensions, font_size, total_width, total_height

    def draw(self, block, draw, x, img_height):
        symbols = block["draw_info"]
        block_info = block["block_info"]
        self.font = self.font_loader(block_info[0])
        for idx, symbol in enumerate(symbols):
            y = img_height - symbol["y2"]
            if idx != 0:
                y = 0 - symbol["y1"]

            draw.text(
                (x, y),
                text=symbol["symbol"],
                fill=self.symbol_color,
                font=self.font,
            )
            x += symbol["symbol_width"] - (self.padding * 3)
