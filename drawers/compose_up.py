from .common import CommonDraw


class ComposeUpDraw(CommonDraw):
    def __init__(self):
        super().__init__()

    @classmethod
    def get_class_draw_type(cls):
        return "compose_up"

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

        total_height = max(heights[:2]) + heights[2]
        bottom_symbol_width = widths[2]
        total_width = max(bottom_symbol_width, sum(widths[:2]))

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
        temp_x = x
        for idx, symbol in enumerate(symbols):
            cx = (block_info[1] - symbol["symbol_width"]) // 2
            y = 0 - symbol["y1"]
            if idx == 2:
                y = img_height - symbol["y2"]
                temp_x = x + cx

            draw.text(
                (temp_x, y),
                text=symbol["symbol"],
                fill=self.symbol_color,
                font=self.font,
            )
            temp_x += symbol["symbol_width"]
