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
            for i in range(len(sections)):
                if sections[i] == "":
                    continue
                if i % 2 == 0:
                    new_nodes.append(
                        textnode.TextNode(sections[i], textnode.TEXT_TYPE_TEXT)
                    )
                else:
                    new_nodes.append(
                        textnode.TextNode(image[0], textnode.TEXT_TYPE_IMAGE, image[1])
                    )

    return new_nodes
