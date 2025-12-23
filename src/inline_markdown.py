import re

from textnode import TextNode, TextType


def split_nodes_delimiter(old_nodes, delimiter, text_type):
    tnode_list = []
    for node in old_nodes:
        if node.text_type.value != "text":
            tnode_list.append(node)
            continue
        txt = node.text
        split_list = txt.split(f"{delimiter}")
        if len(split_list) % 2 == 0:
            raise Exception("invalid markdown syntax")

        temp_nodes = []
        for i in range(len(split_list)):
            if split_list[i] == "":
                continue
            if i % 2 == 0:
                temp_nodes.append(TextNode(split_list[i], TextType.TEXT))
            else:
                temp_nodes.append(TextNode(split_list[i], text_type))

        tnode_list.extend(temp_nodes)
    return tnode_list


def extract_markdown_images(text):
    pattern = r"!\[([^\[\]]*)\]\(([^\(\)]*)\)"
    matches = re.findall(pattern, text)

    return matches

    """ images = re.findall(r"\[([^\[\]]*)\]", text)
    link = re.findall(r"\(([^\(\)]*)\)", text)
    tlist = []
    for i in range(len(images)):
        tup = (images[i], link[i])
        tlist.append(tup)
    return tlist"""


def extract_markdown_links(text):
    pattern = r"(?<!!)\[([^\[\]]*)\]\(([^\(\)]*)\)"
    matches = re.findall(pattern, text)
    return matches

    """atexts = re.findall(r"(?<!!)\[([^\[\]]*)\]", text)
    link = re.findall(r"\(([^\(\)]*)\)", text)
    tlist = []
    for i in range(len(atexts)):
        tup = (atexts[i], link[i])
        tlist.append(tup)
    return tlist"""


def split_nodes_image(old_nodes):
    new_nodes = []
    for node in old_nodes:
        if node.text_type != TextType.TEXT:
            new_nodes.append(node)
            continue
        text = node.text
        extracted_pairs = extract_markdown_images(text)
        if len(extracted_pairs) == 0:
            new_nodes.append(node)
            continue

        for pair in extracted_pairs:
            # parts = text.split(f"![{pair[0]}]({pair[1]})", 1)
            image_alt = pair[0]
            image_link = pair[1]

            split = text.split(f"![{image_alt}]({image_link})", 1)
            if len(split) != 2:
                raise ValueError("invalid markdown, image section")

            if split[0] != "":
                new_nodes.append(TextNode(split[0], TextType.TEXT))
            new_nodes.append(
                TextNode(
                    pair[0],
                    TextType.IMAGE,
                    pair[1],
                )
            )
            text = split[1]
        if text != "":
            new_nodes.append(TextNode(text, TextType.TEXT))

            """if len(split[0]) != 0:
                node_one = TextNode(split[0], TextType.TEXT)
                node_two = TextNode(image_alt, TextType.IMAGE, image_link)
                new_nodes.extend([node_one, node_two])
                text = split[1]
            if split[1] != "" and count == len(extracted_pairs):
                new_nodes.append(TextNode(split[1], TextType.TEXT))
            count += 1"""

    return new_nodes


def split_nodes_link(old_nodes):
    new_nodes = []
    for node in old_nodes:
        if node.text_type != TextType.TEXT:
            new_nodes.append(node)
            continue
        text = node.text
        extracted_pairs = extract_markdown_links(text)

        if len(extracted_pairs) == 0:
            new_nodes.append(node)
            continue

        for pair in extracted_pairs:
            link_anch = pair[0]
            link_link = pair[1]

            sections = text.split(f"[{link_anch}]({link_link})", 1)

            if len(sections) != 2:
                raise ValueError("Invalid markdown")
            if sections[0] != "":
                new_nodes.append(TextNode(sections[0], TextType.TEXT))
            new_nodes.append(TextNode(link_anch, TextType.LINK, link_link))
            text = sections[1]
        if text != "":
            new_nodes.append(TextNode(text, TextType.TEXT))

        """
                node_one = TextNode(before, TextType.TEXT)
                node_two = TextNode(link_anch, TextType.LINK, link_link)
                new_nodes.extend([node_one, node_two])
                text = after
            if after != "" and count == len(extracted_pairs):
                new_nodes.append(TextNode(after, TextType.TEXT))
            count += 1"""

    return new_nodes


def text_to_textnodes(text):
    node_list = [TextNode(text, TextType.TEXT)]
    node_list = split_nodes_delimiter(node_list, "**", TextType.BOLD)
    node_list = split_nodes_delimiter(node_list, "_", TextType.ITALIC)
    node_list = split_nodes_delimiter(node_list, "`", TextType.CODE)
    node_list = split_nodes_image(node_list)
    node_list = split_nodes_link(node_list)

    return node_list
