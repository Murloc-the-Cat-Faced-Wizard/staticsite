import re
from textnode import TextNode, TextType

# images
# r"!\[([^\[\]]*)\]\(([^\(\)]*)\)"

# regular links
# r"(?<!!)\[([^\[\]]*)\]\(([^\(\)]*)\)"

def extract_markdown_images(text):
    # ![alt text for image](url/of/image.jpg)
    # "This is text with a ![rick roll](https://i.imgur.com/aKaOqIh.gif) and ![obi wan](https://i.imgur.com/fJRm4Vk.jpg)"
    # !\[(.*?)\]\((.*?)\)
    first_search = re.findall(r"!\[([^\[\]]*)\]\(([^\(\)]*)\)", text)
    if not first_search:
        return None
    tuple_list = []
    for res in range(0, len(first_search)):
        tuple_list.append(first_search[res])
    return tuple_list


def extract_markdown_links(text):
    # This is a paragraph with a [link](https://www.google.com).
    first_search = re.findall(r"(?<!!)\[([^\[\]]*)\]\(([^\(\)]*)\)", text)
    if not first_search:
        return None
    tuple_list = []
    for res in range(0, len(first_search)):
        tuple_list.append(first_search[res])
    return tuple_list


def split_nodes_images(old_nodes):
    new_nodes = []
    recur_nodes = []
    if len(old_nodes) > 1:
        recur_nodes.extend(split_nodes_images(old_nodes[1:]))
    list_of_img_tuples = extract_markdown_images(old_nodes[0].text)
    if not list_of_img_tuples:
        new_nodes.append(old_nodes[0])
        if recur_nodes:
            new_nodes.extend(recur_nodes)
        return new_nodes
    new_nodes.append(old_nodes[0])
    for img in range(0, len(list_of_img_tuples)):
        img_alt = list_of_img_tuples[img][0]
        img_link = list_of_img_tuples[img][1]
        sections = new_nodes.pop().text.split(f"![{img_alt}]({img_link})", maxsplit=1)
        if sections[0]:
            new_nodes.append(TextNode(sections[0], TextType.TEXT))
        new_nodes.append(TextNode(img_alt, TextType.IMAGE, img_link))
        if sections[1]:
            new_nodes.append(TextNode(sections[1], TextType.TEXT))
    if recur_nodes:
        new_nodes.extend(recur_nodes)
    return new_nodes


def split_nodes_links(old_nodes):
    new_nodes = []
    recur_nodes = []
    if len(old_nodes) > 1:
        recur_nodes.extend(split_nodes_links(old_nodes[1:]))
    list_of_link_tuples = extract_markdown_links(old_nodes[0].text)
    if not list_of_link_tuples:
        new_nodes.append(old_nodes[0])
        if recur_nodes:
            new_nodes.extend(recur_nodes)
        return new_nodes
    new_nodes.append(old_nodes[0])
    for link in range(0, len(list_of_link_tuples)):
        link_text = list_of_link_tuples[link][0]
        link_url = list_of_link_tuples[link][1]
        sections = new_nodes.pop().text.split(f"[{link_text}]({link_url})", maxsplit=1)
        if sections[0]:
            new_nodes.append(TextNode(sections[0], TextType.TEXT))
        new_nodes.append(TextNode(link_text, TextType.LINK, link_url))
        if sections[1]:
            new_nodes.append(TextNode(sections[1], TextType.TEXT))
    if recur_nodes:
        new_nodes.extend(recur_nodes)
    return new_nodes
