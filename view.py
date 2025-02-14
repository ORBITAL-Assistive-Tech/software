import tkinter as tk
from controller import Controller
from model import Reader
import json

reader = Reader()

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

if braille_input:  # Ensure the input isn't empty
    merged_row = []
    for i, word_list in enumerate(braille_input):
        merged_row.extend(word_list)  # Add the word's Braille cells
        if i < len(braille_input) - 1:  # Don't add empty cell after the last word
            merged_row.append(empty_cell)
    merged_braille_input.append(merged_row)

# Flatten the list (assuming all cells are in the first sublist)
flat_list = merged_braille_input[0]

# === Create rows and pages from the flat list ===
total_cols = 15  # Each row has 15 Braille cells
rows_per_page = 10  # Each page displays 10 rows

# Split flat_list into rows (each row having 15 cells)
rows = [flat_list[i : i + total_cols] for i in range(0, len(flat_list), total_cols)]
# Pad any row that has fewer than 15 cells
for row in rows:
    while len(row) < total_cols:
        row.append(empty_cell)

# Group rows into pages (each page has 10 rows)
merged_braille_input_wpages = [
    rows[i : i + rows_per_page] for i in range(0, len(rows), rows_per_page)
]
# Pad any page that has fewer than 10 rows with rows of empty cells
for page in merged_braille_input_wpages:
    while len(page) < rows_per_page:
        page.append([empty_cell] * total_cols)

print("Total pages:", len(merged_braille_input_wpages))


# === GUI with page navigation ===


class View:
    def __init__(self):
        person_a = Reader()
        control = Controller(person_a)

        self.root = tk.Tk()
        self.root.title("Braille Reader")

        # Set a larger window size
        self.root.geometry("1200x900")

        # Track the current page index
        self.page_index = 0

        # Create Braille display canvas with larger dimensions
        self.dot_size = 10
        self.spacing = 20
        self.row_spacing = 80  # Increased row spacing between braille rows
        self.canvas = tk.Canvas(self.root, width=1000, height=800, bg="white")
        self.canvas.grid(row=0, column=0, columnspan=10)

        # Draw the initial page
        self.update_canvas()

        # Create Forward button to advance a page
        self.forward_btn = tk.Button(self.root, text="Forward", command=self.next_page)
        self.forward_btn.grid(row=1, column=4, pady=10)

        # Optional: Create Back button to go to the previous page
        self.back_btn = tk.Button(self.root, text="Back", command=self.prev_page)
        self.back_btn.grid(row=1, column=3, pady=10)

        # Start the GUI event loop
        self.root.mainloop()

    def draw_braille(self, braille_grid):
        """Draws the braille dots on the canvas for the provided grid (a page)."""
        self.canvas.delete("all")  # Clear previous page from canvas
        x_offset = 20
        y_offset = 20
        # Iterate through each row and cell of the page
        for row_idx, braille_row in enumerate(braille_grid):
            for char_idx, braille in enumerate(braille_row):
                for i, bit in enumerate(braille):
                    # Calculate position for each dot (2 columns x 3 rows per cell)
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
        """Updates the canvas to display the current page."""
        if self.page_index < len(merged_braille_input_wpages):
            self.draw_braille(merged_braille_input_wpages[self.page_index])
        else:
            print("No such page:", self.page_index)

    def next_page(self):
        """Advances to the next page, if available."""
        if self.page_index < len(merged_braille_input_wpages) - 1:
            self.page_index += 1
            self.update_canvas()
        else:
            print("Already at the last page.")

    def prev_page(self):
        """Goes back to the previous page, if available."""
        if self.page_index > 0:
            self.page_index -= 1
            self.update_canvas()
        else:
            print("Already at the first page.")


# Run the application
View()
