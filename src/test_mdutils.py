import unittest

import mdutils
import textnode
import htmlnode


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

    def test_markdown_to_blocks_empty_string(self):
        markdown = ""
        expected_output = []
        output = mdutils.markdown_to_blocks(markdown)

        self.assertEqual(expected_output, output)

    def test_markdown_to_blocks_consecutive_newlines(self):
        markdown = (
            "This is **bolded** paragraph\n"
            "\n"
            "\n"
            "\n"
            "This is another paragraph with *italic* text and `code` here\n"
            "This is the same paragraph on a new line\n"
            "\n"
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

    def test_markdown_to_blocks_no_newlines(self):
        markdown = "Just a simple string"
        expected_output = ["Just a simple string"]
        output = mdutils.markdown_to_blocks(markdown)

        self.assertCountEqual(expected_output, output)

    def test_block_to_block_type_headings(self):
        blocks = [
            "# Heading 1",
            "## Heading 2",
            "### Heading 3",
            "#### Heading 4",
            "##### Heading 5",
            "###### Heading 6",
        ]
        for block in blocks:
            self.assertEqual(
                mdutils.BLOCK_TYPE_HEADING, mdutils.block_to_block_type(block)
            )

    def test_block_to_block_type_non_headings(self):
        blocks = [
            "####### 7 Headings",
            "#NoSpaceHeading",
            "No markdown text",
        ]
        for block in blocks:
            self.assertEqual(
                mdutils.BLOCK_TYPE_PARAGRAPH, mdutils.block_to_block_type(block)
            )

    def test_block_to_block_type_code(self):
        blocks = [
            "```code```",
            "``` code ```",
            "```code ```",
            "``` code ```",
            "```\ncode```",
            "```code\n```",
        ]
        for block in blocks:
            self.assertEqual(
                mdutils.BLOCK_TYPE_CODE, mdutils.block_to_block_type(block)
            )

    def test_block_to_block_type_non_code(self):
        blocks = [
            "```code`````",
            "`````code```",
            "code```",
            "```code",
            "`````code`````",
            "````code\n````",
            "````\ncode\n````",
        ]
        for block in blocks:
            self.assertEqual(
                mdutils.BLOCK_TYPE_PARAGRAPH, mdutils.block_to_block_type(block)
            )

    def test_block_to_block_type_blockquote(self):
        blocks = [
            "> quote",
        ]
        for block in blocks:
            self.assertEqual(
                mdutils.BLOCK_TYPE_QUOTE, mdutils.block_to_block_type(block)
            )

    def test_block_to_block_type_non_blockquote(self):
        blocks = [
            ">quote",
            "quote",
            ">\nquote",
            ">> quote",
        ]
        for block in blocks:
            self.assertEqual(
                mdutils.BLOCK_TYPE_PARAGRAPH, mdutils.block_to_block_type(block)
            )

    def test_block_to_block_type_unordered_list(self):
        blocks = [
            "- One",
            "* One",
            ("- One\n- Two\n- Three\n- Four\n"),
            ("* One\n* Two\n* Three\n* Four\n"),
        ]
        for block in blocks:
            self.assertEqual(
                mdutils.BLOCK_TYPE_UNORDERED_LIST, mdutils.block_to_block_type(block)
            )

    def test_block_to_block_type_broken_unordered_list(self):
        blocks = [
            "One",
            "*One",
            ("- One\n- Two\n- Three\n^ Four\n"),
            ("* One\n* Two\n^ Three\n- Four\n"),
        ]
        for block in blocks:
            self.assertEqual(
                mdutils.BLOCK_TYPE_PARAGRAPH, mdutils.block_to_block_type(block)
            )

    def test_block_to_block_type_ordered_list(self):
        blocks = [
            "1. One",
            ("1. One\n2. Two\n3. Three\n4. Four\n"),
        ]
        for block in blocks:
            self.assertEqual(
                mdutils.BLOCK_TYPE_ORDERED_LIST, mdutils.block_to_block_type(block)
            )

    def test_block_to_block_type_broken_ordered_list(self):
        blocks = [
            "One",
            "1.One",
            "1 One",
            ("1. One\n2. Two\n5. Three\n4. Four\n"),
            ("1. One\nb. Two\n3. Three\n4. Four\n"),
        ]
        for block in blocks:
            self.assertEqual(
                mdutils.BLOCK_TYPE_PARAGRAPH, mdutils.block_to_block_type(block)
            )

    def test_blockquote_to_HTMLNode(self):
        text = "> Excuses are **lies**"
        expected_node = htmlnode.ParentNode(
            "blockquote",
            [
                htmlnode.LeafNode(None, "Excuses are "),
                htmlnode.LeafNode("b", "lies"),
            ],
        )
        output = mdutils.blockquote_to_HTMLNode(text)
        self.assertEqual(expected_node, output)
        self.assertEqual(expected_node.to_html(), output.to_html())

    def test_paragraph_to_HTMLNode(self):
        text = "Excuses are **lies**"
        expected_node = htmlnode.ParentNode(
            "p",
            [
                htmlnode.LeafNode(None, "Excuses are "),
                htmlnode.LeafNode("b", "lies"),
            ],
        )
        output = mdutils.paragraph_to_HTMLNode(text)
        self.assertEqual(expected_node, output)
        self.assertEqual(expected_node.to_html(), output.to_html())

    def test_headings_to_HTMLNode(self):
        headings_text = [
            "# Excuses are lies",
            "## Excuses are lies",
            "### Excuses are lies",
            "#### Excuses are lies",
            "##### Excuses are lies",
            "###### Excuses are lies",
        ]
        expected_nodes = [
            htmlnode.ParentNode(
                "h1",
                [
                    htmlnode.LeafNode(None, "Excuses are lies"),
                ],
            ),
            htmlnode.ParentNode(
                "h2",
                [
                    htmlnode.LeafNode(None, "Excuses are lies"),
                ],
            ),
            htmlnode.ParentNode(
                "h3",
                [
                    htmlnode.LeafNode(None, "Excuses are lies"),
                ],
            ),
            htmlnode.ParentNode(
                "h4",
                [
                    htmlnode.LeafNode(None, "Excuses are lies"),
                ],
            ),
            htmlnode.ParentNode(
                "h5",
                [
                    htmlnode.LeafNode(None, "Excuses are lies"),
                ],
            ),
            htmlnode.ParentNode(
                "h6",
                [
                    htmlnode.LeafNode(None, "Excuses are lies"),
                ],
            ),
        ]
        for i in range(0, len(headings_text)):
            output = mdutils.headings_to_HTMLNode(headings_text[i])
            self.assertEqual(expected_nodes[i], output)
            self.assertEqual(expected_nodes[i].to_html(), output.to_html())

    def test_headings_to_HTMLNode_no_headings(self):
        text = "Excuses are lies"
        with self.assertRaises(ValueError):
            mdutils.headings_to_HTMLNode(text)

    def test_unordered_list_to_HTMLNode(self):
        text = "- One\n- Two\n- Three\n- Four\n"
        expected_node = htmlnode.ParentNode(
            "ul",
            [
                htmlnode.LeafNode("li", "One"),
                htmlnode.LeafNode("li", "Two"),
                htmlnode.LeafNode("li", "Three"),
                htmlnode.LeafNode("li", "Four"),
            ],
        )
        output = mdutils.unordered_list_to_HTMLNode(text)
        self.assertEqual(expected_node, output)
        self.assertEqual(expected_node.to_html(), output.to_html())

    def test_ordered_list_to_HTMLNode(self):
        text = "1. One\n2. Two\n3. Three\n4. Four\n"
        expected_node = htmlnode.ParentNode(
            "ol",
            [
                htmlnode.LeafNode("li", "One"),
                htmlnode.LeafNode("li", "Two"),
                htmlnode.LeafNode("li", "Three"),
                htmlnode.LeafNode("li", "Four"),
            ],
        )
        output = mdutils.ordered_list_to_HTMLNode(text)
