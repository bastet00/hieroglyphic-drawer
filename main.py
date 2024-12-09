from draw import Draw
from read import BlocksGenerator

if __name__ == "__main__":
    blocks = BlocksGenerator("./signs_mapper.json", "B1-G39-X1-B1-I6-G17-X1:O49").unicode_to_draw_array()
    drawer = Draw()

    for idx, block in enumerate(blocks):
        drawer.set_blocks(idx, block)

    drawer.draw()