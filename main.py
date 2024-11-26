from draw import Draw
from read import BlocksGenerator

if __name__ == "__main__":

    # generator = BlocksGenerator("./signs_mapper.json", "G1-N29:Z7-D51:U9-N33:Z2")
    # generator = BlocksGenerator("./signs_mapper.json", "M17-A2-D4:D21-G29&V31-A1")

    # generator = BlocksGenerator(
    #     "./signs_mapper.json", "G1-X1:N21:Z1-N35:G1-Aa1:X1*U30-G1&Z7-T14-N25:Z2"
    # )

    # generator = BlocksGenerator("./signs_mapper.json", "R15-D58-G4-A1*B1:Z2")
    # generator = BlocksGenerator(
    #     "./signs_mapper.json", "M17-D36:N35a-Z7-N36-X1:Aa2-F4:X1*Z1-F34-Z3a"
    # )

    # generator = BlocksGenerator(
    #     "./signs_mapper.json", "N36:N23-M17-X1*Z7:D21-N35a-N36:N23-O49"
    # )

    generator = BlocksGenerator("./signs_mapper.json", "N18:N23-Z1-D21:D46-Z7-T12-O49")

    blocks = generator.unicode_to_draw_array()
    drawer = Draw(font_size=40)

    for idx, block in enumerate(blocks):
        drawer.set_blocks(idx, block)

    drawer.draw()
