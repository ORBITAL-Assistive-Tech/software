import json
from model import Braille_file, Reader


class Controller:
    """
    This class controls the interaction between the model and view
    """

    def __init__(self, reader):
        self.reader = reader
        self.page_index = 0

    def pdf_to_text(self, path_to_pdf):
        pass

    def text_to_braille(self, text):
        pass

    def load_braille_file(self, path_to_braille_file):
        with open(path_to_braille_file, "r+") as f:
            data = json.load(f)
            braille_file = Braille_file(
                data["text"], data["braille"], path_to_braille_file
            )
            self.reader.add_document(braille_file)

    def save_braille_file(self, text, braille):
        data = {"text": text, "braille": braille}
        with open("documents/book2.txt", "w") as f:
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
