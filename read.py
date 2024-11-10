import json


class GenerateSmybols:
    def __init__(self, file_path):
        self.file_path = file_path
        # Mocking input after being mapped
        self.input = [["𓀀"], ["𓀻"], ["𓀿", "𓀿", "𓀿"], ["𓆑"]]


# def load_unicode_symbol_mapper(self):
#     """
#     @Returns parsed json file
#     """
#     with open(self.file_path, "r") as file:
#         return json.load(file)
#
# def map_code_to_symbols(self):
#     """
#     @Returns generated symbols depends on the input
#     """
#     unicode_as_symbol = ""
#     mapper = self.load_unicode_symbol_mapper()
#     for unicode in self.input:
#         unicode_as_symbol += mapper[unicode]
#
#     return unicode_as_symbol
