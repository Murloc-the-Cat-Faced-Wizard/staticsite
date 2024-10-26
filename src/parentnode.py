from htmlnode import HTMLNode

class ParentNode(HTMLNode):
    def __init__(self, tag=None, children=None, props=None):
        super().__init__(tag=tag, children=children, props=props)

        
    def to_html(self):
        if not self.tag:
            raise ValueError("Tag not set")
        if len(self.children) < 1:
            raise ValueError("Parent has no children")
        if self.props:
            string = f"<{self.tag}{self.props_to_html()}>"
        else:
            string = f"<{self.tag}>"
        #for child in self.children:
            #string += child.to_html()
        string += "".join(list(map(lambda x: x.to_html(), self.children)))
        string += f"</{self.tag}>"
        return string
