import os
import shutil
from markdown_blocks import markdown_to_html_node
from htmlnode import HTMLNode, ParentNode, LeafNode
from extract_title import extract_title

def generate_page(from_path, template_path, dest_path,basepath):
    print(f"Generating page from {from_path} to {dest_path} using {template_path}")
    with open(from_path,"r") as f:
        from_md = f.read()
    with open(template_path,"r") as f:
        from_template = f.read()
    html_string = markdown_to_html_node(from_md).to_html()
    title = extract_title(from_md)
    finished_html_string = from_template.replace("{{ Title }}", title)
    finished_html_string = finished_html_string.replace("{{ Content }}", html_string)
    finished_html_string = finished_html_string.replace('href="/', f'href="{basepath}')
    finished_html_string = finished_html_string.replace('src="/', f'src="{basepath}')

    directory = os.path.dirname(dest_path)
    if directory != "":
        os.makedirs(directory, exist_ok=True)
    with open(dest_path,"w") as f:
        f.write(finished_html_string)

def generate_pages_recursive(dir_path_content, template_path, dest_dir_path,basepath):
    for entry in os.listdir(dir_path_content):
        entry_path = os.path.join(dir_path_content, entry)
        if os.path.isfile(entry_path):
            generate_page(entry_path, template_path, os.path.join(dest_dir_path,entry[:-3]+".html"),basepath)
        else:
            generate_pages_recursive(entry_path, template_path, os.path.join(dest_dir_path,entry),basepath)