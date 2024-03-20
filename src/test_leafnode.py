import unittest

from leafnode import LeafNode


class TestLeafNode(unittest.TestCase):
    def test_to_html_no_props(self):
        """Test to_html without any properties"""
        node = LeafNode("p", "This is a paragraph of text.")
        self.assertEqual("<p>This is a paragraph of text.</p>", node.to_html())

    def test_to_html_props(self):
        """Test using properties"""
        node = LeafNode("a", "Click me!", {"href": "https://www.google.com"})
        self.assertEqual('<a href="https://www.google.com">Click me!</a>', node.to_html())

    def test_to_html_no_value(self):
        """A LeafNode without a value should throw a ValueError exception"""
        with self.assertRaises(ValueError):
            node = LeafNode("p")
            node.to_html()

if __name__ == "__main__":
    unittest.main()
