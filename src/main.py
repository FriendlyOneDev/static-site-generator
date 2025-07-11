from pathlib import Path
import re
import os
import shutil
from block_utils import markdown_to_html_node


def main():
    public_dir = Path(__file__).parent.parent / "public"
    static_dir = Path(__file__).parent.parent / "static"

    markdown_path = Path(__file__).parent.parent / "content/index.md"
    template_path = Path(__file__).parent.parent / "template.html"

    if public_dir.exists() and public_dir.is_dir():
        shutil.rmtree(public_dir)

    # shutil.copytree(static_dir, public_dir)
    copy_file_tree(static_dir, public_dir)

    generate_page(markdown_path, template_path, public_dir)


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


def generate_page(from_path, template_path, dest_path):
    print(f"Generating page from {from_path} to {dest_path} using {template_path}")

    with open(from_path) as f:
        markdown = f.read()

    with open(template_path) as f:
        template = f.read()

    html_string = markdown_to_html_node(markdown).to_html()
    title = extract_title(markdown)

    html_string = template.replace("{{ Content }}", html_string)
    html_string = html_string.replace("{{ Title }}", title)

    with open(f"{dest_path}/index.html", "w", encoding="utf-8") as f:
        f.write(html_string)


if __name__ == "__main__":
    main()
