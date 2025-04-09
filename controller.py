import json
import os
import sys
from model import Braille_file, Reader
import utils.docx as docs
import utils.brf as brf
import warnings

# /home/koroko/Workspace/pybrl


class Controller:
    """
    This class controls the interaction between the model and view
    """

    def __init__(self, reader):
        self.reader = reader
        self.page_index = 0

        for f in os.listdir("documents"):
            if not os.path.isfile(f"documents/{f}"):
                continue
            _, extension = os.path.splitext(f)
            if extension == ".pdf":
                continue
            if extension == ".json":
                self.load_braille_file(f"documents/{f}")
                continue
            warnings.warn(f"{f} did not have a recognized file extension")

    def text_to_braille(self, text):
        return []

    def load_braille_file(self, path_to_braille_file):
        with open(path_to_braille_file, "r+") as f:
            data = json.load(f)
            braille_file = Braille_file(
                data["text"], data["braille"], path_to_braille_file
            )
            self.reader.add_document(braille_file)

    def save_braille_file(self, text, braille):
        data = {"text": text, "braille": braille}
        with open(
            f"documents/book{len(self.reader.get_all_documents())+1}.json", "w"
        ) as f:
            json.dump(data, f, ensure_ascii=False)

    def go_to_page(self, target_page, braille_pages):
        if 0 <= target_page < len(braille_pages):
            self.page_index = target_page
            return braille_pages[self.page_index]
        else:
            print("Invalid page number.")
            return None

    def next_page(self, braille_pages):
        if self.page_index < len(braille_pages) - 1:
            self.page_index += 1
            return braille_pages[self.page_index]
        else:
            print("Already at the last page.")
            return None

    def prev_page(self, braille_pages):
        if self.page_index > 0:
            self.page_index -= 1
            return braille_pages[self.page_index]
        else:
            print("Already at the first page.")
            return None

    def docx_to_braille(self, filepath):
        text = docs.docx_to_txt(filepath)
        braille = self.text_to_braille(text)
        self.save_braille_file(text, braille)

    def brf_to_braille(self, filepath):
        data = brf.brf_to_binary(filepath)
        text = data[0]
        braille = data[1]
        self.save_braille_file(text, braille)
