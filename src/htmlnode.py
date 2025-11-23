class HTMLNode:
    def __init__(self,tag = None, value = None, children = None, props = None):
        self.tag = tag
        self.value = value
        self.children = children
        self.props = props

    def to_html(self):
        raise NotImplementedError("to_html method not implemented")
    
    def props_to_html(self):
        if self.props == None or len(self.props)==0:
            return ""
        output = ''
        for key in self.props:
            output += f' {key}="{self.props[key]}"'
        return output
    
    def __repr__(self):
        return f"HTMLNode({self.tag}, {self.value}, children: {self.children}, {self.props})"

class LeafNode(HTMLNode):
    def __init__(self,tag, value, props = None):
        super().__init__(tag,value,None,props)

    def to_html(self):
        if self.value == None:
            raise ValueError("All leaf nodes must have a value")
        if self.tag == None:
            return self.value
        return f"<{self.tag}{self.props_to_html()}>{self.value}</{self.tag}>"
    
class ParentNode(HTMLNode):
    def __init__(self,tag,children, props = None):
        super().__init__(tag,None,children,props)

    def to_html(self):
        if self.tag == None:
            raise ValueError("No tag given")
        if self.children == None:
            raise ValueError("No children given")
        output = ""
        for child in self.children:
            output += child.to_html()
        return f"<{self.tag}>{output}</{self.tag}>"
