import json
from model import BrailleFile, Reader


class Controller:
    """
    This class is controls the interaction between the model and view
    """

    def __init__(self, reader):
        self.reader = reader

    def pdf_to_text(self, path_to_pdf):
        pass

    def text_to_braille(self, text):
        pass

    def load_braille_file(self, path_to_braille_file):
        with open(path_to_braille_file, "r+") as f:
            data = json.load(f)
            braille_file = BrailleFile(
                data["text"], data["braille"], path_to_braille_file
            )
            self.reader.add_document(braille_file)

    def save_braille_file(self, text, braille):
        data = {"text": text, "braille": braille}
        with open("documents/book2.txt", "w") as f:
            json.dump(data, f, ensure_ascii=False)
