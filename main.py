from view import View
from controller import Controller
from model import Person


def main():
    control = Controller()
    control.docx_to_text(
        "path/to/your/pdf/file.pdf", "path/to/output/textfile.txt"
    )  # Replace the pathsto what you want
    # control.text_to_braille("hello")


if __name__ == "__main__":
    main()
