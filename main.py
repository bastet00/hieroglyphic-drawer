from read import BlocksGenerator

if __name__ == "__main__":
    blocks = BlocksGenerator("./signs_mapper.json", "B1-G39-X1-B1-I6-G17-X1:O49:O49")
    blocks.draw_image(font_size=200, storage_path="output.png")
