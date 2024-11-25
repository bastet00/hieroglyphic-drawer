import json
import inspect
import sys


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
        self.signs = ["*", ":", "&"]

    def unicode_map_error(self, e):
        stack = inspect.stack()
        caller = stack[1].function
        print("Could not map unicode to a symbol", e)
        print(f"Caller function: {caller}")
        sys.tracebacklimit = 0
        raise

    def _convert_mdc_to_nested_array(self):
        return self.mdc.split("-")

    def pre_convertor(self, mdc):
        """
        Returns an array of indexes mapped to each special char
        in the same order they appear in the input string.
        """
        char_idxs = []

        for idx, char in enumerate(mdc):
            if char in self.signs:
                char_idxs.append(idx)

        return char_idxs

    def detect_draw_type(self, mdc, spchar_idxs):
        """
        Draw type detector.

        Add a new detecting spcial character by adding the char in self.sign.

        WARNING: return value has to be the same as a function,
        that is going to be implemented in Draw class which,
        specifies the draw technique.

        NOTE: keep in mind that one block could has multiple special chars
        """
        match mdc:
            case _ if "*" in mdc:
                return "compose"
            case _ if "*" not in mdc and ":" in mdc:
                return "vertical_draw"
            case _ if "&" in mdc:
                return "second_on_top"
            case _:
                return "stand_alone"

    def create_block_object(self, spchar_idxs, num_of_symbols, mdc):
        block_object = {"draw_type": "", "draw_info": []}
        i = 0
        start = 0
        temp = 0
        block_object["draw_type"] = self.detect_draw_type(mdc, spchar_idxs)

        for symbol in range(num_of_symbols):
            unicode = mdc[start : spchar_idxs[i] if i != len(spchar_idxs) else None]
            try:
                block_object["draw_info"].append({"symbol": self.mapper[unicode]})
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
            spcial_chars_idxs = self.pre_convertor(mdc)
            num_of_symbols = len(spcial_chars_idxs) + 1
            block_object = self.create_block_object(
                spcial_chars_idxs, num_of_symbols, mdc
            )
            unicode_array.append(block_object)

        return unicode_array
