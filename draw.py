from PIL import Image, ImageDraw, ImageFont

from drawers.drawer import (
    AmbersandDraw,
    ComposeDraw,
    ComposeUpDraw,
    StandAloneDraw,
    VerticalDraw,
)


DRAW_TYPE = {
    "second_on_top": AmbersandDraw,
    "compose": ComposeDraw,
    "compose_up": ComposeUpDraw,
    "stand_alone": StandAloneDraw,
    "vertical_draw": VerticalDraw,
}


class Draw:
    def __init__(self, font_size):
        self.default_font_size = font_size
        self.font = self.font_loader(self.default_font_size)
        self._blocks = {}
        self.symbol_color = "black"
        self.wall_color = "white"
        # self.symbol_color = "#090909"
        # self.wall_color = "#763c0c"

    def font_loader(self, font_size):
        custom_font_path = "./NotoSansEgyptianHieroglyphs-Regular.ttf"
        return ImageFont.truetype(custom_font_path, font_size)

    def set_font_size(self, font_size):
        self.font = self.font_loader(font_size)

    def set_blocks(self, block_num, blocks):
        self._blocks[block_num] = blocks

    def get_text_dimensions(self, text):
        """
        NOTE: Diemensions (0 width, 0 height) would always return x1 as 0
        @Return -> Tuple (x1,y1,x2,y2)
        """
        clone = Image.new("RGB", (0, 0), color="white")
        text_clone = ImageDraw.Draw(clone)
        dimensions = text_clone.textbbox((0, 0), text, font=self.font)
        return dimensions

    def symbol_coordinates(self, symbol):
        """
        @symbol => symbol that going to be drawn
        @Return object contains info about symbol coordinates,width,height
        """
        x1, y1, x2, y2 = self.get_text_dimensions(symbol)
        symbol_width = x2
        symbol_height = y2 - y1

        if symbol == "𓏏":
            symbol_height = symbol_height + 10

        return {
            "symbol": symbol,
            "symbol_width": symbol_width,
            "symbol_height": symbol_height,
            "y2": y2,
            "baseline_y": y1,
        }

    def displacement_per_block(self):
        horizontal_offset = []
        vertical_offset = []
        for block_num, block in self._blocks.items():
            symbols = block["draw_info"]
            block["draw_info"] = [
                self.symbol_coordinates(symbol["symbol"]) for symbol in symbols
            ]
            x_offset, y_offset = self.calc_offsets(block)
            horizontal_offset.append(x_offset)
            vertical_offset.append(y_offset)
        return horizontal_offset, vertical_offset

    def compose_offsets(self, x_offsets, y_offsets):
        top_height = y_offsets[0]
        bottom_max_height = max(y_offsets[1], y_offsets[2])
        top_width = x_offsets[0]
        bottom_max_width = x_offsets[1] + x_offsets[2]
        return (
            max(top_width, bottom_max_width),
            top_height + bottom_max_height,
        )

    def compose_up_offsets(self, x_offsets, y_offsets):
        max_top_height = max(y_offsets[0], y_offsets[1])
        bottom_height = y_offsets[2]
        top_width = x_offsets[0] + x_offsets[1]
        bottom_width = x_offsets[2]
        return max(top_width, bottom_width), max_top_height + bottom_height

    def calc_offsets(self, block):
        """
        Each block requires some specific calculation
        ex.
            second_on_top is a vertical draw technique that
            calculates the block width with the max width of all elements
            calculates the block height with all elements heights
        """

        data = block["draw_info"]
        draw_type = block["draw_type"]
        x_offsets = []
        y_offsets = []

        for obj in data:
            x_offsets.append(obj["symbol_width"])
            y_offsets.append(obj["symbol_height"])
            # print(block)
            # print(x_offsets, y_offsets)
        match draw_type:
            case "compose":
                return self.compose_offsets(x_offsets, y_offsets)
            case "compose_up":
                return self.compose_up_offsets(x_offsets, y_offsets)
            case _:
                return max(x_offsets), sum(y_offsets)

    def stand_alone(self, **kwargs):
        symbol = kwargs["block"]["draw_info"][0]
        kwargs["draw"].text(
            (kwargs["x"], kwargs["total_height"] - symbol["y2"]),
            text=symbol["symbol"],
            fill=self.symbol_color,
            font=self.font,
        )

    def vertical_draw(self, **kwargs):
        symbols = kwargs["block"]["draw_info"]
        y = kwargs["total_height"]

        for symbol in symbols[::-1]:
            move_symbol = (kwargs["block_width"] - symbol["symbol_width"]) // 2
            centered_x = kwargs["x"] + move_symbol
            kwargs["draw"].text(
                (centered_x, y - symbol["y2"]),
                text=symbol["symbol"],
                fill=self.symbol_color,
                font=self.font,
            )

            y -= symbol["symbol_height"]

    def second_on_top(self, **kwargs):
        # TODO: if two symbols is the same use & to combine them,
        # horizontally
        # TODO: case : &
        # TODO: Horizontal offset, verticall offset calculation may be considered ?
        symbols = kwargs["block"]["draw_info"]
        y = kwargs["total_height"]
        for idx, symbol in enumerate(symbols):
            if idx == 0:
                y = y - symbol["y2"]
            else:
                y = 0
                y -= symbol["baseline_y"]
                kwargs["x"] += symbol["symbol_width"]

            kwargs["draw"].text(
                (kwargs["x"], y),
                text=symbol["symbol"],
                fill=self.symbol_color,
                font=self.font,
            )

    def compose(self, **kwargs):
        symbols = kwargs["block"]["draw_info"]
        y = 0
        # print(
        #     f"this block starts from {kwargs["x"]} with block_width of {kwargs["block_width"]}"
        # )
        for idx, symbol in enumerate(symbols):
            temp_x = kwargs["x"]
            if idx == 0:
                y = y - symbol["baseline_y"]
                kwargs["x"] = (kwargs["block_width"] - symbol["symbol_width"]) // 2
            else:
                y = kwargs["total_height"] - symbol["y2"]
                # if symbol["symbol"] == "𓏏":
                #     y += 7

            kwargs["x"] = temp_x

            if idx == 2:
                prev_width = symbols[idx - 1]["symbol_width"]
                kwargs["x"] = kwargs["x"] + prev_width

            print(f"Drawing at {symbol["symbol"]} {kwargs["x"], y}")

            kwargs["draw"].text(
                (kwargs["x"], y),
                text=symbol["symbol"],
                fill=self.symbol_color,
                font=self.font,
            )

    def compose_up(self, **kwargs):
        symbols = kwargs["block"]["draw_info"]
        y = 0

        # print(
        #     f"this block starts from {kwargs["x"]} with block_width of {kwargs["block_width"]}"
        # )

        for idx, symbol in enumerate(symbols):
            y = 0 - symbol["baseline_y"]
            if idx == 1:
                kwargs["x"] += symbols[idx - 1]["symbol_width"]
            if idx == 2:
                y = kwargs["total_height"] - symbol["y2"]
                reset_x = kwargs["x"] - symbols[0]["symbol_width"]
                block_center = reset_x + kwargs["block_width"] // 2
                symbol_half_width = symbol["symbol_width"] // 2
                kwargs["x"] = block_center - symbol_half_width

            # print(f"Drawing at {symbol["symbol"]} {kwargs["x"], y}")
            kwargs["draw"].text(
                (kwargs["x"], y),
                text=symbol["symbol"],
                fill=self.symbol_color,
                font=self.font,
            )

    def draw(self):
        x_offset, y_offset = self.displacement_per_block()
        w, h = sum(x_offset), max(y_offset)
        print(f"Image width:{w}, Image Height {h}")
        image = Image.new("RGB", (w, h), color=self.wall_color)
        draw = ImageDraw.Draw(image)
        x = 0
        for block_num, block in self._blocks.items():
            print(f"I need to call class for", block["draw_type"])
            foo = DRAW_TYPE[block["draw_type"]]().hello_idiot()
            if hasattr(self, block["draw_type"]):
                draw_method = getattr(self, block["draw_type"])
                draw_method(
                    draw=draw,
                    block=block,
                    x=x,
                    total_height=h,
                    block_width=x_offset[block_num],
                )
            else:
                raise ValueError(
                    f"Function implementation for {block["draw_type"]} block is missing"
                )

            # Move x position for next block
            x += x_offset[block_num]

        image.save("output.png")
