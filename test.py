import unittest
from read import MdcConvertor


class MdcConverterTest(unittest.TestCase):
    def test_convert_mdc_to_unicode__should_return_right_unicode(self):
        mdcConverter = MdcConverter("A1-B1")
        hieroglyphics_unicode = mdcConverter.to_unicode()
        self.self.assertEqual(hieroglyphics_unicode, "𓀀𓁐")

    def test_convert_mdc_to_image(self):
        mdcConverter = MdcConverter("A1-B1")
        hieroglyphics_unicode = mdcConverter.to_image(size=(100, 100))
        # assert image is created or so


class BlockTest(unittest.TestCase):
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

    def test_raise_key_error(self):
        generator = MdcConvertor("./signs_mapper.json", "Z100")
        with self.assertRaises(KeyError):
            generator.unicode_to_draw_array()

    def test_vertical_draw_block(self):
        generator = MdcConvertor("./signs_mapper.json", "F40:X1:F34")
        blocks = generator.unicode_to_draw_array()
        self.assertEqual(blocks[0]["draw_type"], "vertical_draw")

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
            self.assertEqual(block["draw_type"], "vertical_draw")
        compose = blocks[-1]
        self.assertEqual(compose["draw_type"], "compose")


if __name__ == "__main__":
    unittest.main()
