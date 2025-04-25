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
        """
        Load a Braille file from a given path and add it to the list of documents in Reader.

        Args:
            path_to_braille_file (str): Path to a JSON Braille file.
        """
        braille_file = self.reader.load_braille_file(path_to_braille_file)
        self.reader.add_document(braille_file)

    def save_braille_file(self, text, braille):
        """
        Save the given text and Braille data to a new JSON file.

        Args:
            text (str): The original text.
            braille (list of str): The braille representation of the text.
            Each string is a 6-digit sequence of '0's and '1's representing a braille cell.
        """
        data = {"text": text, "braille": braille}
        with open(
            f"documents/book{len(self.reader.get_all_documents())+1}.json", "w"
        ) as f:
            json.dump(data, f, ensure_ascii=False)

    def go_to_page(self, target_page, braille_pages):
        """
        Navigate to a specific page in the Braille document.

        Args:
            target_page (int): Index of the target page.
            braille_pages (list): List of braille content in all pages.

        Returns:
            list of lists or None: If valid, list of the content to be displayed on the given page.
            Each inner list represents a group of Braille cells to be displayed on one line.
        """
        if 0 <= target_page < len(braille_pages):
            self.page_index = target_page
            return braille_pages[self.page_index]
        else:
            print("Invalid page number.")
            return None

    def next_page(self, braille_pages):
        """
        Move to the next page, if possible.

        Args:
            braille_pages (list): List of braille content in all pages.

        Returns:
            list of lists: if available, the content to be displayed on the next page.
            None: if already at the last page
        """
        if self.page_index < len(braille_pages) - 1:
            self.page_index += 1
            return braille_pages[self.page_index]
        else:
            print("Already at the last page.")
            return None

    def prev_page(self, braille_pages):
        """
        Move to the previous page, if possible.

        Args:
            braille_pages (list): List of braille content in all pages.

        Returns:
            list of lists: if available, the content to be displayed on the previous page.
            None: if already at the last page
        """
        if self.page_index > 0:
            self.page_index -= 1
            return braille_pages[self.page_index]
        else:
            print("Already at the first page.")
            return None

    def docx_to_braille(self, filepath):
        """
        Convert a .docx file to text, then to braille, and save the result.

        Args:
            filepath (str): Path to the .docx file to be converted.
        """
        text = docs.docx_to_txt(filepath)
        braille = self.text_to_braille(text)
        self.save_braille_file(text, braille)

    def brf_to_braille(self, filepath):
        """
        Read a .brf Braille file, extract its content, and save the text and braille representation.

        Args:
            filepath (str): Path to the .brf file.
        """
        data = brf.brf_to_binary(filepath)
        text = data[0]
        braille = data[1]
        self.save_braille_file(text, braille)
