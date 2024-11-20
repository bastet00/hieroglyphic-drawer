from draw import Draw
from read import GenerateSmybols

if __name__ == "__main__":
    text = GenerateSmybols("./signs_mapper.json", "G1&D36&D58-X1:G37")
    drawer = Draw(font_size=40)

    for idx, block in enumerate(text.get_unicode_draw_array()):
        drawer.set_blocks(idx, block)

    drawer.draw()
