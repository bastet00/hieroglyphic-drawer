import os
from PIL import Image, ImageDraw, ImageFont


class FontController:
    def __init__(self):
        self.default_font_size = 100
        self.font = self.font_loader(self.default_font_size)

    def font_loader(self, font_size):
        custom_font_path = os.path.join(os.path.dirname(__file__), "..", "Gardiner.ttf")
        try:
            return ImageFont.truetype(custom_font_path, font_size)
        except OSError as e:
            print(f"Error loading font: {e}")
            raise

    def set_font_size(self, size):
        self.font = self.font_loader(size)


class CommonDraw:
    symbol_color = "black"
    padding = 10

    def get_dimensions(self, symbol, font):
        clone = Image.new("RGB", (0, 0), color="white")
        text_clone = ImageDraw.Draw(clone)
        x1, y1, x2, y2 = text_clone.textbbox((0, 0), symbol, font)
        symbol_width = x2 - x1
        symbol_height = y2 - y1
        return symbol_width, symbol_height, y2, y1


class StandAloneDraw(FontController, CommonDraw):
    def __init__(self):
        super().__init__()

    def __str__(self):
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


class VerticalDraw(FontController, CommonDraw):
    def __init__(self):
        super().__init__()

    def __str__(self):
        return "vertical_draw"

    def calc_dimensions(self, block, max_block_height, font_size=None):
        if font_size is None:
            font_size = max_block_height

        blocks = block["draw_info"]
        widths = []
        heights = []
        self.set_font_size(font_size)
        symbol_dimensions = []

        for symbol in blocks:
            width, height, y2, y1 = self.get_dimensions(symbol["symbol"], self.font)
            widths.append(width)
            heights.append(height)
            symbol_dimensions.append(
                {
                    "symbol": symbol["symbol"],
                    "symbol_width": width,
                    "symbol_height": height,
                    "y2": y2,
                    "y1": y1,
                },
            )

        total_height = sum(heights)
        if total_height > max_block_height - self.padding:
            new_font_size = font_size - 5
            return self.calc_dimensions(
                block, max_block_height, font_size=new_font_size
            )

        return symbol_dimensions, font_size, max(widths), sum(heights)

    def draw(self, block, draw, x, img_height):
        print(block)
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
            img_height -= symbol["symbol_height"] + empty_space - self.padding // 2


class ComposeDraw(FontController, CommonDraw):
    def __init__(self):
        super().__init__()

    def __str__(self):
        return "compose"

    def calc_dimensions(self, block, max_block_height, font_size=None):
        if font_size is None:
            font_size = max_block_height

        blocks = block["draw_info"]
        widths = []
        heights = []
        self.set_font_size(font_size)
        symbol_dimensions = []

        for symbol in blocks:
            width, height, y2, y1 = self.get_dimensions(symbol["symbol"], self.font)
            widths.append(width)
            heights.append(height)
            symbol_dimensions.append(
                {
                    "symbol": symbol["symbol"],
                    "symbol_width": width,
                    "symbol_height": height,
                    "y2": y2,
                    "y1": y1,
                },
            )

        total_height = heights[0] + max(heights[1:])
        top_symbol_width = widths[0]
        total_width = max(top_symbol_width, sum(widths[1:]))

        if total_height > max_block_height - self.padding:
            # Recursively decrease font size to fit block in image height
            new_font_size = font_size - 5
            return self.calc_dimensions(
                block, max_block_height, font_size=new_font_size
            )
        return symbol_dimensions, total_width, total_height, font_size

    def draw(self, block, draw, x, block_width, block_height, font_size, img_height):
        symbols = block["draw_info"]
        self.font = self.font_loader(font_size)
        curr_symbol_width = 0
        bottom_symbols = block["draw_info"][1:]
        vertical_empty_space = block_width - sum(
            [width["symbol_width"] for width in bottom_symbols]
        )
        for idx, symbol in enumerate(symbols):
            cx = (block_width - symbol["symbol_width"]) // 2
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


class ComposeUpDraw(FontController, CommonDraw):
    def __init__(self):
        super().__init__()

    def __str__(self):
        return "compose_up"

    def calc_dimensions(self, block, max_block_height, font_size=None):
        if font_size is None:
            font_size = max_block_height

        blocks = block["draw_info"]
        widths = []
        heights = []
        self.set_font_size(font_size)
        symbol_dimensions = []

        for symbol in blocks:
            width, height, y2, y1 = self.get_dimensions(symbol["symbol"], self.font)
            widths.append(width)
            heights.append(height)
            symbol_dimensions.append(
                {
                    "symbol": symbol["symbol"],
                    "symbol_width": width,
                    "symbol_height": height,
                    "y2": y2,
                    "y1": y1,
                },
            )

        total_height = max(heights[:2]) + heights[2]
        bottom_symbol_width = widths[2]
        total_width = max(bottom_symbol_width, sum(widths[:2]))

        if total_height > max_block_height - self.padding:
            # Recursively decrease font size to fit block in image height

            new_font_size = font_size - 5
            return self.calc_dimensions(
                block, max_block_height, font_size=new_font_size
            )
        return symbol_dimensions, total_width, total_height, font_size

    def draw(self, block, draw, x, block_width, block_height, font_size, img_height):
        symbols = block["draw_info"]
        self.font = self.font_loader(font_size)
        temp_x = x
        for idx, symbol in enumerate(symbols):
            cx = (block_width - symbol["symbol_width"]) // 2
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


class AmpersandDraw(FontController, CommonDraw):
    def __init__(self):
        super().__init__()

    def __str__(self):
        return "ampersand"

    def calc_dimensions(self, block, max_block_height, font_size=None):
        if font_size is None:
            font_size = max_block_height

        blocks = block["draw_info"]
        widths = []
        heights = []
        self.set_font_size(font_size)
        symbol_dimensions = []

        for symbol in blocks:
            width, height, y2, y1 = self.get_dimensions(symbol["symbol"], self.font)
            widths.append(width)
            heights.append(height)
            symbol_dimensions.append(
                {
                    "symbol": symbol["symbol"],
                    "symbol_width": width,
                    "symbol_height": height,
                    "y2": y2,
                    "y1": y1,
                },
            )

        total_height = max(heights)
        total_width = widths[0] + (widths[1])
        if total_height > max_block_height - self.padding:
            new_font_size = font_size - 5
            return self.calc_dimensions(
                block, max_block_height, font_size=new_font_size
            )
        return symbol_dimensions, total_width, total_height, font_size

    def draw(self, block, draw, x, block_width, block_height, font_size, img_height):
        symbols = block["draw_info"]
        self.font = self.font_loader(font_size)
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
            x += symbol["symbol_width"] - self.padding
