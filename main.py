from handlers.convertor import MdcConvertor

if __name__ == "__main__":
    blocks = MdcConvertor("./signs_mapper.json", "F40:X1*F34")
    blocks.draw_image(font_size=200, storage_path="output.png")
