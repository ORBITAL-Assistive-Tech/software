import tkinter as tk
from tkinter import ttk
from controller import Controller
from model import Reader
import json

reader = Reader()
controller = Controller(reader)

# Load books
book1 = reader.load_braille_file("documents/book1.txt")
book2 = reader.load_braille_file("documents/book2.txt")
reader.add_document(book1)
reader.add_document(book2)

# Load the braille in the book we want to display
braille_input = reader.get_document(book2.file_path)

# Merge words into a single list with an empty cell between them
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


class Menu(tk.Tk):
    def __init__(self):
        super().__init__()
        self.geometry("1200x900")
        self.title("Braille Reader Menu")
        ttk.Button(self, text="Book 1", command=self.open_chapter).pack(expand=True)

    def open_chapter(self):
        self.chapter = Chapter(self)


class Chapter(tk.Toplevel):
    def __init__(self, parent):
        super().__init__(parent)
        self.parent = parent
        self.geometry("1200x900")
        self.title("Braille Reader")
        ttk.Button(self, text="Chapter 1", command=self.open_window).pack(expand=True)
        ttk.Button(self, text="Back to Main Menu", command=self.return_to_main).pack(
            pady=10
        )

    def open_window(self):
        Content(self).grab_set()

    def return_to_main(self):
        self.destroy()
        self.parent.deiconify()


class Content(tk.Toplevel):
    def __init__(self, parent):
        super().__init__(parent)
        self.geometry("1200x950")
        self.title("Content Display")

        self.dot_size = 10
        self.spacing = 20
        self.row_spacing = 80

        self.canvas = tk.Canvas(self, width=1000, height=800, bg="white")
        self.canvas.pack(pady=10)

        self.update_canvas()

        self.forward_btn = tk.Button(self, text="Forward", command=self.next_page)
        self.forward_btn.pack(side="right", padx=10)

        self.back_btn = tk.Button(self, text="Back", command=self.prev_page)
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

    def go_to_page(self):
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

    def update_canvas(self):
        page_content = controller.go_to_page(
            controller.page_index, merged_braille_input_wpages
        )
        if page_content:
            self.draw_braille(page_content)

    def next_page(self):
        page_content = controller.next_page(merged_braille_input_wpages)
        if page_content:
            self.draw_braille(page_content)

    def prev_page(self):
        page_content = controller.prev_page(merged_braille_input_wpages)
        if page_content:
            self.draw_braille(page_content)


if __name__ == "__main__":
    view = Menu()
    view.mainloop()
