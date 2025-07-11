import unittest

from main import *


class TestExtractTitle(unittest.TestCase):

    def test_valid_title(self):
        self.assertEqual(extract_title("# My Title"), "My Title")

    def test_valid_title_with_whitespace(self):
        self.assertEqual(extract_title("   #   My Title   "), "My Title")

    def test_multiple_hashes(self):
        with self.assertRaises(Exception):
            extract_title("## Not a valid H1")

    def test_no_hash(self):
        with self.assertRaises(Exception):
            extract_title("Just text with no header")

    def test_header_on_second_line(self):
        with self.assertRaises(Exception):
            extract_title("Text\n# Real Header")


if __name__ == "__main__":
    unittest.main()
