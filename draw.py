from PIL import Image, ImageDraw, ImageFont


class Draw:
    def __init__(self, font_size):
        self.font_size = font_size
        self.font = self.font_loader()
        self._arrange_blocks = {}

    def font_loader(self):
        custom_font_path = "./NotoSansEgyptianHieroglyphs-Regular.ttf"
        return ImageFont.truetype(custom_font_path, self.font_size)

    def set_blocks(self, block_num, blocks):
        self._arrange_blocks[block_num] = blocks

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

    def generate_block_points(self):
        """
        @Returns object contains block number as key,
            arr of object each holds symbol info
        """
        calc_per_block = {}
        for block_num, block in self._arrange_blocks.items():
            calc_per_block[block_num] = []
            for symbol in block:
                info = self.symbol_coordinates(symbol)
                calc_per_block[block_num].append(info)
        return calc_per_block

    def get_text_dimensions(self, text):
        """
        NOTE: Diemensions (0 width, 0 height) would always return x1 as 0
        @Return -> Tuple (x1,y1,x2,y2)
        """
        clone = Image.new("RGB", (0, 0), color="white")
        text_clone = ImageDraw.Draw(clone)
        dimensions = text_clone.textbbox((0, 0), text, font=self.font)
        return dimensions

    def displacement_per_block(self):
        """
        @Returns -> Tuple (
            horizontal_offset -> max value for each block horizontally
            vertical_offsets ->
            blocks: blocks to be drawn
        )
        """
        blocks = self.generate_block_points()
        horizontal_offset = []
        vertical_offsets = []

        for block_num, arr_of_blocks in blocks.items():
            widths = []
            heights = []
            for idx, block in enumerate(arr_of_blocks):
                widths.append(block["symbol_width"])
                heights.append(block["symbol_height"])
            if len(arr_of_blocks) == 3:
                sum1 = widths[0] + widths[1]
                sum2 = widths[2]
                horizontal_offset.append(max(sum1, sum2))

                bottom_height = max(heights[0], heights[1])
                total_height = bottom_height + heights[2]
                vertical_offsets.append(total_height)
            else:
                horizontal_offset.append(max(widths))
                if len(arr_of_blocks) == 2:
                    vertical_offsets.append(heights[0] + heights[1])
                else:
                    vertical_offsets.append(heights[0])

        return horizontal_offset, vertical_offsets, blocks

    def three_element_block_info(self, xoffset, yoffset, arr_of_blocks, block_num):
        # Calculate how many points to reach certain block_num
        start_x = sum(xoffset[0:block_num])

        # width of two horizontal elements
        bottom_width = (
            arr_of_blocks[0]["symbol_width"] + arr_of_blocks[1]["symbol_width"]
        )
        y = max(yoffset) - arr_of_blocks[0]["symbol_height"]
        return start_x, bottom_width, y

    def three_elements_block(self, xoffset, yoffset, arr_of_blocks, draw, block_num):

        start_x, bottom_width, y = self.three_element_block_info(
            xoffset, yoffset, arr_of_blocks, block_num
        )
        # Drawing elements one by one
        draw.text(
            (start_x, y - arr_of_blocks[0]["baseline_y"]),
            text=arr_of_blocks[0]["symbol"],
            fill="black",
            font=self.font,
        )
        draw.text(
            (
                start_x + arr_of_blocks[0]["symbol_width"],
                y - arr_of_blocks[1]["baseline_y"],
            ),
            text=arr_of_blocks[1]["symbol"],
            fill="black",
            font=self.font,
        )
        cx = start_x + (bottom_width - arr_of_blocks[2]["symbol_width"]) // 2
        top_y = y - arr_of_blocks[2]["symbol_height"]
        draw.text(
            (cx, top_y - arr_of_blocks[2]["baseline_y"]),
            text=arr_of_blocks[2]["symbol"],
            fill="black",
            font=self.font,
        )

    def draw(self):
        xoffset, yoffset, blocks = self.displacement_per_block()
        w = sum(xoffset)
        h = max(yoffset)
        image = Image.new("RGB", (w, h), color="white")
        draw = ImageDraw.Draw(image)
        x = 0
        y = h

        for block_num, arr_of_blocks in blocks.items():
            if len(arr_of_blocks) > 2:
                self.three_elements_block(
                    xoffset, yoffset, arr_of_blocks, draw, block_num
                )
            elif len(arr_of_blocks) <= 2:
                # 1-2 Symbols per block
                for idx, block in enumerate(arr_of_blocks):
                    y -= block["symbol_height"]
                    draw.text(
                        (x, y - block["baseline_y"]),
                        text=block["symbol"],
                        fill="black",
                        font=self.font,
                    )

            # Move x position for next block
            x += xoffset[block_num]
            y = h

        image.save("output.png")
