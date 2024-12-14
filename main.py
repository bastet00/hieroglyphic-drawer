from handlers.convertor import MdcConvertor

if __name__ == "__main__":
    blocks = MdcConvertor("./signs_mapper.json", "G1-N29:Z7-D51:U9-N33:Z2")
    blocks.draw_image(font_size=200, storage_path="output.png")
