import unittest
from block_utils import *


class TestMarkdownToBlocks(unittest.TestCase):

    def test_basic_paragraphs(self):
        md = """
This is **bolded** paragraph

This is another paragraph
"""
        expected = ["This is **bolded** paragraph", "This is another paragraph"]
        self.assertEqual(markdown_to_blocks(md), expected)

    def test_paragraph_with_newlines(self):
        md = """
First line
Second line

Third line
Fourth line
"""
        expected = ["First line\nSecond line", "Third line\nFourth line"]
        self.assertEqual(markdown_to_blocks(md), expected)

    def test_list_block(self):
        md = """
- Item 1
- Item 2
"""
        expected = ["- Item 1\n- Item 2"]
        self.assertEqual(markdown_to_blocks(md), expected)

    def test_mixed_content(self):
        md = """
This is **bolded** paragraph

This is another paragraph with _italic_ text and `code` here
This is the same paragraph on a new line

- This is a list
- with items
"""
        expected = [
            "This is **bolded** paragraph",
            "This is another paragraph with _italic_ text and `code` here\nThis is the same paragraph on a new line",
            "- This is a list\n- with items",
        ]
        self.assertEqual(markdown_to_blocks(md), expected)

    def test_leading_trailing_whitespace(self):
        md = "  \n\n  Paragraph with spaces  \n \n"
        expected = ["Paragraph with spaces"]
        self.assertEqual(markdown_to_blocks(md), expected)

    def test_empty_input(self):
        md = ""
        expected = []
        self.assertEqual(markdown_to_blocks(md), expected)


class TestBlockToBlockType(unittest.TestCase):

    def test_paragraph(self):
        block = "This is just a paragraph."
        self.assertEqual(block_to_block_type(block), BlockType.PARAGRAPH)

    def test_heading(self):
        block = "# Heading 1"
        self.assertEqual(block_to_block_type(block), BlockType.HEADING)

    def test_code(self):
        block = "```\ndef foo():\n    return 'bar'\n```"
        self.assertEqual(block_to_block_type(block), BlockType.CODE)

    def test_quote(self):
        block = "> Quote line 1\n> Quote line 2"
        self.assertEqual(block_to_block_type(block), BlockType.QUOTE)

    def test_unordered_list(self):
        block = "- Item 1\n- Item 2"
        self.assertEqual(block_to_block_type(block), BlockType.UNORDERED_LIST)

    def test_ordered_list(self):
        block = "1. First\n2. Second\n3. Third"
        self.assertEqual(block_to_block_type(block), BlockType.ORDERED_LIST)

    def test_ordered_list_wrong_start(self):
        block = "2. First\n3. Second"
        self.assertEqual(block_to_block_type(block), BlockType.PARAGRAPH)

    def test_unordered_list_with_indent(self):
        block = "- Item 1\n  - Subitem"
        self.assertEqual(
            block_to_block_type(block), BlockType.PARAGRAPH
        )  # because not all lines match pattern


class TestMarkdownToHtml(unittest.TestCase):
    def test_single_paragraph(self):
        md = "This is a simple paragraph."
        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(html, "<div><p>This is a simple paragraph.</p></div>")

    def test_paragraph_with_formatting(self):
        md = "This is **bold**, _italic_, and `code`."
        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><p>This is <b>bold</b>, <i>italic</i>, and <code>code</code>.</p></div>",
        )

    def test_multiple_paragraphs(self):
        md = """
First paragraph.

Second **bold** paragraph.
"""
        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><p>First paragraph.</p><p>Second <b>bold</b> paragraph.</p></div>",
        )

    def test_code_block(self):
        md = """
        ```
some_code()
with_multiple_lines()
        ```
        """
        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><pre><code>some_code()\nwith_multiple_lines()</code></pre></div>",
        )

    def test_heading(self):
        md = "### This is a heading"
        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(html, "<div><h3>This is a heading</h3></div>")

    def test_quote_block(self):
        md = """
> This is a quote
> across two lines
"""
        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html, "<div><blockquote>This is a quote across two lines</blockquote></div>"
        )

    def test_unordered_list(self):
        md = """
- Item one
- Item two
"""
        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(html, "<div><ul><li>Item one</li><li>Item two</li></ul></div>")

    def test_ordered_list(self):
        md = """
1. First item
2. Second item
"""
        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html, "<div><ol><li>First item</li><li>Second item</li></ol></div>"
        )

    def test_mixed_content(self):
        md = """
### Heading

This is _italic_ and **bold**.

- List item one
- List item two
"""
        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><h3>Heading</h3><p>This is <i>italic</i> and <b>bold</b>.</p><ul><li>List item one</li><li>List item two</li></ul></div>",
        )


if __name__ == "__main__":
    unittest.main()
