from htmlnode import HTMLNode

class LeafNode(HTMLNode):
    """
    LeafNode represents HTML tags without any children.
    For example, a <p> tag with just some text in it.
    """
    
    def __init__(self, tag=None, value=None, props=None):
        if not value:
            raise ValueError("value required for Leaf nodes")
        super().__init__(tag, value, None, props)

    def to_html(self):
        if not self.value:
            raise ValueError("no value in element")
        if not self.tag:
            return self.value
        if self.props:
            return f"<{self.tag}{self.props_to_html()}>{self.value}</{self.tag}>"
        return f"<{self.tag}>{self.value}</{self.tag}>"
