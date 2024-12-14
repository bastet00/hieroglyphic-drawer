from .common import CommonDraw


class StandAloneDraw(CommonDraw):
    def __init__(self):
        super().__init__()

    @classmethod
    def get_class_draw_type(cls):
        return "stand_alone"

    def calc_dimensions(self, block, font_size):
        blocks = block["draw_info"]
        symbol_dimensions = []
        for symbol in blocks:
            width, height, y2, y1 = self.get_dimensions(
                symbol["symbol"], self.font_loader(font_size)
            )
            symbol_dimensions.append(
                {
                    "symbol": symbol["symbol"],
                    "symbol_width": width,
                    "symbol_height": height,
                    "y2": y2,
                    "y1": y1,
                }
            )
        return symbol_dimensions, font_size, width, height

    def draw(self, block, draw, x, img_height):
        data = block["draw_info"][0]
        block_info = block["block_info"]
        self.font = self.font_loader(block_info[0])
        y = img_height - data["y2"]
        draw.text(
            (x, y),
            text=data["symbol"],
            fill=self.symbol_color,
            font=self.font,
        )
