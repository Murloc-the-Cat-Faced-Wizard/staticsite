class HTMLNode():
    def __init__(self, tag=None, value=None, children=None, props=None):
        self.tag = tag
        self.value = value
        self.children = children
        self.props = props

    def to_html(self):
        raise NotImplementedError("Child must define to_html function")
    
    def props_to_html(self):
        #tuple_list = self.props.items()
        #new_list = []
        #for key, value in tuple_list:
            #new_list.append(f' {key}="{value}"')
        new_list = list(map(lambda x: f' {x[0]}="{x[1]}"', self.props.items()))
        return "".join(new_list)
    
    def __repr__(self):
        return f"HTMLNode({self.tag}, {self.value}, {self.children}, {self.props})"

