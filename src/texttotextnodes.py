from textnode import TextNode, TextType
from extractmarkdown import split_nodes_images, split_nodes_links
from splitnodesdelimiter import split_nodes_delimiter


def text_to_textnodes(text):
    nodes_list = []
    nodes_list.append(TextNode(text, TextType.TEXT))
    nodes_list = split_nodes_delimiter(nodes_list, "**", TextType.BOLD)
    nodes_list = split_nodes_delimiter(nodes_list, "*", TextType.ITALIC)
    nodes_list = split_nodes_delimiter(nodes_list, "`", TextType.CODE)
    nodes_list = split_nodes_images(nodes_list)
    nodes_list = split_nodes_links(nodes_list)
    return nodes_list
