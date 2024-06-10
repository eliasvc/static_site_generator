import textnode
import parse


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
