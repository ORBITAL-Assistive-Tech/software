import tkinter as tk
from controller import Controller
from model import Person


class View:

    def __init__(self):

        person_a = Person()
        control = Controller(person_a)

        root = tk.Tk()

        # Create braille cells
        n_rows = 4
        n_columns = 6

        for i in range(n_rows):
            for j in range(n_columns):
                label = tk.Label(
                root,
                text=f"braille({i},{j})",  # Label text to show its position
                foreground="black",
                background="white",
                width=10,  # Adjust width for spacing
                height=2  # Adjust height for spacing
                )
                label.grid(row=i, column=j, padx=5, pady=5)

        # Create button
        btn = tk.Button(root, text="Backward", command=control.print_hello_world)
        btn.grid(row=n_rows + 1, column=n_columns//2 - 1)

        btn = tk.Button(root, text="Forward", command=control.print_hello_world)
        btn.grid(row=n_rows + 1, column=n_columns//2)

        btn = tk.Button(root, text="On/off", command=control.print_hello_world)
        btn.grid(row=n_rows + 2, column=n_columns-1)

        btn = tk.Button(root, text="Menu", command=control.print_hello_world)
        btn.grid(row=n_rows + 2, column=0)

        # Start the GUI event loop
        root.mainloop()
