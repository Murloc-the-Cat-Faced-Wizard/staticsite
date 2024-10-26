# Split the markdown into blocks
# Loop over each block:
#   Determine the type of block
#   Based on the type of block, create a new HTMLNode with the proper data
#   Assign the proper child HTMLNodes to the block node
# Make all the block nodes children to a single parent HTMLNode (div) and return it
# Children of lists need the <li> tag, both open and close </li> around each child of the list
# Code blocks should be surrounded by a <code> tag nested inside a <pre> tag. -> <pre><code>block text</code></pre>

# I've added line breaks to the end of every line through the remove_markdown_block_formating() function, so if the line breaks fuck shit up, that's where they are
# Also, just realized that my remove_markdown_block_formating() function for ordered lists might be wrong, as I might have to strip the number from the front of the line
# Do I need to worry about nested blocks?

from markdowntoblocks import markdown_to_blocks, block_to_blocktype
from texttotextnodes import text_to_textnodes
from textnodetohtmlnode import text_node_to_html_node
from parentnode import ParentNode

def markdown_to_html_node(markdown):
    final_html= ParentNode("div", [])
    markdown_blocks = markdown_to_blocks(markdown)
    for block in markdown_blocks:
        new_block = new_block_node(block)
        # !!!THIS IS WHERE YOUR \n ARE BEING REMOVED!!!
        # I believe the correct way to fix this is to add the \n at the end of every line in the block!
        split_block = remove_markdown_block_formating(block, new_block.tag)
        block_children = []
        for line in split_block:
            block_children.extend(check_for_list_wrap(line, new_block.tag))
        if new_block.tag == "pre":
            new_block.children[0].children.extend(block_children)
        else:
            new_block.children.extend(block_children)
        final_html.children.append(new_block)
    return final_html


def new_block_node(block):
    new_blocktype = block_to_blocktype(block)
    if new_blocktype == "code":
        return ParentNode("pre", [ParentNode("code", [])])
    return ParentNode(new_blocktype, [])


def line_to_html_nodes(line):
    text_node_list = text_to_textnodes(line)
    html_nodes = []
    for node in text_node_list:
        new_html_node = text_node_to_html_node(node)
        html_nodes.append(new_html_node)
    return html_nodes


def check_for_list_wrap(line, tag):
    block_children = []
    if tag == "code":
        pass
    if tag == "ul" or tag == "ol":
        line_parent = ParentNode("li", [])
        line_parent.children.extend(line_to_html_nodes(line))
        block_children.append(line_parent)
    else:
        leaves = line_to_html_nodes(line)
        block_children.extend(leaves)
    return block_children


def remove_markdown_block_formating(block, tag):
    split_block = block.split("\n")
    striped_block = []
    for line in split_block:
        if "h" in tag:
            striped_block.append(line.lstrip("# "))
        elif tag == "pre":
            striped_block.append(line.strip("```") + "\n")
        elif tag == "blockquote":
            striped_block.append(line.lstrip("> "))
        elif tag == "ul":
            if line.startswith("*"):
                striped_block.append(line.lstrip("* "))
            if line.startswith("-"):
                striped_block.append(line.lstrip("- "))
        elif tag == "ol":
            striped_block.append(line.lstrip("1234567890. "))
        else:
            striped_block.append(line)
    return striped_block
