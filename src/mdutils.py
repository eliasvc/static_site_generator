import textnode
import parse


def split_nodes_image(old_nodes):
    new_nodes = []
    for node in old_nodes:
        if node.text == "":
            continue
        images = parse.extract_markdown_images(node.text)
        if not images:
            continue
        target_text = node.text
        for image in images:
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
