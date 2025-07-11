from pathlib import Path
import re
import os
import shutil
import sys
from block_utils import markdown_to_html_node


def main():
    basepath = sys.argv[1] if len(sys.argv) > 1 else "/"
    public_dir = Path(__file__).parent.parent / "docs"
    static_dir = Path(__file__).parent.parent / "static"

    content_dir = Path(__file__).parent.parent / "content"
    template_path = Path(__file__).parent.parent / "template.html"

    if public_dir.exists() and public_dir.is_dir():
        shutil.rmtree(public_dir)

    # shutil.copytree(static_dir, public_dir)
    copy_file_tree(static_dir, public_dir)
    generate_pages_recursive(content_dir, template_path, public_dir, basepath)


def copy_file_tree(src, dst):
    os.makedirs(dst, exist_ok=True)

    for item in os.listdir(src):
        src_path = os.path.join(src, item)
        dst_path = os.path.join(dst, item)

        if os.path.isdir(src_path):
            copy_file_tree(src_path, dst_path)
        else:
            shutil.copy2(src_path, dst_path)


def extract_title(markdown):
    title = markdown.split("\n", 1)[0]
    match = re.match(r"^#[^#]", title.strip())
    if match:
        return title.strip(" #\t\n")
    else:
        raise Exception("No header provided")


def generate_pages_recursive(content_path, template_path, dest_dir_path, basepath):
    for root, dirs, files in os.walk(content_path):
        relative_path = os.path.relpath(root, content_path)
        current_dest_dir = os.path.join(dest_dir_path, relative_path)

        os.makedirs(current_dest_dir, exist_ok=True)

        for file in files:
            if file.endswith(".md"):
                from_path = os.path.join(root, file)
                html_filename = (
                    "index.html"
                    if file.lower() == "index.md"
                    else f"{os.path.splitext(file)[0]}.html"
                )
                final_dest_path = os.path.join(current_dest_dir, html_filename)
                generate_page(from_path, template_path, final_dest_path, basepath)


def generate_page(from_path, template_path, dest_path, basepath):
    print(f"Generating page from {from_path} to {dest_path} using {template_path}")

    with open(from_path, encoding="utf-8") as f:
        markdown = f.read()

    with open(template_path, encoding="utf-8") as f:
        template = f.read()

    html_string = markdown_to_html_node(markdown).to_html()
    title = extract_title(markdown)

    html_string = template.replace("{{ Content }}", html_string)
    html_string = html_string.replace("{{ Title }}", title)

    html_string = html_string.replace('href="/', f'href="{basepath}')
    html_string = html_string.replace('src="/', f'src="{basepath}')

    os.makedirs(os.path.dirname(dest_path), exist_ok=True)

    with open(dest_path, "w", encoding="utf-8") as f:
        f.write(html_string)


if __name__ == "__main__":
    main()
