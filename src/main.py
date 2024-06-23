import os, shutil


def copy(src: str, dst: str):
    if not os.path.exists(dst):
        os.mkdir(dst)
    for file in os.listdir(src):
        if os.path.isfile(src + "/" + file):
            shutil.copy(src + "/" + file, dst)
        elif os.path.isdir(src + "/" + file):
            copy(src + "/" + file, dst + "/" + file)


def main():
    shutil.rmtree("../public")
    copy("../static", "../public")


if __name__ == "__main__":
    main()
