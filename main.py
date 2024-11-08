from draw import Draw
from read import GenerateSmybols

if __name__ == "__main__":
    text = GenerateSmybols("./signs_mapper.json").map_code_to_symbols()
    Draw(text=text, font_size=30).draw()
