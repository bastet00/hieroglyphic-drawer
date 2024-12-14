from .common import CommonDraw


class ComposeDraw(CommonDraw):
    def __init__(self):
        super().__init__()

    @classmethod
    def get_class_draw_type(cls):
        return "compose"

    def calc_dimensions(self, block, max_block_height, font_size=None):
        if font_size is None:
            font_size = max_block_height

        blocks = block["draw_info"]
        widths = []
        heights = []
        self.set_font_size(font_size)
        symbol_dimensions = []

        for idx, symbol in enumerate(blocks):
            symbol_dimensions.append(self.get_symbol_dimensions(symbol["symbol"]))
            widths.append(symbol_dimensions[idx]["symbol_width"])
            heights.append(symbol_dimensions[idx]["symbol_height"])

        total_height = heights[0] + max(heights[1:])
        top_symbol_width = widths[0]
        total_width = max(top_symbol_width, sum(widths[1:]))

        if total_height > max_block_height - self.padding:
            # Recursively decrease font size to fit block in image height
            new_font_size = font_size - 5
            return self.calc_dimensions(
                block, max_block_height, font_size=new_font_size
            )
        return symbol_dimensions, font_size, total_width, total_height

    def draw(self, block, draw, x, img_height):
        symbols = block["draw_info"]
        block_info = block["block_info"]
        self.font = self.font_loader(block_info[0])
        curr_symbol_width = 0
        bottom_symbols = block["draw_info"][1:]
        vertical_empty_space = block_info[1] - sum(
            [width["symbol_width"] for width in bottom_symbols]
        )
        for idx, symbol in enumerate(symbols):
            cx = (block_info[1] - symbol["symbol_width"]) // 2
            y = 0 - symbol["y1"]
            if idx != 0:
                y = img_height
                y -= symbol["y2"]
                curr_symbol_width = symbol["symbol_width"] + vertical_empty_space

            draw.text(
                (x + cx if idx == 0 else x, y),
                text=symbol["symbol"],
                fill=self.symbol_color,
                font=self.font,
            )
            x += curr_symbol_width
