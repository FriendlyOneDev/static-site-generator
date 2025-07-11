import re
from enum import Enum, auto
from htmlnode import *
from text_utils import *


class BlockType(Enum):
    PARAGRAPH = auto()
    HEADING = auto()
    CODE = auto()
    QUOTE = auto()
    UNORDERED_LIST = auto()
    ORDERED_LIST = auto()


def block_to_block_type(block):
    lines = block.split("\n")

    if block.startswith("```") and block.endswith("```"):
        return BlockType.CODE

    if re.match(r"#{1,6} ", lines[0]):
        return BlockType.HEADING

    if all(line.startswith(">") for line in lines):
        return BlockType.QUOTE

    if all(re.match(r"- ", line) for line in lines):
        return BlockType.UNORDERED_LIST

    for i, line in enumerate(lines, 1):
        if not re.match(rf"{i}\. ", line):
            break
    else:
        return BlockType.ORDERED_LIST

    return BlockType.PARAGRAPH


def markdown_to_html_node(markdown):
    blocks = markdown_to_blocks(markdown)
    block_nodes = []

    for block in blocks:
        block_type = block_to_block_type(block)
        tag = block_type_to_tag(block_type, block)

        match block_type:
            case BlockType.CODE:
                code_content = block.strip("`").strip()
                text_node = TextNode(code_content, TextType.CODE)
                child_node = text_node_to_html_node(text_node)
                block_node = ParentNode(tag, [child_node])

            case BlockType.HEADING:
                heading_text = re.sub(r"^#{1,6} ", "", block)
                children = text_to_children(heading_text)
                block_node = ParentNode(tag, children)

            case BlockType.QUOTE:
                quote_lines = [line.lstrip("> ").rstrip() for line in block.split("\n")]
                quote_text = " ".join(quote_lines)
                children = text_to_children(quote_text)
                block_node = ParentNode(tag, children)

            case BlockType.UNORDERED_LIST | BlockType.ORDERED_LIST:
                list_items = block.split("\n")
                list_nodes = []
                for item in list_items:
                    item_text = re.sub(r"^(-|\d+\.) ", "", item)
                    children = text_to_children(item_text)
                    list_nodes.append(ParentNode("li", children))
                block_node = ParentNode(tag, list_nodes)

            case BlockType.PARAGRAPH:
                children = text_to_children(block)
                block_node = ParentNode(tag, children)

            case _:
                raise ValueError(f"Unknown block type: {block_type}")

        block_nodes.append(block_node)

    return ParentNode("div", block_nodes)


def markdown_to_blocks(markdown):
    raw_blocks = re.split(r"\n\s*\n", markdown)
    clean_blocks = [block.strip() for block in raw_blocks if block.strip()]
    return clean_blocks


def block_type_to_tag(block_type, block):
    match block_type:
        case BlockType.PARAGRAPH:
            return "p"
        case BlockType.HEADING:
            level = 1
            match = re.match(r"(#{1,6}) ", block)
            if match:
                level = len(match.group(1))

            return f"h{level}"
        case BlockType.CODE:
            return "pre"
        case BlockType.QUOTE:
            return "blockquote"
        case BlockType.UNORDERED_LIST:
            return "ul"
        case BlockType.ORDERED_LIST:
            return "ol"


if __name__ == "__main__":
    md = """
### This is a heading

This is **bolded** paragraph

This is another paragraph with _italic_ text and `code` here
This is the same paragraph on a new line

- This is a list
- with items
"""
    print(markdown_to_blocks(md))
    for block in markdown_to_blocks(md):
        print(block_to_block_type(block))

    print("------------")

    print(markdown_to_html_node(md).to_html())
