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

        self.assertCountEqual(expected_output, new_nodes)

    def test_split_nodes_image_no_text_node(self):
        node = textnode.TextNode("", textnode.TEXT_TYPE_TEXT)
        output = mdutils.split_nodes_image([node])
        self.assertEqual(output, [])

    def test_split_nodes_image_no_image_text(self):
        node = textnode.TextNode(
            "not an image element in here", textnode.TEXT_TYPE_TEXT
        )
        output = mdutils.split_nodes_image([node])
        self.assertEqual(output, [node])

    def test_split_nodes_image_non_textnode(self):
        node = textnode.TextNode("", textnode.TEXT_TYPE_BOLD)
        output = mdutils.split_nodes_image([node])
        self.assertEqual(output, [node])

    def test_split_nodes_link(self):
        node = textnode.TextNode(
            "This is text with an [link](https://storage.googleapis.com/qvault-webapp-dynamic-assets/course_assets/zjjcJKZ.png) and another [second link](https://storage.googleapis.com/qvault-webapp-dynamic-assets/course_assets/3elNhQu.png)",
            textnode.TEXT_TYPE_TEXT,
        )
        new_nodes = mdutils.split_nodes_link([node])
        expected_output = [
            textnode.TextNode("This is text with an ", textnode.TEXT_TYPE_TEXT),
            textnode.TextNode(
                "link",
                textnode.TEXT_TYPE_LINK,
                "https://storage.googleapis.com/qvault-webapp-dynamic-assets/course_assets/zjjcJKZ.png",
            ),
            textnode.TextNode(" and another ", textnode.TEXT_TYPE_TEXT),
            textnode.TextNode(
                "second link",
                textnode.TEXT_TYPE_LINK,
                "https://storage.googleapis.com/qvault-webapp-dynamic-assets/course_assets/3elNhQu.png",
            ),
        ]

        self.assertCountEqual(expected_output, new_nodes)

    def test_split_nodes_link_no_text_node(self):
        node = textnode.TextNode("", textnode.TEXT_TYPE_TEXT)
        output = mdutils.split_nodes_link([node])
        self.assertEqual(output, [])

    def test_split_nodes_link_text_only(self):
        node = textnode.TextNode("not a link element in here", textnode.TEXT_TYPE_TEXT)
        output = mdutils.split_nodes_link([node])
        self.assertEqual(output, [node])

    def test_split_nodes_link_non_textnode(self):
        node = textnode.TextNode("", textnode.TEXT_TYPE_BOLD)
        output = mdutils.split_nodes_link([node])
        self.assertEqual(output, [node])

    def test_text_to_textnodes(self):
        text = "This is **text** with an *italic* word and a `code block` and an ![image](https://storage.googleapis.com/qvault-webapp-dynamic-assets/course_assets/zjjcJKZ.png) and a [link](https://boot.dev)"
        expected_output = [
            textnode.TextNode("This is ", textnode.TEXT_TYPE_TEXT),
            textnode.TextNode("text", textnode.TEXT_TYPE_BOLD),
            textnode.TextNode(" with an ", textnode.TEXT_TYPE_TEXT),
            textnode.TextNode("italic", textnode.TEXT_TYPE_ITALIC),
            textnode.TextNode(" word and a ", textnode.TEXT_TYPE_TEXT),
            textnode.TextNode("code block", textnode.TEXT_TYPE_CODE),
            textnode.TextNode(" and an ", textnode.TEXT_TYPE_TEXT),
            textnode.TextNode(
                "image",
                textnode.TEXT_TYPE_IMAGE,
                "https://storage.googleapis.com/qvault-webapp-dynamic-assets/course_assets/zjjcJKZ.png",
            ),
            textnode.TextNode(" and a ", textnode.TEXT_TYPE_TEXT),
            textnode.TextNode("link", textnode.TEXT_TYPE_LINK, "https://boot.dev"),
        ]
        output = mdutils.text_to_textnodes(text)
        print(output)
        self.assertCountEqual(expected_output, output)

    def test_text_to_textnodes_text_only(self):
        expected_output = [
            textnode.TextNode("not a link element in here", textnode.TEXT_TYPE_TEXT)
        ]
        output = mdutils.text_to_textnodes("not a link element in here")
        self.assertEqual(expected_output, output)

    def test_markdown_to_blocks(self):
        markdown = (
            "This is **bolded** paragraph\n"
            "\n"
            "This is another paragraph with *italic* text and `code` here\n"
            "This is the same paragraph on a new line\n"
            "\n"
            "* This is a list\n"
            "* with items\n"
        )
        expected_output = [
            "This is **bolded** paragraph",
            (
                "This is another paragraph with *italic* text and `code` here\n"
                "This is the same paragraph on a new line"
            ),
            ("* This is a list\n" "* with items"),
        ]
        output = mdutils.markdown_to_blocks(markdown)
        self.assertCountEqual(expected_output, output)
