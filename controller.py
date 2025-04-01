import json
from model import BrailleFile, Reader
import utils.docx as docs
import utils.brf as brf

import sys

sys.path.append("/home/koroko/Workspace/pybrl")

import pybrl as brl

# /home/koroko/Workspace/pybrl


class Controller:
    """
    This class is controls the interaction between the model and view
    """

    def __init__(self, reader):
        self.reader = reader

    def text_to_braille(self, text):
        return brl.translate(text)

    def upload_text_file(self, path):
        with open(path, "r") as f:
            text = "".join(f.readlines())
            braille = brl.translate(text)
            braille_file = BrailleFile(text, braille, path)
            self.reader.add_document(braille_file)
            self.save_braille_file(text, braille)

    def load_braille_file(self, path_to_braille_file):
        with open(path_to_braille_file, "r+") as f:
            data = json.load(f)
            braille_file = BrailleFile(
                data["text"], data["braille"], path_to_braille_file
            )
            self.reader.add_document(braille_file)

    def save_braille_file(self, text, braille):
        data = {"text": text, "braille": braille}
        with open(
            f"documents/book{len(self.reader.get_all_documents())+1}.json", "w"
        ) as f:
            json.dump(data, f, ensure_ascii=False)

    def docx_to_braille(self, filepath):
        text = docs.docx_to_txt(filepath)
        braille = self.text_to_braille(text)
        self.save_braille_file(text, braille)

    def brf_to_braille(self, filepath):
        data = brf.brf_to_binary(filepath)
        text = data[0]
        braille = data[1]
        self.save_braille_file(text, braille)
