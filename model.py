import json


class Braille_file:

    def __init__(self, text, braille, file_path):
        self.file_path = file_path
        self.text = text
        self.braille = braille
        self.id = 0
        pass

    def get_braille(self):
        return self.braille

    def get_text(self):
        return self.text


class Reader:

    # Store important variables like battery etc.
    def __init__(self, documents=None):
        self.documents = []

    def add_document(self, document: Braille_file):
        self.documents.append(document)

    def remove_document(self, document: Braille_file):
        pass

    # Load braille from a book
    def get_braille_in_document(self, file_path):
        for document in self.documents:
            if document.file_path == file_path:
                return document.get_braille()
        return None

    def load_braille_file(self, file_path):
        with open(file_path, "r") as f:
            data = json.load(f)
        return Braille_file(
            text=data["text"], braille=data["braille"], file_path=file_path
        )

    # Load the list of books on menu
    def get_all_documents(self):
        return self.documents

    # Load braille content
    def get_content(self, book, chapter="chapter1"):
        path = f"documents/{book}/{chapter}.txt"
        chapter_content = self.load_braille_file(path)
        self.add_document(chapter_content)
        braille_input = self.get_braille_in_document(chapter_content.file_path)
        return braille_input

    def get_book_nums(self):
        pass

    def get_chapter_nums(self):
        pass
