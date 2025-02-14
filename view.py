import tkinter as tk
from controller import Controller
from model import Reader
import json

with open("documents/book1.txt", "r") as f:
    data = json.load(f)

braille_input = data.get("braille")


class View:

    def __init__(self):

        person_a = Reader()
        control = Controller(person_a)

        root = tk.Tk()

        # Ensure 10x15 grid by filling empty spaces with "000000"
        total_rows = 15
        total_cols = 10
        empty_cell = "000000"

        while len(braille_input) < total_rows:
            braille_input.append([empty_cell] * total_cols)
        for row in braille_input:
            while len(row) < total_cols:
                row.append(empty_cell)

        # Create Braille display
        dot_size = 10
        spacing = 20
        row_spacing = 80  # Increased row spacing
        canvas = tk.Canvas(root, width=500, height=600, bg="white")
        canvas.grid(row=0, column=0, columnspan=10)

        def draw_braille(canvas, braille_grid):
            x_offset = 20
            y_offset = 20
            for row_idx, braille_row in enumerate(braille_grid):
                for char_idx, braille in enumerate(braille_row):
                    for i, bit in enumerate(braille):
                        col = i % 2
                        row = i // 2
                        x = x_offset + col * spacing + char_idx * 50
                        y = y_offset + row * spacing + row_idx * row_spacing
                        if bit == "1":
                            canvas.create_oval(
                                x, y, x + dot_size, y + dot_size, fill="black"
                            )
                        else:
                            canvas.create_oval(
                                x, y, x + dot_size, y + dot_size, outline="black"
                            )

        draw_braille(canvas, braille_input)

        # Create button
        # btn = tk.Button(root, text="Backward", command=control.print_hello_world)
        # btn.grid(row=n_rows + 1, column=n_columns // 2 - 1)

        # btn = tk.Button(root, text="Forward", command=control.print_hello_world)
        # btn.grid(row=n_rows + 1, column=n_columns // 2)

        # btn = tk.Button(root, text="On/off", command=control.print_hello_world)
        # btn.grid(row=n_rows + 2, column=n_columns - 1)

        # btn = tk.Button(root, text="Menu", command=control.print_hello_world)
        # btn.grid(row=n_rows + 2, column=0)

        # Start the GUI event loop
        root.mainloop()
