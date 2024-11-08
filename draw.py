from PIL import Image, ImageDraw, ImageFont


class Draw:
    def __init__(self, font_size, text):
        self.font_size = font_size
        self.text = text
        self.font = self.font_loader()

    def font_loader(self):
        custom_font_path = "./NotoSansEgyptianHieroglyphs-Regular.ttf"
        return ImageFont.truetype(custom_font_path, self.font_size)

    def get_text_dimensions(self):
        """
        generate dimensions spesfic for each text
        @Return (width,height)
        """
        clone = Image.new("RGB", (0, 0), color="white")
        text_clone = ImageDraw.Draw(clone)
        dimensions = text_clone.textbbox((0, 0), self.text, font=self.font)

        height_padding = 1.5
        w = dimensions[2] - dimensions[0]
        h = int((dimensions[3] - dimensions[1]) * height_padding)

        return w, h

    def draw(self):
        w, h = self.get_text_dimensions()
        image = Image.new("RGB", (w, h), color="white")
        draw = ImageDraw.Draw(image)

        text_dimensions = draw.textbbox((0, 0), self.text, font=self.font)
        total_x = text_dimensions[2] - text_dimensions[0]
        total_y = text_dimensions[3] - text_dimensions[1]

        x = (w - total_x) / 2
        y = (h - total_y) / 2 - text_dimensions[1]

        draw.text((x, y), self.text, font=self.font, fill="black")
        image.save("output.png")
