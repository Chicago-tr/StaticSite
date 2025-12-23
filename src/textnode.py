from enum import Enum

from htmlnode import LeafNode


class TextType(Enum):
    TEXT = "text"
    BOLD = "bold"
    ITALIC = "italic"
    LINK = "link"
    CODE = "code"
    IMAGE = "image"


class TextNode:
    def __init__(self, text, text_type, url=None):
        self.text = text
        self.text_type = text_type
        self.url = url

    def __eq__(self, other):
        return (
            self.text == other.text
            and self.text_type == other.text_type
            and self.url == other.url
        )

    def __repr__(self):
        return f"TextNode({self.text}, {self.text_type.value}, {self.url})"


def text_node_to_html_node(text_node):
    txt = text_node.text
    type = text_node.text_type.value
    url = text_node.url
    if type == "text":
        return LeafNode(None, txt)
        # return str(txt)
    elif type == "bold":
        return LeafNode("b", txt)
        # return f"<b>{txt}</b>"
    elif type == "italic":
        return LeafNode("i", txt)
        # return f"<i>{txt}</i>"
    elif type == "code":
        return LeafNode("code", txt)
    # return f"<code>{txt}</code>"
    elif type == "link":
        return LeafNode("a", txt, {"href": url})
    # return f"<a href= "
    elif type == "image":
        return LeafNode("img", "", {"src": url, "alt": txt})
    raise ValueError(f"invalid text type: {text_node.text_type}")
