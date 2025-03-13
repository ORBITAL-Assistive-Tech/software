from view import View
from controller import Controller
from model import Reader
import os
import warnings


def main():
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


if __name__ == "__main__":
    main()
