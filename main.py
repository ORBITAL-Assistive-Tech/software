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
    control.docx_to_braille(
        "/home/koroko/Workspace/orbital_software/test_materials/superman_and_me.docx"
    )
    control.brf_to_braille(
        "/home/koroko/Workspace/orbital_software/test_materials/The_Giver.brf"
    )


if __name__ == "__main__":
    main()
