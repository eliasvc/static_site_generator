from textnode import TextNode


def main():
    bold_text = TextNode("boom", "bold", "example.com")
    more_bold_text = TextNode("boom", "bold", "example.com")
    italic_text = TextNode("boom", "italic", "example.com")
    print(bold_text)
    print(bold_text == more_bold_text)
    print(bold_text == italic_text)


if __name__ == "__main__":
    main()
