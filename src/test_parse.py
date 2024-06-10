import unittest

import parse


class TestParse(unittest.TestCase):
    def test_extract_markdown_image(self):
        text = "This is text with an ![image](https://test.com/boom/boom.png) and ![another](https://www.test.com/kaboom/kabOOM233.jpeg)"
        expected_output = [
            ("image", "https://test.com/boom/boom.png"),
            ("another", "https://www.test.com/kaboom/kabOOM233.jpeg"),
        ]
        output = parse.extract_markdown_images(text)
        self.assertEqual(output, expected_output)

    def test_extract_markdown_image_empty_image(self):
        text = "This is text with an ![]()"
        expected_output = [
            ("", ""),
        ]
        output = parse.extract_markdown_images(text)
        self.assertEqual(output, expected_output)

    def test_extract_markdown_links(self):
        text = "This is text with a [link](https://test.com/boom/) and [another](https://www.test.com/another)"
        expected_output = [
            ("link", "https://test.com/boom/"),
            ("another", "https://www.test.com/another"),
        ]
        output = parse.extract_markdown_links(text)
        self.assertEqual(output, expected_output)

    def test_extract_markdown_links_empty_link(self):
        text = "This is text with an []()"
        expected_output = [
            ("", ""),
        ]
        output = parse.extract_markdown_links(text)
        self.assertEqual(output, expected_output)
