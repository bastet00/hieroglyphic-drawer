from draw import Draw
from read import GenerateSmybols

if __name__ == "__main__":
    text = GenerateSmybols("./signs_mapper.json")
    drawer = Draw(font_size=40)

    for idx, block in enumerate(text.input):
        drawer.set_blocks(idx, block)

    drawer.draw()
