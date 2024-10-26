
def markdown_to_blocks(markdown):
    split_doc = markdown.split("\n\n")
    removed_blanks = []
    for block in split_doc:
        if block:
            split_lines = block.split("\n")
            lst= []
            for line in split_lines:
                if line:
                    #lst.append(line.strip())
                    lst.append(line)
            removed_blanks.append("\n".join(lst))
    return removed_blanks


def block_to_blocktype(block):
    split_block = block.split("\n")
    type_list = []
    for blk in range(0, len(split_block)):
        if split_block[blk].startswith("#"):
            if split_block[blk].startswith("# "):
                type_list.append("heading1")
            elif split_block[blk].startswith("## "):
                type_list.append("heading2")
            elif split_block[blk].startswith("### "):
                type_list.append("heading3")
            elif split_block[blk].startswith("#### "):
                type_list.append("heading4")
            elif split_block[blk].startswith("##### "):
                type_list.append("heading5")
            elif split_block[blk].startswith("###### "):
                type_list.append("heading6")
            else:
                type_list.append("nope")
        elif (blk == 0 and split_block[blk].startswith("```")) or (blk == len(split_block)-1 and split_block[blk].endswith("```")):
            type_list.append("code")
        elif split_block[blk].startswith(">"):
            type_list.append("quote")
        elif split_block[blk].startswith("* ") or split_block[blk].startswith("- "):
            type_list.append("un list")
        elif split_block[blk].startswith(f"{blk+1}. "):
            type_list.append("ord list")
        else:
            type_list.append("nope")
    if type_list.count("heading1") == len(split_block):
        return "h1"
    elif type_list.count("heading2") == len(split_block):
        return "h2"
    elif type_list.count("heading3") == len(split_block):
        return "h3"
    elif type_list.count("heading4") == len(split_block):
        return "h4"
    elif type_list.count("heading5") == len(split_block):
        return "h5"
    elif type_list.count("heading6") == len(split_block):
        return "h6"
    elif type_list[0] == "code" and  type_list[len(type_list)-1] == "code":
        return "code"
    elif type_list.count("quote") == len(split_block):
        return "blockquote"
    elif type_list.count("un list") == len(split_block):
        return "ul"
    elif type_list.count("ord list") == len(split_block):
        return "ol"
    else:
        return "p"
