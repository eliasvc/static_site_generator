import textnode
import parse


def split_nodes_image(old_nodes):
    """Split text attribute from nodes in old_nodes into one or more TextNodes based on the following rules:
    * ![alt](url) => TextNode(alt, textnode.TEXT_TYPE_TEXT, url)
    * regular text => TextNode(regular text, texnode.TEXT_TYPE_TEXT)
    Nodes not of text type textnode.TEXT_TYPE_TEXT will be kept as is.
    Returns list of all nodes that splinter from old_nodes"""
    new_nodes = []
    for node in old_nodes:
        if node.text_type != textnode.TEXT_TYPE_TEXT:
            new_nodes.append(node)
            continue
        if node.text == "":
            continue
        images = parse.extract_markdown_images(node.text)
        # No markdown image elements were found or had broken elements. Either way, add it as is
        if not images:
            continue
        target_text = node.text
        for image in images:
            # Split text in two sections, one containing everything before the image element and
            # the other containin the rest for later processing.
            sections = target_text.split(f"![{image[0]}]({image[1]})", maxsplit=1)
            if sections[0] != "":
                new_nodes.append(
                    textnode.TextNode(sections[0], textnode.TEXT_TYPE_TEXT)
                )
            if sections[1] != "":
                target_text = sections[1]

            new_nodes.append(
                textnode.TextNode(image[0], textnode.TEXT_TYPE_IMAGE, image[1])
            )

    return new_nodes
