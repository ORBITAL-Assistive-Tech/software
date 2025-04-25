import json
import uuid


class Braille_file:
    """Class to store braille documents"""

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
    """
    Class to access, handle, and format the braille documents.
    """

    # Will store other important variables like battery etc.
    def __init__(self, documents=None):
        self.documents = []

    # -------------------------------
    # Document management
    # -------------------------------
    def add_document(self, document: Braille_file):
        """Adds a Braille_file document to the list of documents."""
        self.documents.append(document)

    def remove_document(self, document: Braille_file):
        """Removes a Braille_file document from the list of documents."""
        pass

    # Load the list of books on Menu
    def get_all_documents(self):
        """Returns the list of all loaded documents."""
        return self.documents

    def load_braille_file(self, file_path):
        """
        Loads a braille file from a JSON file and returns a Braille_file object ready for use

        Args:
            file_path (str): Path to the JSON file containing Braille data

        Returns:
            Braille_file: An instance of the braille document
            that contains accessible features with matching names
        """
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
        """
        Returns chapters and Braille content for a given book name.

        Args:
            book (str): Name of the book (without extension).

        Returns:
            tuple: (list of chapters, list of braille content) or None if not found.
        """
        path = f"documents/{book}.json"
        file_content = self.load_braille_file(path)
        self.add_document(file_content)
        for document in self.documents:
            if document.file_path == path:
                return document.get_chapters(), document.get_braille()
        return None

    def get_chapter_content(self, book, chapter_name):
        """
        Returns the Braille content of a specific chapter in a book.

        Args:
            book (str): Name of the book.
            chapter_name (str): Name of the chapter.

        Returns:
            list: Braille content for the given chapter.
        """
        chapters, braille = self.get_chapters_and_braille(book)
        for idx, chapter in enumerate(chapters):
            if chapter == chapter_name:
                return braille[idx]

    def load_input(self, book, chapter):
        """
        Converts Braille chapter content into a standardized visual format for UI display,
        which includes flattening the content, inserting spacing cells between sections,
        and organizing the braille cells into rows and pages.

        Args:
            book (str): Name of the book.
            chapter (str): Chapter to be displayed.

        Returns:
            list or None:
                If valid, returns a list of lists.
                Each inner list represents a group of Braille cells to be displayed on one line.
        """
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

        total_cols = 40
        rows_per_page = 15

        rows = [
            flat_list[i : i + total_cols] for i in range(0, len(flat_list), total_cols)
        ]
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
