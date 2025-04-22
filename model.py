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
        """Given the book name and chapter number, return the chapter's braille content"""
        chapters, braille = self.get_chapters_and_braille(book)
        for idx, chapter in enumerate(chapters):
            if chapter == chapter_name:
                return braille[idx]

    
    def load_input(self, book, chapter):
        '''Load the braille and write it into 6 dots format to display in tkinter'''
        braille_input = self.get_chapter_content(book, chapter)

        empty_cell = "000000"
        merged_braille_input = []

        if braille_input:
            merged_row = []
            for i, word_list in enumerate(braille_input):
                merged_row.extend(word_list)
                if i < len(braille_input) - 1:
                    merged_row.append(empty_cell)
            merged_braille_input.append(merged_row)

        flat_list = merged_braille_input[0]

        total_cols = 15
        rows_per_page = 10

        rows = [flat_list[i : i + total_cols] for i in range(0, len(flat_list), total_cols)]
        for row in rows:
            while len(row) < total_cols:
                row.append(empty_cell)

        merged_braille_input_wpages = [
            rows[i : i + rows_per_page] for i in range(0, len(rows), rows_per_page)
        ]
        for page in merged_braille_input_wpages:
            while len(page) < rows_per_page:
                page.append([empty_cell] * total_cols)

        print("Total pages:", len(merged_braille_input_wpages))
        return merged_braille_input_wpages

    def get_book_nums(self):
        pass

    def get_chapter_nums(self):
        pass
