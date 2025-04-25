import tkinter as tk
from tkinter import ttk
from controller import Controller
from model import Reader
import json

reader = Reader()
controller = Controller(reader)


class Menu(tk.Tk):
    """
    Main window for the Braille Reader.

    Displays buttons for all available Braille documents loaded into the system.
    Each button opens a new window showing the chapters of the corresponding book.

    Attributes:
        documents (list): A list of Braille_file instances available for reading.
        book_choice (int): The index of the selected book.
    """

    def __init__(self):
        super().__init__()
        self.geometry("1600x900")
        self.title("Braille Reader Menu")
        self.documents = reader.get_all_documents()
        self.book_choice = None
        for i in range(len(self.documents)):
            ttk.Button(
                self, text=f"Book {i+1}", command=lambda i=i: self.open_chapter_page(i)
            ).pack(expand=True)

    def open_chapter_page(self, i):
        self.book_choice = i + 1
        self.chapter = Chapter(self)


class Chapter(tk.Toplevel):
    """
    Chapter selection window for a chosen book.

    Shows all available chapters in the selected book and allows users to select one
    to view its braille content. Also has a button to return to the main menu.

    Attributes:
        book_choice (int): Index of the selected book.
        chapter_list (list): List of chapter names in the book.
        content_list (list): List of Braille content corresponding to each chapter.
    """

    def __init__(self, parent):
        super().__init__(parent)
        self.book_choice = parent.book_choice
        self.parent = parent
        (self.chapter_list, self.content_list) = reader.get_chapters_and_braille(
            f"book{self.book_choice}"
        )
        self.geometry("1600x900")
        self.title("Braille Reader")

        for i in range(len(self.chapter_list)):
            ttk.Button(
                self,
                text=f"Chapter {i+1}",
                command=lambda i=i: self.open_content_page(i),
            ).pack(expand=True)

        ttk.Button(self, text="Back to Main Menu", command=self.return_to_main).pack(
            pady=10
        )

    def open_content_page(self, i):
        self.chapter_choice = i + 1
        self.chapter = Content(self)

    def return_to_main(self):
        self.destroy()
        self.parent.deiconify()


class Content(tk.Toplevel):
    """
    Content display window for a specific chapter of a book.
    """

    def __init__(self, parent):
        super().__init__(parent)
        self.book_choice = parent.book_choice
        self.chapter_choice = parent.chapter_choice
        self.parent = parent
        self.geometry("1600x900")
        self.title("Content Display")

        self.dot_size = 6
        self.spacing = 8
        self.row_spacing = 40

        self.canvas = tk.Canvas(self, width=1500, height=650, bg="white")
        self.canvas.pack(pady=10)

        self.merged_braille_input_wpages = reader.load_input(
            f"book{self.book_choice}", f"Chapter {self.chapter_choice}"
        )
        self.update_canvas(f"book{self.book_choice}", f"Chapter {self.chapter_choice}")

        self.forward_btn = tk.Button(
            self,
            text="Forward",
            command=lambda: self.next_page(self.merged_braille_input_wpages),
        )
        self.forward_btn.pack(side="right", padx=10)

        self.back_btn = tk.Button(
            self,
            text="Back",
            command=lambda: self.prev_page(self.merged_braille_input_wpages),
        )
        self.back_btn.pack(side="left", padx=10)

        self.close_btn = ttk.Button(
            self, text="Back to Book Chapters", command=self.destroy
        )
        self.close_btn.pack(side="bottom", pady=5)

    def draw_braille(self, page_content):
        """
        Draws the Braille cells (6 dots each cell) representing the braille content.

        Args:
            page_content (list of lists): the content to be displayed on the given page.
            Each inner list represents a row of Braille cells.
        """
        self.canvas.delete("all")
        x_offset = 20
        y_offset = 20
        for row_idx, braille_row in enumerate(page_content):
            for char_idx, braille in enumerate(braille_row):
                for i, bit in enumerate(braille):
                    col = i % 2
                    row = i // 2
                    x = x_offset + col * self.spacing + char_idx * 50
                    y = y_offset + row * self.spacing + row_idx * self.row_spacing
                    if bit == "1":
                        self.canvas.create_oval(
                            x, y, x + self.dot_size, y + self.dot_size, fill="black"
                        )
                    else:
                        self.canvas.create_oval(
                            x, y, x + self.dot_size, y + self.dot_size, outline="black"
                        )

    def update_canvas(self, book, chapter):
        """
        Updates the canvas with the new Braille content for the selected book and chapter.

        Args:
            book (str): The name of the selected book.
            chapter (str): The name of the selected chapter.
        """
        merged_braille_input_wpages = reader.load_input(book, chapter)
        page_content = controller.go_to_page(
            controller.page_index, merged_braille_input_wpages
        )
        if page_content:
            self.draw_braille(page_content)

    def next_page(self, merged_braille_input_wpages):
        """
        Displays the next page of Braille content in the document.

        Args:
            merged_braille_input_wpages (list): A list of pages containing all braille content.
        """
        page_content = controller.next_page(merged_braille_input_wpages)
        if page_content:
            self.draw_braille(page_content)

    def prev_page(self, merged_braille_input_wpages):
        """
        Displays the previous page of Braille content in the document.

        Args:
            merged_braille_input_wpages (list): A list of pages containing all braille content.
        """
        page_content = controller.prev_page(merged_braille_input_wpages)
        if page_content:
            self.draw_braille(page_content)


if __name__ == "__main__":
    view = Menu()
    view.mainloop()
