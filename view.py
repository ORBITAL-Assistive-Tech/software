import tkinter as tk
from controller import Controller
from model import Person


class View:

    def __init__(self):

        person_a = Person()
        control = Controller(person_a)

        root = tk.Tk()

        # Create a label widget
        btn = tk.Button(root, text="Click me !", command=control.print_hello_world)

        btn.pack(side="top")

        # Start the GUI event loop
        root.mainloop()
