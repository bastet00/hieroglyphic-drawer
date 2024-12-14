from .common import CommonDraw


class VerticalDraw(CommonDraw):

    def __init__(self):
        super().__init__()

    @classmethod
    def get_class_draw_type(cls):
        return "vertical"

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

        total_height = sum(heights)
        if total_height > max_block_height - self.padding:
            new_font_size = font_size - 5
            return self.calc_dimensions(
                block, max_block_height, font_size=new_font_size
            )

        return symbol_dimensions, font_size, max(widths), total_height

    def draw(self, block, draw, x, img_height):
        symbols = block["draw_info"]
        block_info = block["block_info"]
        font_size = block_info[0]
        self.font = self.font_loader(font_size)
        empty_space = img_height - block_info[2]
        for symbol in symbols[::-1]:
            cx = (block_info[1] - symbol["symbol_width"]) // 2
            y = img_height - symbol["y2"]
            draw.text(
                (x + cx, y),
                text=symbol["symbol"],
                fill=self.symbol_color,
                font=self.font,
            )
            if len(symbols) > 2:
                img_height -= symbol["symbol_height"] + (empty_space // len(symbols))
            else:
                img_height -= symbol["symbol_height"] + empty_space - self.padding // 2
