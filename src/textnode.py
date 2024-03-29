from htmlnode import HTMLNode, LeafNode

TEXT_TYPE_TEXT = "text"
TEXT_TYPE_BOLD = "bold"
TEXT_TYPE_ITALIC = "italic"
TEXT_TYPE_CODE = "code"
TEXT_TYPE_LINK = "link"
TEXT_TYPE_IMAGE = "image"

class TextNode:
    def __init__(self, text, text_type, url=None):
        self.text = text
        self.text_type = text_type
        self.url = url

    def __eq__(self, other):
        if (
            self.text == other.text
            and self.text_type == other.text_type
            and self.url == other.url
        ):
            return True
        return False

    def __repr__(self):
        return f"TextNode({self.text}, {self.text_type}, {self.url})"

def text_node_to_html_node(text_node):
    """Convert a TextNode into an HTMLNode"""
    if text_node.text_type == TEXT_TYPE_TEXT:
        return LeafNode(value=text_node.text)
    elif text_node.text_type == TEXT_TYPE_BOLD:
        return LeafNode('b', text_node.text)
    elif text_node.text_type == TEXT_TYPE_ITALIC:
        return LeafNode('i', text_node.text)
    elif text_node.text_type == TEXT_TYPE_CODE:
        return LeafNode('code', text_node.text)
    elif text_node.text_type == TEXT_TYPE_LINK:
        props = {"href": text_node.url}
        return LeafNode('a', text_node.text, props=props)
    elif text_node.text_type == TEXT_TYPE_IMAGE:
        props = {"src": text_node.url, "alt": text_node.text}
        return LeafNode('img', text_node.text, props)