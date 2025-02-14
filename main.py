from view import View
from controller import Controller
from model import Reader


def main():
    reader = Reader()
    control = Controller(reader)
    control.load_braille_file("documents/book1.txt")
    control.upload_text_file("documents/test.txt")


if __name__ == "__main__":
    main()
