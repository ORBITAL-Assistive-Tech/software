import tkinter as tk

class View:

    def __init__(self):
        root = tk.Tk()
    
        # Create a label widget
        label = tk.Label(root, text='Hello, Tkinter!')
        label.pack()
        
        # Start the GUI event loop
        root.mainloop()