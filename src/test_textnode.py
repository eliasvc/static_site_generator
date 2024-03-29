import unittest

from textnode import TextNode, text_node_to_html_node
from htmlnode import LeafNode


class TestTextNode(unittest.TestCase):
    def test_eq(self):
        node = TextNode("This is a text node", "bold")
        node2 = TextNode("This is a text node", "bold")
        self.assertEqual(node, node2)

    def test_eq_url(self):
        node = TextNode("This is a text node", "bold", "example.com")
        node2 = TextNode("This is a text node", "bold", "example.com")
        self.assertEqual(node, node2)

    def test_eq_false_type(self):
        node = TextNode("This is a text node", "bold")
        node2 = TextNode("This is a text node", "italic")
        self.assertNotEqual(node, node2)

    def test_eq_false_text(self):
        node = TextNode("This is a text node", "italic")
        node2 = TextNode("This might be a text node", "bold")
        self.assertNotEqual(node, node2)

    def test_eq_false_url(self):
        node = TextNode("This is a text node", "bold", "example.com")
        node2 = TextNode("This is a text node", "bold")
        self.assertNotEqual(node, node2)

    def test_text_node_to_html_node(self):
        bold_text = TextNode("boom", "bold", "example.com")
        italic_text = TextNode("boom", "italic", "example.com") 
        just_text = TextNode('just text', 'text')
        code_text = TextNode("boom", "code")
        link_text = TextNode("boom", "link", "bold.com")
        image_text = TextNode("boom", "image", "image.com")

        leaf_bold = text_node_to_html_node(bold_text)
        leaf_italic = text_node_to_html_node(italic_text)
        leaf_text = text_node_to_html_node(just_text)
        leaf_code = text_node_to_html_node(code_text)
        leaf_link = text_node_to_html_node(link_text)
        leaf_image = text_node_to_html_node(image_text)

class TestTextNodeToHTMLNode(unittest.TestCase):
    def test_bold_text_node(self):
        bold_text = TextNode("boom", "bold")
        leaf_bold = text_node_to_html_node(bold_text)

        leaf_bold_test = LeafNode("b", "boom")
        self.assertEqual(leaf_bold, leaf_bold_test)

if __name__ == "__main__":
    unittest.main()
