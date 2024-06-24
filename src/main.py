import os
import shutil
import mdutils


def copy(src: str, dst: str):
    if not os.path.exists(dst):
        os.mkdir(dst)
    for file in os.listdir(src):
        if os.path.isfile(src + "/" + file):
            shutil.copy(src + "/" + file, dst)
        elif os.path.isdir(src + "/" + file):
            copy(src + "/" + file, dst + "/" + file)


def generate_page(from_path: str, template_path: str, dest_path: str):
    if not os.path.exists(os.path.dirname(dest_path)):
        os.makedirs(os.path.dirname(dest_path))
    with open(from_path) as from_file:
        source = from_file.read()
    with open(template_path) as template_file:
        template = template_file.read()

    html_node = mdutils.markdown_to_HTMLNode(source)
    html_output = html_node.to_html()
    title = mdutils.extract_title(source)

    template = template.replace("{{ Title }}", title)
    template = template.replace("{{ Content }}", html_output)
    with open(dest_path, "w") as destination:
        destination.write(template)


def main():
    shutil.rmtree("public")
    copy("static", "public")
    generate_page("content/index.md", "template.html", "public/index.html")


if __name__ == "__main__":
    main()
