import unittest

from textnode import TextNode, TextType


class TestTextNode(unittest.TestCase):
    def test_eq_identical_values(self):
        """Two nodes with identical constructor args compare equal."""
        self.assertEqual(
            TextNode("spam", TextType.PLAIN), TextNode("spam", TextType.PLAIN)
        )

    def test_eq_transitive(self):
        """Transitivity: if a==b and b==c, then a==c."""
        a = TextNode("alpha", TextType.ITALIC)
        b = TextNode("alpha", TextType.ITALIC)
        c = TextNode("alpha", TextType.ITALIC)
        self.assertEqual(a, b)
        self.assertEqual(b, c)
        self.assertEqual(a, c)

    def test_neq_text(self):
        """Different text strings → not equal."""
        self.assertNotEqual(
            TextNode("one", TextType.PLAIN), TextNode("two", TextType.PLAIN)
        )

    def test_neq_text_type(self):
        """Different enum values → not equal."""
        self.assertNotEqual(
            TextNode("same", TextType.BOLD), TextNode("same", TextType.ITALIC)
        )

    def test_neq_url(self):
        """Different URL values (including None vs str) → not equal."""
        self.assertNotEqual(
            TextNode("link text", TextType.LINK, "https://a.example"),
            TextNode("link text", TextType.LINK, "https://b.example"),
        )
        self.assertNotEqual(
            TextNode("img", TextType.IMAGE, None),
            TextNode("img", TextType.IMAGE, "https://example/img.png"),
        )

    def test_eq_with_url(self):
        """Identical text, type and url should be equal."""
        self.assertEqual(
            TextNode("Google it!", TextType.LINK, "https://www.google.com"),
            TextNode("Google it!", TextType.LINK, "https://www.google.com"),
        )


if __name__ == "__main__":
    unittest.main()
