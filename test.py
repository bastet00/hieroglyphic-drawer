import unittest
from read import BlocksGenerator


class BlockTest(unittest.TestCase):
    """
    Test drawing types to the input
    """

    def test_stand_alone_block(self):
        generator = BlocksGenerator("./signs_mapper.json", "F40-G43")
        blocks = generator.unicode_to_draw_array()
        for block in blocks:
            self.assertIsInstance(block, str)

    def test_compose_block(self):
        generator = BlocksGenerator("./signs_mapper.json", "F40:X1*F34")
        blocks = generator.unicode_to_draw_array()
        self.assertEqual(blocks[0]["draw_type"], "compose")

    def test_raise_key_error(self):
        generator = BlocksGenerator("./signs_mapper.json", "Z100")
        with self.assertRaises(KeyError):
            generator.unicode_to_draw_array()

    def test_vertical_draw_block(self):
        generator = BlocksGenerator("./signs_mapper.json", "F40:X1:F34")
        blocks = generator.unicode_to_draw_array()
        self.assertEqual(blocks[0]["draw_type"], "vertical_draw")

    def test_multiple_block(self):
        generator = BlocksGenerator(
            "./signs_mapper.json", "F40-G43-X1:Y1:Z2-F34:Z2-N33:Z2*X1"
        )
        blocks = generator.unicode_to_draw_array()
        stand_alone = blocks[0:2]
        for block in stand_alone:
            self.assertIsInstance(block, str)
        vertical_draw = blocks[2:4]
        for block in vertical_draw:
            self.assertEqual(block["draw_type"], "vertical_draw")
        compose = blocks[-1]
        self.assertEqual(compose["draw_type"], "compose")


if __name__ == "__main__":
    unittest.main()
