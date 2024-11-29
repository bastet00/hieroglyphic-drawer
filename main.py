from draw import Draw
from read import BlocksGenerator
from time import sleep

if __name__ == "__main__":

    foo = [
        BlocksGenerator("./signs_mapper.json", "F40-G43-X1:Y1"),
        BlocksGenerator("./signs_mapper.json", "F40:X1*F34"),
        BlocksGenerator("./signs_mapper.json", "F40-G43-X1:Y1:Z2-F34:Z2-N33:Z2"),
        BlocksGenerator("./signs_mapper.json", "F40-X1&G43-Y1:Z2-D36:Z1"),
        BlocksGenerator("./signs_mapper.json", "F40-Z7-Y1"),
        BlocksGenerator("./signs_mapper.json", "R15-D58-D54"),
        BlocksGenerator("./signs_mapper.json", "U23-D58-X1:N25"),
        BlocksGenerator("./signs_mapper.json", "U23-D58-X1-A1-B1-Z2"),
        #
        BlocksGenerator("./signs_mapper.json", "U23-D58-Z7-W7:N25-O49"),
        BlocksGenerator("./signs_mapper.json", "U23-D58-G43-E26"),
        BlocksGenerator("./signs_mapper.json", "U23-D58-G43-X1-A53"),
        BlocksGenerator("./signs_mapper.json", "U23-D58-D58-Z5:D54"),
        BlocksGenerator("./signs_mapper.json", "U23-D58-N35:Z4-N35:Z4-G39"),
        BlocksGenerator("./signs_mapper.json", "U23-D58-Aa1:Z9"),
        BlocksGenerator("./signs_mapper.json", "N11"),
        BlocksGenerator("./signs_mapper.json", "R15-D58-D46:Z7*O49"),
        #
        BlocksGenerator("./signs_mapper.json", "G1-D21:T12"),
        BlocksGenerator("./signs_mapper.json", "G1-O4:D46-A2"),
        BlocksGenerator("./signs_mapper.json", "G1&N21-V28"),
        BlocksGenerator("./signs_mapper.json", "G1-V28-X1:N23-Z1-Z3a"),
        BlocksGenerator(
            "./signs_mapper.json", "G1-X1:N21:Z1-N35:G1-Aa1:X1*U30-G1&Z7-T14-N25:Z2"
        ),
        BlocksGenerator("./signs_mapper.json", "G1-V28-U6-O6-X1:O1"),
        #
        BlocksGenerator("./signs_mapper.json", "G25&Aa1"),
        BlocksGenerator("./signs_mapper.json", "Z7-G25&Aa1-T30"),
        BlocksGenerator("./signs_mapper.json", "G25-Aa1:Y1"),
        BlocksGenerator("./signs_mapper.json", "M8:X1"),
        BlocksGenerator("./signs_mapper.json", "G25&Aa1-X1:Y1:Z2"),
        BlocksGenerator("./signs_mapper.json", "G1-V28-U6-O6-X1:O1"),
        BlocksGenerator("./signs_mapper.json", "G25-Aa1:Y1-A53-A40"),
    ]

    for fo in foo:
        blocks = fo.unicode_to_draw_array()
        drawer = Draw()

        for idx, block in enumerate(blocks):
            drawer.set_blocks(idx, block)

        drawer.draw()
        sleep(3)

    # generator = BlocksGenerator("./signs_mapper.json", "G25&Aa1-X1:Y1:Z2")
    #
    # blocks = generator.unicode_to_draw_array()
    # drawer = Draw()
    # for idx, block in enumerate(blocks):
    #     drawer.set_blocks(idx, block)
    #
    # drawer.draw()
