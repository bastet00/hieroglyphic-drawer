from draw import Draw
from read import GenerateSmybols

if __name__ == "__main__":
    text = GenerateSmybols("./signs_mapper.json")
    # drawer = Draw(text="Hello World", font_size=30).draw()
    drawer = Draw(font_size=40)

    # self.input = [
    #       ["𓇋", "𓇋", "𓅱"]
    #     , ["𓆑", "𓇋"]
    #     , ["𓇋", "𓅱", "𓋿"]
    #     , ["𓆑"]
    # ]
    drawer.set_blocks(0, text.input[0])
    drawer.set_blocks(1, text.input[1])
    drawer.set_blocks(2, text.input[2])
    drawer.set_blocks(3, text.input[3])
    drawer.draw()
