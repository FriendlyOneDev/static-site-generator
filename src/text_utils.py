from textnode import TextNode, TextType
import re


def split_nodes_delimiter(old_nodes, delimiter, text_type):
    new_nodes = []
    for node in old_nodes:
        if node.text_type != TextType.TEXT:
            new_nodes.append(node)
            continue

        split_text = node.text.split(delimiter)
        if len(split_text) % 2 == 0:
            raise ValueError(
                f"Invalid markdown syntax: unmatched delimiter {delimiter}"
            )

        for i in range(len(split_text)):
            if split_text[i] == "":
                continue
            if i % 2 == 0:
                new_nodes.append(TextNode(split_text[i], TextType.TEXT))
            else:
                new_nodes.append(TextNode(split_text[i], text_type))
    return new_nodes


def split_nodes_image(old_nodes):
    new_nodes = []
    for node in old_nodes:
        if node.text_type != TextType.TEXT:
            new_nodes.append(node)
            continue

        remaining_text = node.text
        images = extract_markdown_images(remaining_text)
        if not images:
            new_nodes.append(node)
            continue

        for alt_text, image_url in images:
            parts = remaining_text.split(f"![{alt_text}]({image_url})", 1)
            if len(parts) != 2:
                continue

            before_text = parts[0]
            remaining_text = parts[1]

            if before_text:
                new_nodes.append(TextNode(before_text, TextType.TEXT))

            if alt_text:
                new_nodes.append(TextNode(alt_text, TextType.IMAGE, image_url))

        if remaining_text:
            new_nodes.append(TextNode(remaining_text, TextType.TEXT))

    return new_nodes


def split_nodes_link(old_nodes):
    new_nodes = []
    for node in old_nodes:
        if node.text_type != TextType.TEXT:
            new_nodes.append(node)
            continue

        links = extract_markdown_links(node.text)
        if not links:
            new_nodes.append(node)
            continue

        remaining_text = node.text
        for link_text, link_url in links:
            parts = remaining_text.split(f"[{link_text}]({link_url})", 1)
            if len(parts) != 2:
                continue

            before_text = parts[0]
            remaining_text = parts[1]

            if before_text:
                new_nodes.append(TextNode(before_text, TextType.TEXT))

            if link_text:
                new_nodes.append(TextNode(link_text, TextType.LINK, link_url))

        if remaining_text:
            new_nodes.append(TextNode(remaining_text, TextType.TEXT))
    return new_nodes


def text_to_textnodes(text):
    pass


def extract_markdown_images(text):
    return re.findall(r"!\[([^\[\]]*)\]\(([^\(\)]*)\)", text)


def extract_markdown_links(text):
    return re.findall(r"(?<!!)\[([^\[\]]*)\]\(([^\(\)]*)\)", text)


if __name__ == "__main__":
    node = TextNode("This is text with a `code block` word", TextType.TEXT)
    new_nodes = split_nodes_delimiter([node], "`", TextType.CODE)
    print(new_nodes)

    text = "This is text with a ![rick roll](https://i.imgur.com/aKaOqIh.gif) and ![obi wan](https://i.imgur.com/fJRm4Vk.jpeg)"
    print(extract_markdown_images(text))

    text = "This is text with a link [to boot dev](https://www.boot.dev) and [to youtube](https://www.youtube.com/@bootdotdev)"
    print(extract_markdown_links(text))

    node = TextNode(
        "This is text with a link [to boot dev](https://www.boot.dev) and [to youtube](https://www.youtube.com/@bootdotdev)",
        TextType.TEXT,
    )
    print(split_nodes_link([node]))

    node = TextNode(
        "This is text with a image ![to boot dev](https://www.image.dev) and [to youtube](https://www.youtube.com/@bootdotdev)",
        TextType.TEXT,
    )
    print(split_nodes_image([node]))

    text = "This is **text** with an _italic_ word and a `code block` and an ![obi wan image](https://i.imgur.com/fJRm4Vk.jpeg) and a [link](https://boot.dev)"
    print(text_to_textnodes(text))
