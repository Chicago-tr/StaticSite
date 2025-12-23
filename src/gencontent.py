import os
from pathlib import Path

from markdown_blocks import markdown_to_html_node


def extract_title(markdown: str):
    lines = markdown.splitlines()
    for line in lines:
        stripped = line.lstrip()
        if stripped.startswith("# "):
            line = line.lstrip("#")
            line = line.strip()
            return line

    raise Exception("no title found")


def generate_page(from_path, template_path, dest_path, basepath):
    print(f"Generating page {from_path} to {dest_path} using {template_path}")
    with open(from_path, "r") as f:
        from_md_file = f.read()

    with open(template_path, "r") as f:
        template_md_file = f.read()

    from_htmlnode = markdown_to_html_node(from_md_file)
    from_html_string = from_htmlnode.to_html()
    html_title = extract_title(from_md_file)

    page = template_md_file.replace("{{ Title }}", html_title)
    page = page.replace("{{ Content }}", from_html_string)
    page = page.replace('href="/', 'href="' + basepath)
    page = page.replace('src="/', 'src="' + basepath)

    dirpath = os.path.dirname(dest_path)
    if dirpath != "":
        os.makedirs(dirpath, exist_ok=True)

    with open(dest_path, "w") as f:
        f.write(page)


def generate_pages_recursive(dir_path_content, template_path, dest_dir_path, basepath):
    print(
        f"Generating page {dir_path_content} to {dest_dir_path} using {template_path}"
    )

    for file in os.listdir(dir_path_content):
        from_path = os.path.join(dir_path_content, file)
        dest_path = os.path.join(dest_dir_path, file)

        if os.path.isfile(from_path):
            dest_path = Path(dest_path).with_suffix(".html")
            generate_page(from_path, template_path, dest_path, basepath)

        else:
            generate_pages_recursive(from_path, template_path, dest_path, basepath)
