import json


class GenerateSmybols:
    def __init__(self, file_path, mdc):
        """

        @param file_path: path to the json file
        @param mdc: MDC code ie: "G1&X1-F9" or "G1-D36:D36-D51:D40" or "G1-D36&D58-X1:G37"
        """
        self.file_path = file_path
        self.mdc = mdc
        with open(self.file_path, "r") as file:
            self.mapper = json.load(file)


        # self.input = [
        #     ["𓄿", "𓄇", "𓏏"],
        #     ["𓄿"],
        #     ["𓏯", "𓏏"],
        #     ["𓇳"],
        #     ["𓏤"],
        #     ["𓄿"],
        #     ["𓄿", "𓄿", "𓇳"],
        #     ["𓂝", "𓂝", "𓏏"],
        #     ["𓂡", "𓂡", "𓏏"],
        #     ["𓂡", "𓂷", "𓇳"],
        #     ["𓌙"],
        #     ["𓄑"],
        #     ["𓀁"],
        # ]

    def _convert_mdc_to_nested_array(self):
        symbolBlocks = self.mdc.split("-")
        for i in range(len(symbolBlocks)):
            if ":" in symbolBlocks[i]:
                symbolBlocks[i] = symbolBlocks[i].split(":")
            if "&" in symbolBlocks[i]:
                symbolBlocks[i] = symbolBlocks[i].split("&")
        return symbolBlocks
    
    def get_unicode_draw_array(self):
        unicode_array = []
        for symbolBlock in self._convert_mdc_to_nested_array():
            if isinstance(symbolBlock, list):
                unicode_array.append([ self.mapper[symbol] for symbol in symbolBlock])
            else:
                unicode_array.append(self.mapper[symbolBlock])
        return unicode_array
            
    # def load_unicode_symbol_mapper(self):
    #     """
    #     @Returns parsed json file
    #     """
    #     with open(self.file_path, "r") as file:
    #         return json.load(file)

    # def map_code_to_symbols(self):
    #     """
    #     @Returns generated symbols depends on the input
    #     """
    #     unicode_as_symbol = ""
    #     mapper = self.load_unicode_symbol_mapper()
    #     for unicode in self.input:
    #         unicode_as_symbol += mapper[unicode]

    #     return unicode_as_symbol
