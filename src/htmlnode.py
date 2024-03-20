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
