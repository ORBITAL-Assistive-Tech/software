from view import View
from controller import Controller
from model import Reader


def main():
    reader = Reader()
    control = Controller(reader)
    control.load_braille_file("documents/book1.txt")
    print(reader.get_all_documents()[0].get_text())


if __name__ == "__main__":
    main()
