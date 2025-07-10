import unittest
from textnode import TextNode, TextType
from text_utils import (
    text_to_textnodes,
    split_nodes_delimiter,
    split_nodes_image,
    split_nodes_link,
    extract_markdown_images,
    extract_markdown_links,
)


class TestSplitNodesDelimiter(unittest.TestCase):

    def test_basic_bold_split(self):
        nodes = [TextNode("This is **bold** text", TextType.TEXT)]
        result = split_nodes_delimiter(nodes, "**", TextType.BOLD)
        expected = [
            TextNode("This is ", TextType.TEXT),
            TextNode("bold", TextType.BOLD),
            TextNode(" text", TextType.TEXT),
        ]
        self.assertEqual(result, expected)

    def test_multiple_bold_sections(self):
        nodes = [TextNode("**bold1** then **bold2**", TextType.TEXT)]
        result = split_nodes_delimiter(nodes, "**", TextType.BOLD)
        expected = [
            TextNode("bold1", TextType.BOLD),
            TextNode(" then ", TextType.TEXT),
            TextNode("bold2", TextType.BOLD),
        ]
        self.assertEqual(result, expected)

    def test_no_delimiter(self):
        nodes = [TextNode("plain text", TextType.TEXT)]
        result = split_nodes_delimiter(nodes, "**", TextType.BOLD)
        self.assertEqual(result, nodes)

    def test_unmatched_delimiter_raises(self):
        nodes = [TextNode("This is **not closed", TextType.TEXT)]
        with self.assertRaises(ValueError):
            split_nodes_delimiter(nodes, "**", TextType.BOLD)

    def test_skips_non_text_nodes(self):
        input_node = TextNode("click me", TextType.LINK, url="https://example.com")
        nodes = [input_node]
        result = split_nodes_delimiter(nodes, "**", TextType.BOLD)
        self.assertEqual(result, [input_node])

    def test_empty_sections_are_skipped(self):
        nodes = [TextNode("**bold**", TextType.TEXT)]
        result = split_nodes_delimiter(nodes, "**", TextType.BOLD)
        expected = [TextNode("bold", TextType.BOLD)]
        self.assertEqual(result, expected)

    def test_mixed_empty_and_valid(self):
        nodes = [TextNode("A ** ** B **C**", TextType.TEXT)]
        result = split_nodes_delimiter(nodes, "**", TextType.BOLD)
        expected = [
            TextNode("A ", TextType.TEXT),
            TextNode(" ", TextType.BOLD),
            TextNode(" B ", TextType.TEXT),
            TextNode("C", TextType.BOLD),
        ]
        self.assertEqual(result, expected)


class TestMarkdownExtractors(unittest.TestCase):

    def test_extract_single_image(self):
        text = "This is an image ![alt text](image.png)"
        result = extract_markdown_images(text)
        self.assertEqual(result, [("alt text", "image.png")])

    def test_extract_multiple_images(self):
        text = "First ![img1](a.png) and second ![img2](b.jpg)"
        result = extract_markdown_images(text)
        self.assertEqual(result, [("img1", "a.png"), ("img2", "b.jpg")])

    def test_extract_image_with_empty_alt(self):
        text = "![  ](img.png)"
        result = extract_markdown_images(text)
        self.assertEqual(result, [("  ", "img.png")])

    def test_extract_image_with_url_spaces(self):
        text = "![alt](folder name/img.png)"
        result = extract_markdown_images(text)
        self.assertEqual(result, [("alt", "folder name/img.png")])

    def test_extract_image_malformed(self):
        text = "![alt(image.png) and ![text](img.png"
        result = extract_markdown_images(text)
        self.assertEqual(result, [])  # no valid match

    def test_extract_single_link(self):
        text = "This is a [link](https://example.com)"
        result = extract_markdown_links(text)
        self.assertEqual(result, [("link", "https://example.com")])

    def test_extract_multiple_links(self):
        text = "[Google](https://google.com) and [GitHub](https://github.com)"
        result = extract_markdown_links(text)
        self.assertEqual(
            result, [("Google", "https://google.com"), ("GitHub", "https://github.com")]
        )

    def test_extract_link_with_nested_exclamation(self):
        text = "Text ![image](pic.png) and [link](url.com)"
        result = extract_markdown_links(text)
        self.assertEqual(result, [("link", "url.com")])  # image shouldn't match

    def test_extract_link_malformed(self):
        text = "[link(url.com) and [text](url.com"
        result = extract_markdown_links(text)
        self.assertEqual(result, [])  # malformed

    def test_extract_link_with_brackets_in_text(self):
        text = "[a [b]](url.com)"
        result = extract_markdown_links(text)
        self.assertEqual(result, [])  # nested brackets are not supported


class TestSplitNodesImage(unittest.TestCase):
    def test_no_image(self):
        nodes = [TextNode("Hello world", TextType.TEXT)]
        result = split_nodes_image(nodes)
        self.assertEqual(result, [TextNode("Hello world", TextType.TEXT)])

    def test_single_image(self):
        nodes = [TextNode("Look at this ![cat](cat.jpg)", TextType.TEXT)]
        result = split_nodes_image(nodes)
        self.assertEqual(
            result,
            [
                TextNode("Look at this ", TextType.TEXT),
                TextNode("cat", TextType.IMAGE, "cat.jpg"),
            ],
        )

    def test_image_at_start(self):
        nodes = [TextNode("![dog](dog.jpg) is cute", TextType.TEXT)]
        result = split_nodes_image(nodes)
        self.assertEqual(
            result,
            [
                TextNode("dog", TextType.IMAGE, "dog.jpg"),
                TextNode(" is cute", TextType.TEXT),
            ],
        )

    def test_multiple_images(self):
        nodes = [TextNode("![a](a.png) middle ![b](b.png)", TextType.TEXT)]
        result = split_nodes_image(nodes)
        self.assertEqual(
            result,
            [
                TextNode("a", TextType.IMAGE, "a.png"),
                TextNode(" middle ", TextType.TEXT),
                TextNode("b", TextType.IMAGE, "b.png"),
            ],
        )

    def test_mixed_node_types_preserved(self):
        nodes = [
            TextNode("![a](a.png)", TextType.TEXT),
            TextNode("Already a link", TextType.LINK, "example.com"),
        ]
        result = split_nodes_image(nodes)
        self.assertEqual(
            result,
            [
                TextNode("a", TextType.IMAGE, "a.png"),
                TextNode("Already a link", TextType.LINK, "example.com"),
            ],
        )


class TestSplitNodesLink(unittest.TestCase):
    def test_no_link(self):
        nodes = [TextNode("No links here", TextType.TEXT)]
        result = split_nodes_link(nodes)
        self.assertEqual(result, [TextNode("No links here", TextType.TEXT)])

    def test_single_link(self):
        nodes = [TextNode("Click [here](link.com)", TextType.TEXT)]
        result = split_nodes_link(nodes)
        self.assertEqual(
            result,
            [
                TextNode("Click ", TextType.TEXT),
                TextNode("here", TextType.LINK, "link.com"),
            ],
        )

    def test_link_at_start(self):
        nodes = [TextNode("[Start](url) then text", TextType.TEXT)]
        result = split_nodes_link(nodes)
        self.assertEqual(
            result,
            [
                TextNode("Start", TextType.LINK, "url"),
                TextNode(" then text", TextType.TEXT),
            ],
        )

    def test_multiple_links(self):
        nodes = [TextNode("Go [here](1.com) or [there](2.com)", TextType.TEXT)]
        result = split_nodes_link(nodes)
        self.assertEqual(
            result,
            [
                TextNode("Go ", TextType.TEXT),
                TextNode("here", TextType.LINK, "1.com"),
                TextNode(" or ", TextType.TEXT),
                TextNode("there", TextType.LINK, "2.com"),
            ],
        )

    def test_mixed_node_types_preserved(self):
        nodes = [
            TextNode("[x](1.com)", TextType.TEXT),
            TextNode("Just code", TextType.CODE),
        ]
        result = split_nodes_link(nodes)
        self.assertEqual(
            result,
            [
                TextNode("x", TextType.LINK, "1.com"),
                TextNode("Just code", TextType.CODE),
            ],
        )


class TestTextToTextNodes(unittest.TestCase):

    def test_plain_text(self):
        text = "Just plain text"
        result = text_to_textnodes(text)
        self.assertEqual(result, [TextNode("Just plain text", TextType.TEXT)])

    def test_bold_text(self):
        text = "This is **bold** text"
        result = text_to_textnodes(text)
        self.assertEqual(
            result,
            [
                TextNode("This is ", TextType.TEXT),
                TextNode("bold", TextType.BOLD),
                TextNode(" text", TextType.TEXT),
            ],
        )

    def test_italic_text(self):
        text = "This is _italic_ text"
        result = text_to_textnodes(text)
        self.assertEqual(
            result,
            [
                TextNode("This is ", TextType.TEXT),
                TextNode("italic", TextType.ITALIC),
                TextNode(" text", TextType.TEXT),
            ],
        )

    def test_code_text(self):
        text = "Here is `code`"
        result = text_to_textnodes(text)
        self.assertEqual(
            result,
            [
                TextNode("Here is ", TextType.TEXT),
                TextNode("code", TextType.CODE),
            ],
        )

    def test_image(self):
        text = "Here is an image ![cat](cat.jpg)"
        result = text_to_textnodes(text)
        self.assertEqual(
            result,
            [
                TextNode("Here is an image ", TextType.TEXT),
                TextNode("cat", TextType.IMAGE, "cat.jpg"),
            ],
        )

    def test_link(self):
        text = "Click [here](https://example.com) for info"
        result = text_to_textnodes(text)
        self.assertEqual(
            result,
            [
                TextNode("Click ", TextType.TEXT),
                TextNode("here", TextType.LINK, "https://example.com"),
                TextNode(" for info", TextType.TEXT),
            ],
        )

    def test_combined_formatting(self):
        text = "**Bold** and _italic_ and `code`"
        result = text_to_textnodes(text)
        self.assertEqual(
            result,
            [
                TextNode("Bold", TextType.BOLD),
                TextNode(" and ", TextType.TEXT),
                TextNode("italic", TextType.ITALIC),
                TextNode(" and ", TextType.TEXT),
                TextNode("code", TextType.CODE),
            ],
        )

    def test_image_and_link(self):
        text = "![dog](dog.png) and [Google](https://google.com)"
        result = text_to_textnodes(text)
        self.assertEqual(
            result,
            [
                TextNode("dog", TextType.IMAGE, "dog.png"),
                TextNode(" and ", TextType.TEXT),
                TextNode("Google", TextType.LINK, "https://google.com"),
            ],
        )

    def test_nested_ignored(self):
        text = "This is **not _nested_** correctly"
        result = text_to_textnodes(text)
        self.assertEqual(
            result,
            [
                TextNode("This is ", TextType.TEXT),
                TextNode("not _nested_", TextType.BOLD),
                TextNode(" correctly", TextType.TEXT),
            ],
        )

    def test_unmatched_delimiter_raises(self):
        text = "Unclosed **bold"
        with self.assertRaises(ValueError):
            text_to_textnodes(text)

    def test_empty_string(self):
        result = text_to_textnodes("")
        self.assertEqual(result, [])


if __name__ == "__main__":
    unittest.main()
