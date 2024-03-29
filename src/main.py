from enum import Enum

from textnode import TextNode, text_node_to_html_node
from htmlnode import LeafNode

def main():
    bold_text = TextNode("boom", "bold", "example.com")
    more_bold_text = TextNode("boom", "bold", "example.com")
    italic_text = TextNode("boom", "italic", "example.com")
    just_text = TextNode('just text', 'text')
    code_text = TextNode("boom", "code")
    link_text = TextNode("boom", "link", "bold.com")
    image_text = TextNode("boom", "image", "image.com")
    print(bold_text)
    print(bold_text == more_bold_text)
    print(bold_text == italic_text)

    leaf_bold = text_node_to_html_node(bold_text)
    leaf_italic = text_node_to_html_node(italic_text)
    leaf_text = text_node_to_html_node(just_text)
    leaf_code = text_node_to_html_node(code_text)
    leaf_link = text_node_to_html_node(link_text)
    leaf_image = text_node_to_html_node(image_text)
    print(leaf_bold.to_html())
    print(leaf_italic.to_html())
    print(leaf_text.to_html())
    print(leaf_code.to_html())
    print(leaf_link.to_html())
    print(leaf_image.to_html())


if __name__ == "__main__":
    main()
