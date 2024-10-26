import os
import shutil
import json
from markdowntohtmlnode import markdown_to_html_node

#['./static/rivendell.png', './static/rivendell.png:Zone.Identifier', './static/index.css', './static/test_dir/test_dir_2_test_2_fileous/dfjsij.txt', './static/test_dir/test_dir_tier_2/file_in_tier_2.txt', './static/test_dir/test_file.txt']

def main():
    set_up_public()


def set_up_public():
    if os.path.exists("public"):
        shutil.rmtree("public")
    os.mkdir("public")
    to_copy = os.listdir("static")
    full_filepaths = get_dir_paths_to_copy(to_copy, "static")
    print(full_filepaths)
    generate_pages_recusive("content", "template.html", "public")


def get_dir_paths_to_copy(current_dir_list, current_file_path):
    filepath_list = []
    if not current_dir_list:
        return filepath_list
    if len(current_dir_list) > 1:
        filepath_list.extend(get_dir_paths_to_copy(current_dir_list[1:], current_file_path))
    file_path = os.path.join(current_file_path, current_dir_list[0])
    if not os.path.isfile(file_path):
        public_dir = "public" + file_path[6:]
        if not os.path.exists(public_dir):
            os.mkdir(public_dir)
        filepath_list.extend(get_dir_paths_to_copy(os.listdir(file_path), file_path))
    else:
        public_dir = "public" + file_path[6:].rstrip(current_dir_list[0])
        shutil.copy(file_path, public_dir)
        #copy_to_public(file_path, current_dir_list[0])
        filepath_list.append(file_path)
    return filepath_list


# Currently not using this function, but I'll keep it around in case it proves useful for the next step
def copy_to_public(static_dir, file):
    public_dir = "public" + static_dir[8:].rstrip(file)
    shutil.copy(static_dir, public_dir)


def extract_title(markdown):
    split_doc = markdown.split("\n")
    for line in split_doc:
        if line.startswith("# "):
            return line.strip("# ")
    raise Exception("Markdown has no h1 headers")


def generate_page(from_path, template_path, dest_path):
    print(f"Generating page from {from_path} to {dest_path} using {template_path}")
    with open(from_path, "r") as f:
        markdown_file = f.read()
    with open(template_path, "r") as f:
        template_file = f.read()
    full_html_node = markdown_to_html_node(markdown_file)
    full_html_str = full_html_node.to_html()
    title = extract_title(markdown_file)
    template_file = template_file.replace("{{ Title }}", title)
    template_file = template_file.replace("{{ Content }}", full_html_str)
    if not os.path.exists(os.path.dirname(dest_path)):
        os.makedirs(os.path.dirname(dest_path))
    dest_path = dest_path.replace(".md", ".html")
    with open(dest_path, 'w') as f:
        f.write(template_file)
        #json.dump(template_file, f)


def generate_pages_recusive(dir_path_content, template_path, dest_dir_path):
    #print(f"Generating page from {dir_path_content} to {dest_dir_path} using {template_path}")
    files = os.listdir(dir_path_content)
    for file in files:
        if os.path.isfile(os.path.join(dir_path_content, file)):
            generate_page(os.path.join(dir_path_content, file), template_path, os.path.join(dest_dir_path, file))
        else:
            generate_pages_recusive(os.path.join(dir_path_content, file), template_path, os.path.join(dest_dir_path, file))


main()
