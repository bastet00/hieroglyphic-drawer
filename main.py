from draw import Draw
from read import BlocksGenerator

if __name__ == "__main__":
    blocks = BlocksGenerator("./signs_mapper.json", "B1-G39-X1:O49:O49")
    blocks.draw_image(150)
