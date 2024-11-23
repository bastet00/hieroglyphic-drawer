import json
import inspect
import sys

"""
    Analyze what special characters mean to a compiler function.

        - `-` : Mark a new block

        - `:` : Stack symbols vertically where the first one at the top,
        the next one(s) vertically down

        - `*` : Holds two elements horizontally next to each other,
        with one other symbol centered above

        - `##` : Symbol in the middle of a symbol,
        symbol x inside symbol y
"""


class BlocksGenerator:
    def __init__(self, file_path, mdc):
        """
        @param file_path: path to the json file
        @param mdc: MDC code ie: "G1&X1-F9" or "G1-D36:D36-D51:D40" or "G1-D36&D58-X1:G37"
        """
        self.file_path = file_path
        self.mdc = mdc
        with open(self.file_path, "r") as file:
            self.mapper = json.load(file)

        # order matters
        self.signs = {
            "vertical_draw": ":",
            "compose": "*",
        }

    def unicode_map_error(self, e):
        stack = inspect.stack()
        caller = stack[1].function
        print("Could not map unicode to a symbol", e)
        print("Caller:", caller)
        sys.tracebacklimit = 0
        raise

    def _convert_mdc_to_nested_array(self):
        for char in self.mdc:
            if char == "&":
                self.mdc = self.mdc.replace(char, "-")
        return self.mdc.split("-")

    def handle_convert(self, mdc, char_idxs=None):
        if char_idxs is None:
            char_idxs = []

        # stop recursion if string doesn't have special chars or its too short
        if len(mdc) <= 2 or len(mdc) == 0:
            return char_idxs

        idx = 0
        for sign in self.signs.keys():
            founded_at = mdc.find(self.signs[sign])
            if founded_at != -1:
                prev = char_idxs[len(char_idxs) - 1] + 1 if len(char_idxs) else 0
                char_idxs.append(founded_at + prev)
                idx = founded_at
                break

        return self.handle_convert(mdc[idx + 1 :], char_idxs) if idx != 0 else char_idxs

    def detect_draw_type(self, mdc):
        match mdc:
            case _ if "*" in mdc:
                return "compose"
            case _ if "*" not in mdc:
                return "vertical_draw"
            case _:
                raise ValueError("Could not detect a draw type")

    def create_block_object(self, spchar_idxs, num_of_symbols, mdc):
        block_object = {"draw_type": "", "symbols": []}
        i = 0
        start = 0
        temp = 0
        block_object["draw_type"] = self.detect_draw_type(mdc)

        for symbol in range(num_of_symbols):
            unicode = mdc[start : spchar_idxs[i] if i != len(spchar_idxs) else None]
            try:
                block_object["symbols"].append(self.mapper[unicode])
            except KeyError as e:
                self.unicode_map_error(e)

            if len(spchar_idxs) > i:
                temp = spchar_idxs[i] + 1
                i += 1
                start = temp
        return block_object

    def unicode_to_draw_array(self):
        unicode_array = []
        mdcs = self._convert_mdc_to_nested_array()
        for mdc in mdcs:
            idxs = self.handle_convert(mdc)
            symbols = len(idxs)
            if symbols == 0:
                try:
                    unicode_array.append(self.mapper[mdc])
                except KeyError as e:
                    self.unicode_map_error(e)
            else:
                symbols += 1
                block_object = self.create_block_object(idxs, symbols, mdc)
                unicode_array.append(block_object)

        return unicode_array
