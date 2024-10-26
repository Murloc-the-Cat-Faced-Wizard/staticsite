from textnode import TextNode, TextType


def split_nodes_delimiter(old_nodes, delimiter, text_type):
    new_nodes = []
    if len(old_nodes)>1:
        new_nodes.extend(split_nodes_delimiter(old_nodes[:-1], delimiter, text_type))
    match text_type:
        case TextType.BOLD:
            new_nodes.extend(func1(old_nodes[-1], delimiter, text_type))
        case TextType.ITALIC:
            # Intresting artefact, if * is the delimiter and the markdown text includes **, it don't work so good
            new_nodes.extend(func1(old_nodes[-1], delimiter, text_type))
        case TextType.CODE:
            new_nodes.extend(func1(old_nodes[-1], delimiter, text_type))
        case _:
            new_nodes.append(old_nodes[-1])  
    return new_nodes


def func1(node, delimiter, text_type):
    new_nodes = []
    if delimiter not in node.text:
        return [node]
    if delimiter in node.text[node.text.index(delimiter)+1:]:
        sections = node.text.split(delimiter, maxsplit=2)
            #if delimiter in x[2]:
                #recur_nodes.extend(func1(TextNode(text=x[2], text_type=node.text_type), delimiter, text_type))
    else:
        print(node.text)
        raise Exception("No closing delimiter")
    if sections[0]:
        new_nodes.append(TextNode(sections[0], node.text_type))
    new_nodes.append(TextNode(sections[1], text_type))
    if sections[2]:
        #new_nodes.append(TextNode(sections[2], node.text_type))
        #new_nodes.extend([TextNode(x[0], node.text_type), TextNode(x[1], text_type), TextNode(x[2], node.text_type)])
        if delimiter in sections[2]:
            new_nodes.extend(func1(TextNode(text=sections[2], text_type=node.text_type), delimiter, text_type))
        else:
            new_nodes.append(TextNode(sections[2], node.text_type))
    #if recur_nodes:
        #new_nodes.extend(recur_nodes[1:])
    return new_nodes
    


"""
def split_nodes_delimiter(old_nodes, delimiter, text_type):
    new_nodes = []
    for node in old_nodes:
        match text_type:
            case TextType.BOLD:
                new_nodes.extend(func1(node, delimiter, text_type))
            case TextType.ITALIC:
                # Intresting artefact, if * is the delimiter and the markdown text includes **, it don't work so good
                new_nodes.extend(func1(node, delimiter, text_type))
            case TextType.CODE:
                new_nodes.extend(func1(node, delimiter, text_type))
            case _:
                new_nodes.append(old_nodes[0])  
    return new_nodes
"""