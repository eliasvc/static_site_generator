import re

import textnode
import parse
import htmlnode

BLOCK_TYPE_PARAGRAPH = "paragraph"
BLOCK_TYPE_HEADING = "heading"
BLOCK_TYPE_CODE = "code"
BLOCK_TYPE_QUOTE = "quote"
BLOCK_TYPE_UNORDERED_LIST = "unordered_list"
BLOCK_TYPE_ORDERED_LIST = "ordered_list"


def split_nodes_image(old_nodes):
    """Split text attribute from nodes in old_nodes into one or more TextNodes based on the following rules:
    * ![alt](url) => TextNode(alt, textnode.TEXT_TYPE_TEXT, url)
    * regular text => TextNode(regular text, texnode.TEXT_TYPE_TEXT)
    Nodes not of text type textnode.TEXT_TYPE_TEXT will be kept as is.
    Returns list of all nodes that splinter from old_nodes"""
    new_nodes = []
    target_text = ""
    for node in old_nodes:
        if node.text_type != textnode.TEXT_TYPE_TEXT:
            new_nodes.append(node)
            continue
        if node.text == "":
            continue
        images = parse.extract_markdown_images(node.text)
        # No markdown image elements were found or had broken elements. Either way, add it as is
        if not images:
            new_nodes.append(node)
            continue
        target_text = node.text
        for image in images:
            # Split text in two sections, one containing everything before the image element and
            # the other containin the rest for later processing.
            sections = target_text.split(f"![{image[0]}]({image[1]})", maxsplit=1)
            target_text = ""
            if sections[0]:
                new_nodes.append(
                    textnode.TextNode(sections[0], textnode.TEXT_TYPE_TEXT)
                )
            if sections[1]:
                target_text = sections[1]

            new_nodes.append(
                textnode.TextNode(image[0], textnode.TEXT_TYPE_IMAGE, image[1])
            )
    # Any left-over text has to be a text_type_text TextNode
    if target_text:
        new_nodes.append(textnode.TextNode(target_text, textnode.TEXT_TYPE_TEXT))
    return new_nodes


def split_nodes_link(old_nodes):
    """Split text attribute from nodes in old_nodes into one or more TextNodes based on the following rules:
    * [link](url) => TextNode(link, textnode.TEXT_TYPE_TEXT, url)
    * regular text => TextNode(regular text, texnode.TEXT_TYPE_TEXT)
    Nodes not of text type textnode.TEXT_TYPE_TEXT will be kept as is.
    Returns list of all nodes that splinter from old_nodes"""
    new_nodes = []
    target_text = ""
    for node in old_nodes:
        if node.text_type != textnode.TEXT_TYPE_TEXT:
            new_nodes.append(node)
            continue
        if node.text == "":
            continue
        links = parse.extract_markdown_links(node.text)
        # No markdown link elements were found or had broken elements. Either way, add it as is
        if not links:
            new_nodes.append(node)
            continue
        target_text = node.text
        for link in links:
            # Split text in two sections, one containing everything before the link element and
            # the other containin the rest for later processing.
            sections = target_text.split(f"[{link[0]}]({link[1]})", maxsplit=1)
            target_text = ""
            if sections[0]:
                new_nodes.append(
                    textnode.TextNode(sections[0], textnode.TEXT_TYPE_TEXT)
                )
            if sections[1]:
                target_text = sections[1]

            new_nodes.append(
                textnode.TextNode(link[0], textnode.TEXT_TYPE_LINK, link[1])
            )
    # Any left-over text has to be a text_type_text TextNode
    if target_text:
        new_nodes.append(textnode.TextNode(target_text, textnode.TEXT_TYPE_TEXT))
    return new_nodes


def text_to_textnodes(text):
    """Parses text and converts any markdown elments found into TextNodes with the corresponding type.
    Returns a list of all TextNodes created"""
    resulting_nodes = []
    if not text:
        return resulting_nodes
    resulting_nodes.append(textnode.TextNode(text, textnode.TEXT_TYPE_TEXT))
    markdown_delimiters = {
        "`": textnode.TEXT_TYPE_CODE,
        "**": textnode.TEXT_TYPE_BOLD,
        "*": textnode.TEXT_TYPE_ITALIC,
    }
    for delimiter in markdown_delimiters.keys():
        resulting_nodes = textnode.split_nodes_delimiter(
            resulting_nodes, delimiter, markdown_delimiters[delimiter]
        )
    resulting_nodes = split_nodes_link(resulting_nodes)
    resulting_nodes = split_nodes_image(resulting_nodes)
    return resulting_nodes


def markdown_to_blocks(markdown: str) -> list:
    """Takes markdown strings and returns a list of block strings, where block strings are defined as strings separated by one
    or more blank lines"""
    return [x.strip() for x in markdown.split("\n\n") if x]


def block_to_block_type(block):
    """Detect the type of markdown block type. The types than can be identified are:
    * Heading: Block starts with 1 to 6 '#' followed by a space
    * Code: Block needs to start and end with '```'
    * Quote: Block starts with '>' followed by a space
    * Unordered List: All items in the list need to start with '-' or '*' followed by space
    * Ordered List: All items numbers in the list need to be followed by a '.' and a space. They also need to start with 1 and following numbers need to be in ascending order
    If non of the above match, the block is deemed as a regular paragraph"""

    if re.match(r"^#{1,6} .*", block):
        return BLOCK_TYPE_HEADING
    elif re.match(r"^```\s?[^`]*\s?```$", block):
        return BLOCK_TYPE_CODE
    elif re.match(r"^> .*", block):
        return BLOCK_TYPE_QUOTE
    elif re.match(r"^(:?-|\* )", block):
        items = block.splitlines()
        for item in items:
            if not re.match(r"^(:?-|\* )", item):
                return BLOCK_TYPE_PARAGRAPH
        return BLOCK_TYPE_UNORDERED_LIST
    elif re.match(r"^1\. ", block):
        items = block.splitlines()
        for i in range(0, len(items)):
            m = re.match(r"^(\d+). ", items[i])
            if not m:
                return BLOCK_TYPE_PARAGRAPH
            item_number = int(m.group(1))
            # Item numbers need to be in ascending order.
            if i + 1 != item_number:
                return BLOCK_TYPE_PARAGRAPH
        return BLOCK_TYPE_ORDERED_LIST
    return BLOCK_TYPE_PARAGRAPH


def blockquote_to_HTMLNode(text: str) -> htmlnode.HTMLNode:
    new_text = text.replace("> ", "")
    text_nodes = text_to_textnodes(new_text)
    leaf_nodes = [textnode.text_node_to_html_node(node) for node in text_nodes]
    node = htmlnode.ParentNode("blockquote", leaf_nodes)
    return node


def paragraph_to_HTMLNode(text: str) -> htmlnode.ParentNode:
    text_nodes = text_to_textnodes(text)
    leaf_nodes = [textnode.text_node_to_html_node(node) for node in text_nodes]
    node = htmlnode.ParentNode("p", leaf_nodes)
    return node


def headings_to_HTMLNode(text: str) -> htmlnode.ParentNode:
    m = re.match(r"(^#{1,6}) ", text)
    if not m:
        raise ValueError("Expected heading markdown not found")
    headings = m.group(1)
    no_headings_text = text.replace(f"{headings} ", "")
    text_nodes = text_to_textnodes(no_headings_text)
    leaf_nodes = [textnode.text_node_to_html_node(node) for node in text_nodes]
    node = htmlnode.ParentNode(f"h{len(headings)}", leaf_nodes)
    return node


def unordered_list_to_HTMLNode(text: str) -> htmlnode.ParentNode:
    new_text = re.sub(r"(-|\*) ", "", text)
    leaf_nodes = [htmlnode.LeafNode("li", item) for item in new_text.splitlines()]
    node = htmlnode.ParentNode("ul", leaf_nodes)
    return node


def ordered_list_to_HTMLNode(text: str) -> htmlnode.ParentNode:
    new_text = re.sub(r"\d+\. ", "", text)
    leaf_nodes = [htmlnode.LeafNode("li", item) for item in new_text.splitlines()]
    node = htmlnode.ParentNode("ol", leaf_nodes)
    return node


def code_to_HTMLNode(text: str) -> htmlnode.ParentNode:
    new_text = re.sub(r"```", "", text)
    leaf_node = htmlnode.LeafNode("pre", new_text)
    node = htmlnode.ParentNode("code", [leaf_node])
    return node


def markdown_to_HTMLNode(markdown: str) -> htmlnode.ParentNode:
    child_nodes = []
    blocks = markdown_to_blocks(markdown)
    for block in blocks:
        type = block_to_block_type(block)
        if type == BLOCK_TYPE_CODE:
            child_nodes.append(code_to_HTMLNode(block))
        elif type == BLOCK_TYPE_PARAGRAPH:
            child_nodes.append(paragraph_to_HTMLNode(block))
        elif type == BLOCK_TYPE_CODE:
            child_nodes.append(code_to_HTMLNode(block))
        elif type == BLOCK_TYPE_HEADING:
            child_nodes.append(headings_to_HTMLNode(block))
        elif type == BLOCK_TYPE_ORDERED_LIST:
            child_nodes.append(ordered_list_to_HTMLNode(block))
        elif type == BLOCK_TYPE_QUOTE:
            child_nodes.append(blockquote_to_HTMLNode(block))
        elif type == BLOCK_TYPE_UNORDERED_LIST:
            child_nodes.append(unordered_list_to_HTMLNode(block))

    return htmlnode.ParentNode("div", child_nodes)


def extract_title(markdown):
    m = re.match(r"^# (.*)", markdown)
    if not m:
        raise ValueError("Markdown document without h1 header")
    return m.group(1)
