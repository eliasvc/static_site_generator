import unittest

import mdutils
import textnode


class TestMDUtils(unittest.TestCase):
    def test_split_nodes_image(self):
        node = textnode.TextNode(
            "This is text with an ![image](https://storage.googleapis.com/qvault-webapp-dynamic-assets/course_assets/zjjcJKZ.png) and another ![second image](https://storage.googleapis.com/qvault-webapp-dynamic-assets/course_assets/3elNhQu.png)",
            textnode.TEXT_TYPE_TEXT,
        )
        new_nodes = mdutils.split_nodes_image([node])
        expected_output = [
            textnode.TextNode("This is text with an ", textnode.TEXT_TYPE_TEXT),
            textnode.TextNode(
                "image",
                textnode.TEXT_TYPE_IMAGE,
                "https://storage.googleapis.com/qvault-webapp-dynamic-assets/course_assets/zjjcJKZ.png",
            ),
            textnode.TextNode(" and another ", textnode.TEXT_TYPE_TEXT),
            textnode.TextNode(
                "second image",
                textnode.TEXT_TYPE_IMAGE,
                "https://storage.googleapis.com/qvault-webapp-dynamic-assets/course_assets/3elNhQu.png",
            ),
        ]

        self.assertEqual(expected_output, new_nodes)

    def test_split_nodes_image_no_text_node(self):
        node = textnode.TextNode("", textnode.TEXT_TYPE_TEXT)
        output = mdutils.split_nodes_image([node])
        self.assertEqual(output, [])

    def test_split_nodes_image_no_image_text(self):
        node = textnode.TextNode(
            "not an image element in here", textnode.TEXT_TYPE_TEXT
        )
        output = mdutils.split_nodes_image([node])
        self.assertEqual(output, [])
    
    def test_split_nodes_image_non_textnode(self):
        node = textnode.TextNode("", textnode.TEXT_TYPE_BOLD)
        output = mdutils.split_nodes_image([node])
        self.assertEqual(output, [node])

