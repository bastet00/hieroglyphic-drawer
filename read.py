import json


class GenerateSmybols:
    def __init__(self, file_path):
        self.file_path = file_path

        self.input = [
            ["𓄿", "𓄇", "𓏏"],
            ["𓄿"],
            ["𓏯", "𓏏"],
            ["𓇳"],
            ["𓏤"],
            ["𓄿"],
            ["𓄿", "𓄿", "𓇳"],
            ["𓂝", "𓂝", "𓏏"],
            ["𓂡", "𓂡", "𓏏"],
            ["𓂡", "𓂷", "𓇳"],
            ["𓌙"],
            ["𓄑"],
            ["𓀁"],
        ]

    def load_unicode_symbol_mapper(self):
        """
        @Returns parsed json file
        """
        with open(self.file_path, "r") as file:
            return json.load(file)

    def map_code_to_symbols(self):
        """
        @Returns generated symbols depends on the input
        """
        unicode_as_symbol = ""
        mapper = self.load_unicode_symbol_mapper()
        for unicode in self.input:
            unicode_as_symbol += mapper[unicode]

        return unicode_as_symbol
