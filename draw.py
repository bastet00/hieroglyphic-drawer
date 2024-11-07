from PIL import Image, ImageDraw, ImageFont
from read import GenerateSmybols


class Draw:
    def __init__(self, width, height):
        self.width = width
        self.height = height

    def font_loader(self):
        try:
            custom_font_path = "~/Downloads/Noto_Sans_Egyptian_Hieroglyphs/NotoSansEgyptianHieroglyphs-Regular.ttf"
            font = ImageFont.truetype(custom_font_path, 30)
        except IOError:
            print("Couldn't load", custom_font_path, "switch to default")
            font = ImageFont.load_default()

        return font

    def draw(self):
        image = Image.new("RGB", (self.width, self.height), color="white")
        draw = ImageDraw.Draw(image)
        text = GenerateSmybols("./signs_mapper.json").map_code_to_symbols()
        font = self.font_loader()

        text_diementions = draw.textbbox((0, 0), text, font=font)
        text_width = text_diementions[2] - text_diementions[0]
        text_height = text_diementions[3] - text_diementions[1]

        text_position = ((self.width - text_width) / 2, (self.height - text_height) / 2)

        draw.text(text_position, text, font=font, fill="black")

        image.save("output.png")


# Create an instance of Draw and draw the image
Draw(400, 200).draw()
