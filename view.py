import tkinter as tk
from tkinter import ttk
from controller import Controller
from model import Reader
import json

reader = Reader()
controller = Controller(reader)


class Menu(tk.Tk):
    def __init__(self):
        super().__init__()
        self.geometry("1200x900")
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
    def __init__(self, parent):
        super().__init__(parent)
        self.book_choice = parent.book_choice
        self.parent = parent
        (self.chapter_list, self.content_list) = reader.get_chapters_and_braille(
            f"book{self.book_choice}"
        )
        self.geometry("1200x900")
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
    def __init__(self, parent):
        super().__init__(parent)
        self.book_choice = parent.book_choice
        self.chapter_choice = parent.chapter_choice
        self.parent = parent
        self.geometry("1200x950")
        self.title("Content Display")

        self.dot_size = 10
        self.spacing = 20
        self.row_spacing = 80

        self.canvas = tk.Canvas(self, width=1000, height=800, bg="white")
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

        label = tk.Label(self, text="go to page:", font=(24))
        label.pack()
        self.entry = tk.Entry(self, width=6)
        self.entry.pack()

        self.go_to_page_btn = ttk.Button(
            self,
            text="Confirm",
            command=self.go_to_page,
        )
        self.go_to_page_btn.pack()

    def go_to_page(self, merged_braille_input_wpages):
        target_page = int(self.entry.get())
        page_content = controller.go_to_page(target_page, merged_braille_input_wpages)
        if page_content:
            self.draw_braille(page_content)

    def draw_braille(self, braille_grid):
        self.canvas.delete("all")
        x_offset = 20
        y_offset = 20
        for row_idx, braille_row in enumerate(braille_grid):
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
        merged_braille_input_wpages = reader.load_input(book, chapter)
        page_content = controller.go_to_page(
            controller.page_index, merged_braille_input_wpages
        )
        if page_content:
            self.draw_braille(page_content)

    def next_page(self, merged_braille_input_wpages):
        page_content = controller.next_page(merged_braille_input_wpages)
        if page_content:
            self.draw_braille(page_content)

    def prev_page(self, merged_braille_input_wpages):
        page_content = controller.prev_page(merged_braille_input_wpages)
        if page_content:
            self.draw_braille(page_content)


if __name__ == "__main__":
    view = Menu()
    view.mainloop()
