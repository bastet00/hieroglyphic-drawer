import unittest
from handlers.convertor import MdcConvertor


class ConvertorTest(unittest.TestCase):
    """
    Test drawing types to the input
    """

    def test_stand_alone_block(self):
        generator = MdcConvertor("./signs_mapper.json", "F40-G43")
        blocks = generator.unicode_to_draw_array()
        for block in blocks:
            self.assertEqual(block["draw_type"], "stand_alone")

    def test_compose_block(self):
        generator = MdcConvertor("./signs_mapper.json", "F40:X1*F34")
        blocks = generator.unicode_to_draw_array()
        self.assertEqual(blocks[0]["draw_type"], "compose")

    def test_vertical_block(self):
        generator = MdcConvertor("./signs_mapper.json", "F40:X1:F34")
        blocks = generator.unicode_to_draw_array()
        self.assertEqual(blocks[0]["draw_type"], "vertical")

    def test_compose_up_block(self):
        generator = MdcConvertor("./signs_mapper.json", "F40*X1:F34")
        blocks = generator.unicode_to_draw_array()
        self.assertEqual(blocks[0]["draw_type"], "compose_up")

    def test_multiple_block(self):
        generator = MdcConvertor(
            "./signs_mapper.json", "F40-G43-X1:Y1:Z2-F34:Z2-N33:Z2*X1"
        )
        blocks = generator.unicode_to_draw_array()
        stand_alone = blocks[0:2]
        for block in stand_alone:
            self.assertEqual(block["draw_type"], "stand_alone")
        vertical_draw = blocks[2:4]
        for block in vertical_draw:
            self.assertEqual(block["draw_type"], "vertical")
        compose = blocks[-1]
        self.assertEqual(compose["draw_type"], "compose")


if __name__ == "__main__":
    unittest.main()
