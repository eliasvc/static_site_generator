from htmlnode import HTMLNode, LeafNode

TEXT_TYPE_TEXT = "text"
TEXT_TYPE_BOLD = "bold"
TEXT_TYPE_ITALIC = "italic"
TEXT_TYPE_CODE = "code"
TEXT_TYPE_LINK = "link"
TEXT_TYPE_IMAGE = "image"


class TextNode:
    def __init__(self, text, text_type, url=None):
        self.text = text
        self.text_type = text_type
        self.url = url

    def __eq__(self, other):
        if (
            self.text == other.text
            and self.text_type == other.text_type
            and self.url == other.url
        ):
            return True
        return False

    def __repr__(self):
        return f"TextNode({self.text}, {self.text_type}, {self.url})"


def text_node_to_html_node(text_node):
    """Convert a TextNode into an HTMLNode"""
    if text_node.text_type == TEXT_TYPE_TEXT:
        return LeafNode(value=text_node.text)
    elif text_node.text_type == TEXT_TYPE_BOLD:
        return LeafNode("b", text_node.text)
    elif text_node.text_type == TEXT_TYPE_ITALIC:
        return LeafNode("i", text_node.text)
    elif text_node.text_type == TEXT_TYPE_CODE:
        return LeafNode("code", text_node.text)
    elif text_node.text_type == TEXT_TYPE_LINK:
        props = {"href": text_node.url}
        return LeafNode("a", text_node.text, props=props)
    elif text_node.text_type == TEXT_TYPE_IMAGE:
        props = {"src": text_node.url, "alt": text_node.text}
        return LeafNode("img", text_node.text, props)


def split_nodes_delimiter(old_nodes, delimiter, text_type):
    """Takes a list of TextNodes from old_nodes and parses their text looking for substrings marked up with delimiter.
    If it finds them, it will the node into multiple TextNodes, each one having the corresponding text type.
    The result is a list of all resulting nodes.
    """
    regular_text_nodes = []
    delimiter_text_nodes = []
    delimiter_started = False
    temp_delimiter_buffer = []
    temp_text_buffer = []
    
    print('Old Nodes:')
    print(old_nodes)
    print()
    for node in old_nodes:
        for word in node.text.split():
            if word.startswith(delimiter) and word.endswith(delimiter):
                delimiter_text_nodes.append(TextNode(word, text_type))
                # Any regular text that came right before, if any, is ready to be converted to TextNode
                # e.g: In "This is regular text but *this is bold*" the bold part signals the end of a
                # text-only TextNode
                if temp_text_buffer:
                    regular_text_nodes.append(TextNode(' '.join(temp_text_buffer), TEXT_TYPE_TEXT))
                    temp_text_buffer = []
                if delimiter_started:
                    # Found another starting delimiter before the previous one close
                    # Dumping the previous delimited string into text
                    regular_text_nodes.append(TextNode(' '.join(temp_delimiter_buffer), TEXT_TYPE_TEXT))
                    temp_delimiter_buffer = []
            elif word.startswith(delimiter):
                if not delimiter_started:
                    delimiter_started = True
                    temp_delimiter_buffer.append(word)
                else:
                    # This means a delimiter was found before the previous one closed
                    regular_text_nodes.append(TextNode(' '.join(temp_delimiter_buffer), TEXT_TYPE_TEXT))
                    # Start the buffer over with this new word
                    temp_delimiter_buffer = [word]
            # Closing delimiter is found
            # e.g: "*this is bold*" the second asterisk is found after the first one activated delimiter_started
            elif word.endswith(delimiter) and delimiter_started:
                temp_delimiter_buffer.append(word)
                delimiter_text_nodes.append(TextNode(' '.join(temp_delimiter_buffer), text_type))
                temp_delimiter_buffer = []
                delimiter_started = False
                # Any regular text found before this can be converted to a TextNode
                if temp_text_buffer:
                    regular_text_nodes.append(TextNode(' '.join(temp_text_buffer), TEXT_TYPE_TEXT))
                    temp_text_buffer = []
            elif not word.endswith(delimiter) and delimiter_started:
                # Just regular text but preceded by another word with an opening delimiter, which may mean it's marked up too
                temp_delimiter_buffer.append(word)
            # Regular text. No delimiter 
            elif not delimiter_started:
                temp_text_buffer.append(word)

            print(temp_text_buffer)
            print(temp_delimiter_buffer)
            print()

        # Anything left in temp_delimiter_buffer is as string with an open delimiter that was not closed
        # e.g: "Sh** is getting crazy"
        if temp_delimiter_buffer:
            regular_text_nodes.append(TextNode(' '.join(temp_delimiter_buffer), TEXT_TYPE_TEXT))
        # Anything left in temp_text_buffer will also need to be turned into a text TextNode
        if temp_text_buffer:
            regular_text_nodes.append(TextNode(' '.join(temp_text_buffer), TEXT_TYPE_TEXT))
    print(regular_text_nodes)
    regular_text_nodes.extend(delimiter_text_nodes)
    return regular_text_nodes
