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

    def generate_blocks(self):
        blocks = {}
        for key, arr in self._arrange_blocks.items():
            blocks[key] = []
            for char in arr:
                dimensions = self.get_text_dimensions(char)
                baseline_y = dimensions[1]
                max_y_point = dimensions[3]
                blocks[key].append(
                    {
                        "char": char,
                        "max_y": max_y_point,
                        "height": max_y_point - baseline_y,
                        "char_width": dimensions[2] - dimensions[0],
                        "baseline_offset": baseline_y,
                    }
                )
        return blocks

    def generate_diemensions(self):
        blocks = self.generate_blocks()
        total_image_width = 0
        max_block_height = 0
        for block in blocks.values():
            max_symbol_width = max([obj["char_width"] for obj in block])
            block_height = [obj["height"] for obj in block]
            current_block_height = sum(block_height)

            if current_block_height > max_block_height:
                max_block_height = current_block_height

            total_image_width += max_symbol_width

        return total_image_width, max_block_height

    def get_text_dimensions(self, text):
        """
        Generate dimensions specific for each text
        @Return (width, height)
        """
        clone = Image.new("RGB", (0, 0), color="white")
        text_clone = ImageDraw.Draw(clone)
        dimensions = text_clone.textbbox((0, 0), text, font=self.font)
        return dimensions

    def draw(self):
        w, h = self.generate_diemensions()
        print(f"Initializing image with Width:{w} Height:{h}")
        blocks = self.generate_blocks()
        image = Image.new("RGB", (w, h), color="white")
        draw = ImageDraw.Draw(image)

        x = 0

        for idx, block in blocks.items():
            block_width = max(obj["char_width"] for obj in block)
            print(block)
            y = h
            for obj in block:
                y -= obj["max_y"] - obj["baseline_offset"]
                draw.text(
                    (x, (y - obj["baseline_offset"])),
                    text=obj["char"],
                    fill="black",
                    font=self.font,
                )
                print(f"Character '{obj['char']}' drawn at coordinates: ({x}, {y})")

            x += block_width

        image.save("output.png")
