from view import Menu, Chapter, Content
from controller import Controller
from model import Reader
import warnings


def main():
    view = Menu()
    view.mainloop()

    reader = Reader()
    control = Controller(reader)


if __name__ == "__main__":
    main()
