import unittest

from htmlnode import HTMLNode

class TestHTMLNode(unittest.TestCase):
    def test_props_to_html(self):
        node = HTMLNode("<a>", "Google.com", None, {"href": "https://www.google.com", "target": "_blank"})
        self.assertEqual(' href="https://www.google.com" target="_blank"', node.props_to_html())

    def test_repr(self):
        node = HTMLNode("<a>", "Google.com", None, {"href": "https://www.google.com", "target": "_blank"})
        self.assertEqual("tag: <a>\nvalue: Google.com\nchildren: None\nproperties: {'href': 'https://www.google.com', 'target': '_blank'}", repr(node))

if __name__ == "__main__":
    unittest.main()
