class HTMLNode:
    def __init__(self, tag=None, value=None, children=None, props=None):
        self.tag = tag
        self.value = value
        self.children = children
        self.props = props

    def to_html(self):
        raise NotImplementedError()

    def props_to_html(self):
        html = ""
        if self.props:
            for prop, value in self.props.items():
                html += f' {prop}="{value}"'
        return html

    def __repr__(self):
        return f"tag: {self.tag}\nvalue: {self.value}\nchildren: {self.children}\nproperties: {self.props}"

    def __eq__(self, other):
        return (
            isinstance(other, HTMLNode)
            and self.tag == other.tag
            and self.value == other.value
            and self.children == other.children
            and self.props == other.props
        )


class LeafNode(HTMLNode):
    """
    LeafNode represents HTML tags without any children.
    For example, a <p> tag with just some text in it.
    """

    def __init__(self, tag=None, value=None, props=None):
        if not value:
            raise ValueError("value required for Leaf nodes")
        super().__init__(tag, value, None, props)

    def __eq__(self, other):
        return (
            self.tag == other.tag
            and self.value == other.value
            and self.children == other.children
            and self.props == other.props
        )

    def to_html(self):
        if not self.value:
            raise ValueError("no value in element")
        if not self.tag:
            return self.value
        if self.props:
            return f"<{self.tag}{self.props_to_html()}>{self.value}</{self.tag}>"
        return f"<{self.tag}>{self.value}</{self.tag}>"


class ParentNode(HTMLNode):
    """Every node that has children"""

    def __init__(self, tag, children, props=None):
        super().__init__(tag, None, children, props)

    def to_html(self):
        """Recursively print an html representation of child nodes"""
        if self.children is None:
            raise ValueError(f"No children on parent node: {self.tag}")
        child_html = ""
        for child in self.children:
            child_html += child.to_html()
        return f"<{self.tag}{self.props_to_html()}>{child_html}</{self.tag}>"
