import os
import shutil
import sys

from copystatic import copy_files_recursive
from generate_page import generate_page, generate_pages_recursive


dir_path_static = "./static"
dir_path_public = "./docs"
from_path = "./content/index.md"
template_path = "./template.html"
dir_path_content = "./content"
basepath = "/"
if len(sys.argv)>1:
    basepath = sys.argv[1]


def main():
    print("Deleting public directory...")
    if os.path.exists(dir_path_public):
        shutil.rmtree(dir_path_public)

    print("Copying static files to public directory...")
    copy_files_recursive(dir_path_static, dir_path_public)
    generate_pages_recursive(dir_path_content, template_path, dir_path_public,basepath)


main()
