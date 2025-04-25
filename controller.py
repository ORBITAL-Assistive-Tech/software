import json
from model import BrailleFile, Reader
import utils.docx as docs
import utils.brf as brf

import pybrl as brl
import louis


class Controller:
    """
    This class is controls the interaction between the model and view
    """

    def __init__(self, reader):
        self.reader = reader

    def text_to_braille(self, text):
        """
        Convert text into 40 character lines of braille

        Args:
            text (str): text to convert into braille
                assumed to have only line feeds (\n) for new lines

        Returns:
            A list of lines, which contain up to 40 strings, each representing a character
        """
        paragraphs = text.split("\n\n")
        braille_list = []
        for l in paragraphs:
            braille = brl.translate(l)
            paragraph = []
            for word in braille:
                for letter in word:
                    paragraph.append(letter)
                paragraph.append("")
            paragraph = paragraph[:-1]
            while len(paragraph) > 0:
                # removes leading spaces from line
                # not sure if this is the right move so commented out
                # while len(paragraph[0]) < 1:
                #    paragraph.pop(0)
                braille_list.append(paragraph[0:40])
                paragraph = paragraph[40:]
            braille_list.append([])

        braille_list = braille_list[:-1]  # remove trailing empty line

        return braille_list

    def text_to_brf(self, text):
        """
        Convert text into braille ready format (BRF)

        Args:
            text (str): text to convert into BRF

        Returns:
            A string with the BRF translation
        """
        string = louis.translateString(
            ["en-us-brf.dis", "en-us-g2.ctb"],
            text,
        )
        brf_lines = []
        while len(string) > 0:
            brf_lines.append(string[0:40])
            string = string[40:]
        return "\n".join(brf_lines)

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
