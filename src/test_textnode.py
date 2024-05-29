import unittest

from textnode import TextNode, text_node_to_html_node, split_nodes_delimiter
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

class TestSplitNodesDelimiter(unittest.TestCase):
    def test_text_only(self):
        text_only_nodes = [TextNode('This is a text only node', 'text')]
        split_nodes = split_nodes_delimiter(text_only_nodes, '**', 'bold')
        self.assertEqual(TextNode('This is a text only node', 'text'), split_nodes[0])
        
    def test_text_mixed_with_markup_word(self):
        bold_nodes = [TextNode('Sentence with a spice of **bold** in it', 'text')]
        result = split_nodes_delimiter(bold_nodes, '**', 'bold')
        print(result)
        self.assertEqual(TextNode('Sentence with a spice of ', 'text'), result[0])
        self.assertEqual(TextNode('bold', 'bold'), result[1])
        self.assertEqual(TextNode(' in it', 'text'), result[2])

    def test_text_mixed_with_markup_string(self):
        bold_nodes = [TextNode('Sentence with a spice of a **bold sentence** in it', 'text')]
        result = split_nodes_delimiter(bold_nodes, '**', 'bold')
        print(result)
        self.assertEqual(TextNode('Sentence with a spice of a ', 'text'), result[0])
        self.assertEqual(TextNode('bold sentence', 'bold'), result[1])
        self.assertEqual(TextNode(' in it', 'text'), result[2])

    def test_text_mixed_with_multiple_markup_strings(self):
        bold_nodes = [TextNode('Sentence with a **heavy spice** of a **bold sentence** in it', 'text')]
        result = split_nodes_delimiter(bold_nodes, '**', 'bold')
        print(result)
        self.assertEqual(TextNode('Sentence with a ', 'text'), result[0])
        self.assertEqual(TextNode('heavy spice', 'bold'), result[1])
        self.assertEqual(TextNode(' of a ', 'text'), result[2])
        self.assertEqual(TextNode('bold sentence', 'bold'), result[3])
        self.assertEqual(TextNode(' in it', 'text'), result[4])

    def test_markup_only_sentence(self):
        bold_nodes = [TextNode('**Bold sentence**', 'text')]
        result = split_nodes_delimiter(bold_nodes, '**', 'bold')
        print(result)
        self.assertEqual(TextNode('Bold sentence', 'bold'), result[0])
        
    def test_markup_ending_sentence(self):
        bold_nodes = [TextNode('String ending in **Bold**', 'text')]
        result = split_nodes_delimiter(bold_nodes, '**', 'bold')
        print(result)
        self.assertEqual(TextNode('String ending in ', 'text'), result[0])
        self.assertEqual(TextNode('Bold', 'bold'), result[1])

    def test_markup_word(self):
        bold_nodes = [TextNode('**Bold**', 'text')]
        result = split_nodes_delimiter(bold_nodes, '**', 'bold')
        self.assertEqual(TextNode('Bold', 'bold'), result[0])
 
    def test_incomplete_markup_sentence_beginning(self):
        text_only_nodes = [TextNode('**This is a text only node', 'text')]
        with self.assertRaises(ValueError, msg='Invalid markdown, formatted section not closed'):
            split_nodes = split_nodes_delimiter(text_only_nodes, '**', 'bold')

    def test_incomplete_markup_sentence_end(self):
        text_only_nodes = [TextNode('This is a text only node**', 'text')]
        with self.assertRaises(ValueError, msg='Invalid markdown, formatted section not closed'):
            split_nodes = split_nodes_delimiter(text_only_nodes, '**', 'bold')

    def test_incomplete_markup_word(self):
        bold_nodes = [TextNode('**Bold', 'text')]
        with self.assertRaises(ValueError, msg='Invalid markdown, formatted section not closed'):
            result = split_nodes_delimiter(bold_nodes, '**', 'bold')

    def test_incomplete_markup_word_end(self):
        bold_nodes = [TextNode('Bold**', 'text')]
        with self.assertRaises(ValueError, msg='Invalid markdown, formatted section not closed'):
            result = split_nodes_delimiter(bold_nodes, '**', 'bold')

    def test_non_text_type_node(self):
        bold_nodes = [TextNode('**Bold**', 'bold')]
        result = split_nodes_delimiter(bold_nodes, '**', 'bold')
        self.assertEqual(TextNode('**Bold**', 'bold'), result[0])

if __name__ == "__main__":
    unittest.main()
