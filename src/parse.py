import re


def extract_markdown_images(text):
    """Parses all image markdown elements in the form [alt text](image URL/path).
    Returns a list of tuples, each composed of (alt text, image URL/path) of
    every image element found"""
    matches = re.findall(r"!\[(.*?)\]\((.*?)\)", text)

    return matches


def extract_markdown_links(text):
    """Parses all link markdown elements in the form [link](URL/path).
    Returns a list of tuples, each composed of (link, URL/path) of
    every link element found"""
    matches = re.findall(r"\[(.*?)\]\((.*?)\)", text)

    return matches
