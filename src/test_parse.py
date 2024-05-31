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
