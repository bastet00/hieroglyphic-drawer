from PIL import Image, ImageDraw, ImageFont


class Draw:
    def __init__(self, font_size, text, height):
        self.font_size = font_size
        self.text = text
        self.height = height

    def font_loader(self):
        try:
            custom_font_path = "./NotoSansEgyptianHieroglyphs-Regular.ttf"
            font = ImageFont.truetype(custom_font_path, self.font_size)
        except IOError:
            print("Couldn't load", custom_font_path, "switch to default")
            font = ImageFont.load_default()

        return font

    def total_width(self):
        return self.font_size * len(self.text)

    def draw(self):
        print("Width:", self.total_width(), "Height:", self.height)
        image = Image.new("RGB", (self.total_width(), self.height), color="white")
        draw = ImageDraw.Draw(image)
        font = self.font_loader()

        text_diementions = draw.textbbox((0, 0), self.text, font=font)
        text_width = text_diementions[2] - text_diementions[0]
        text_height = text_diementions[3] - text_diementions[1]

        pos_x = (self.total_width() - text_width) / 2
        post_y = (self.height - text_height) / 2

        text_position = (pos_x, post_y)

        draw.text(text_position, self.text, font=font, fill="black")

        image.save("output.png")
