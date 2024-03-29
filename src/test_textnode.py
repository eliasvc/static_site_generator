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


class TestTextNodeToHTMLNode(unittest.TestCase):
    def test_bold_text_node(self):
        bold_text = TextNode("boom", "bold")
        leaf_bold = text_node_to_html_node(bold_text)

        leaf_bold_test = LeafNode("b", "boom")
        self.assertEqual(leaf_bold, leaf_bold_test)

    def test_italic_text_node(self):
        italic_text = TextNode("boom", "italic")
        leaf_italic = text_node_to_html_node(italic_text)

        leaf_italic_test = LeafNode("i", "boom")
        self.assertEqual(leaf_italic, leaf_italic_test)

    def test_raw_text_node(self):
        just_text = TextNode('just text', 'text')
        leaf_text = text_node_to_html_node(just_text)
        
        leaf_text_node_test = LeafNode(value='just text')
        self.assertEqual(leaf_text, leaf_text_node_test)

    def test_code_text_node(self):
        code_text = TextNode("boom", "code")
        leaf_code = text_node_to_html_node(code_text)

        leaf_code_test = LeafNode('code', 'boom') 
        self.assertEqual(leaf_code, leaf_code_test)
    
    def test_link_text_node(self):
        link_text = TextNode("boom", "link", "link.com")
        leaf_link = text_node_to_html_node(link_text)

        leaf_link_test = LeafNode('a', 'boom', {'href': 'link.com'})
        self.assertEqual(leaf_link, leaf_link_test)
    
    def test_image_text_node(self):
        image_text = TextNode("boom", "image", "image.com")
        leaf_image = text_node_to_html_node(image_text)

        leaf_image_test = LeafNode('img', 'boom', props={'src':'image.com', 'alt':'boom'})
        self.assertEqual(leaf_image, leaf_image_test)

if __name__ == "__main__":
    unittest.main()
