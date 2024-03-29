import unittest

from htmlnode import HTMLNode, ParentNode, LeafNode


class TestHTMLNode(unittest.TestCase):
    def test_props_to_html(self):
        node = HTMLNode(
            "<a>",
            "Google.com",
            None,
            {"href": "https://www.google.com", "target": "_blank"},
        )
        self.assertEqual(
            ' href="https://www.google.com" target="_blank"', node.props_to_html()
        )

    def test_repr(self):
        node = HTMLNode(
            "<a>",
            "Google.com",
            None,
            {"href": "https://www.google.com", "target": "_blank"},
        )
        self.assertEqual(
            "tag: <a>\nvalue: Google.com\nchildren: None\nproperties: {'href': 'https://www.google.com', 'target': '_blank'}",
            repr(node),
        )


class TestParentNode(unittest.TestCase):
    def test_to_html(self):
        node = ParentNode(
            "p",
            [
                LeafNode("b", "Bold text"),
                LeafNode(None, "Normal text"),
                LeafNode("i", "italic text"),
                LeafNode(None, "Normal text"),
                ParentNode(
                    "p",
                    [
                        LeafNode("b", "Inside Bold text"),
                        LeafNode("i", "Inside italic text"),
                    ],
                ),
            ],
        )

        self.assertEqual(
            node.to_html(),
            "<p>><b>Bold text</b>Normal text<i>italic text</i>Normal text<p>><b>Inside Bold text</b><i>Inside italic text</i></p></p>",
        )

    def test_no_children(self):
        node = ParentNode("p", None)
        with self.assertRaises(ValueError):
            node.to_html()

class TestLeafNode(unittest.TestCase):
    def test_to_html_no_props(self):
        """Test to_html without any properties"""
        node = LeafNode("p", "This is a paragraph of text.")
        self.assertEqual("<p>This is a paragraph of text.</p>", node.to_html())
    
    def test_eq(self):
        node = LeafNode("p", "This is a paragraph of text.")
        other_node = LeafNode("p", "This is a paragraph of text.")
        self.assertEqual(node, other_node)
        
    def test_not_eq(self):
        node = LeafNode("p", "This is a paragraph of text.")
        other_node = LeafNode("p", "This is a different paragraph of text.")
        self.assertNotEqual(node, other_node)

    def test_to_html_props(self):
        """Test using properties"""
        node = LeafNode("a", "Click me!", {"href": "https://www.google.com"})
        self.assertEqual(
            '<a href="https://www.google.com">Click me!</a>', node.to_html()
        )

    def test_to_html_no_value(self):
        """A LeafNode without a value should throw a ValueError exception"""
        with self.assertRaises(ValueError):
            node = LeafNode("p")
            node.to_html()

if __name__ == "__main__":
    unittest.main()
