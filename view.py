import tkinter as tk
from controller import Controller


class View:

    def __init__(self):

        root = tk.Tk()

        # Create a label widget
        btn = tk.Button(root, text="Click me !")

        btn.pack(side="top")

        # Start the GUI event loop
        root.mainloop()
