import json
import uuid


class Braille_file:

    def __init__(self, name, chapters, text, braille, file_path):
        self.name = name
        self.chapters = chapters
        self.text = text
        self.braille = braille
        self.file_path = file_path
        self.id = uuid.uuid4()

    def get_chapters(self):
        return self.chapters

    def get_braille(self):
        return self.braille

    def get_text(self):
        return self.text


class Reader:

    # Store important variables like battery etc.
    def __init__(self, documents=None):
        self.documents = []

    # -------------------------------
    # Document management
    # -------------------------------
    def add_document(self, document: Braille_file):
        self.documents.append(document)

    def remove_document(self, document: Braille_file):
        pass

    # Load the list of books on Menu
    def get_all_documents(self):
        return self.documents

    def load_braille_file(self, file_path):
        with open(file_path, "r") as f:
            data = json.load(f)
        return Braille_file(
            name=data["name"],
            chapters=data["chapters"],
            text=data["text"],
            braille=data["braille"],
            file_path=file_path,
        )

    # -------------------------------
    # Data lookup in loaded documents
    # -------------------------------
    def get_chapters_and_braille(self, book):
        """Given the book name, return its chapters (list) and braille (list)"""
        path = f"documents/{book}.json"
        file_content = self.load_braille_file(path)
        self.add_document(file_content)
        for document in self.documents:
            if document.file_path == path:
                return document.get_chapters(), document.get_braille()
        return None

    def get_chapter_content(self, book, chapter_name):
        chapters, braille = self.get_chapters_and_braille(book)
        for idx, chapter in enumerate(chapters):
            if chapter == chapter_name:
                return braille[idx]

    def get_book_nums(self):
        pass

    def get_chapter_nums(self):
        pass
