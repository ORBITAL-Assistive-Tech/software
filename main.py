from view import View
from controller import Controller
from model import Reader
import os
import warnings


def main():
<<<<<<< HEAD
    control = Controller()
    control.docx_to_text(
        "path/to/your/pdf/file.pdf", "path/to/output/textfile.txt"
    )  # Replace the pathsto what you want
    # control.text_to_braille("hello")
=======
    reader = Reader()
    control = Controller(reader)
    for f in os.listdir("documents"):
        if not os.path.isfile(f"documents/{f}"):
            continue
        _, extension = os.path.splitext(f)
        if extension == ".pdf":
            pass
        if extension == ".txt":
            control.upload_text_file(f"documents/{f}")
            continue
        if extension == ".json":
            control.load_braille_file(f"documents/{f}")
            continue
        warnings.warn(f"{f} did not have a recognized file extension")
    for d in control.reader.documents:
        print(d.id)
>>>>>>> 31782f415a9b964a66482d4947818017c7d5b145


if __name__ == "__main__":
    main()
