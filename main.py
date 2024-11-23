from draw import Draw
from read import BlocksGenerator

if __name__ == "__main__":
    generator = BlocksGenerator(
        "./signs_mapper.json", "F40-G43-X1:Y1:Z2-F34:Z2-N33:Z2*X1"
    )
    generator.unicode_to_draw_array()
    drawer = Draw(font_size=40)

    # for idx, block in enumerate(text.get_unicode_draw_array()):
    #     drawer.set_blocks(idx, block)
    #
    # drawer.draw()
