from draw import Draw
from read import BlocksGenerator

if __name__ == "__main__":
    generator = BlocksGenerator("./signs_mapper.json", "R15-D58-D46:Z7*O49")

    blocks = generator.unicode_to_draw_array()
    drawer = Draw(font_size=40)

    for idx, block in enumerate(blocks):
        drawer.set_blocks(idx, block)

    drawer.draw()
