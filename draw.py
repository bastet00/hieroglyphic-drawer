from PIL import Image, ImageDraw, ImageFont


class Draw:
    def __init__(self, font_size):
        self.default_font_size = font_size
        self.font = self.font_loader(self.default_font_size)
        self._blocks = {}

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

    def calc_offsets(self, block):
        data = block["draw_info"]
        draw_type = block["draw_type"]
        x_offsets = []
        y_offsets = []

        for obj in data:
            x_offsets.append(obj["symbol_width"])
            y_offsets.append(obj["symbol_height"])

        if draw_type == "compose":
            top_height = y_offsets[0]
            bottom_max_height = max(y_offsets[1], y_offsets[2])
            top_width = x_offsets[0]
            bottom_max_width = max(x_offsets[1], x_offsets[2])
            return max(top_width, bottom_max_width) + 5, top_height + bottom_max_height
        return max(x_offsets), sum(y_offsets)

    def stand_alone(self, draw, block, x, total_height):
        symbol = block["draw_info"][0]
        draw.text(
            (x, total_height - symbol["y2"]),
            text=symbol["symbol"],
            fill="black",
            font=self.font,
        )

    def vertical_draw(self, draw, block, x, total_height):
        # TODO: center the next vertically drawn symbol on x axis if the previous was wider
        symbols = block["draw_info"]
        y = total_height
        for symbol in symbols[::-1]:
            draw.text(
                (x, y - symbol["y2"]),
                text=symbol["symbol"],
                fill="black",
                font=self.font,
            )
            y -= symbol["symbol_height"]

    def second_on_top(self, draw, block, x, total_height):
        # TODO: if two symbols is the same use & to combine them,
        # horizontally
        # TODO: case : &
        # TODO: Horizontal offset, verticall offset calculation may be considered ?
        symbols = block["draw_info"]
        y = total_height
        for idx, symbol in enumerate(symbols):
            if idx == 0:
                y = y - symbol["y2"]
            else:
                y = 0
                y -= symbol["baseline_y"]
                x += symbol["symbol_width"]

            print(f"Drawing {symbol["symbol"]} at {x,y}")

            draw.text(
                (x, y),
                text=symbol["symbol"],
                fill="black",
                font=self.font,
            )

    def compose(self, draw, block, x, total_height):
        symbols = block["draw_info"]
        y = 0
        for idx, symbol in enumerate(symbols):
            if idx == 0:
                y = y - symbol["baseline_y"] + 5
            else:
                y = total_height - symbol["y2"] + 5

            if idx == 2:
                x += symbol["symbol_width"]

            print(f"Drawing {symbol["symbol"]} at {x,y}")
            draw.text(
                (x, y),
                text=symbol["symbol"],
                fill="black",
                font=self.font,
            )

    def draw(self):
        x_offset, y_offset = self.displacement_per_block()
        print(self._blocks)
        w, h = sum(x_offset), max(y_offset)
        print(f"Image width:{w}, Image Height {h}")
        image = Image.new("RGB", (w, h), color="white")
        draw = ImageDraw.Draw(image)
        x = 0
        for block_num, block in self._blocks.items():
            if hasattr(self, block["draw_type"]):
                draw_method = getattr(self, block["draw_type"])
                draw_method(draw, block, x, h)
            else:
                raise ValueError(
                    f"Function implementation for {block["draw_type"]} block is missing"
                )

            # Move x position for next block
            x += x_offset[block_num]

        image.save("output.png")
