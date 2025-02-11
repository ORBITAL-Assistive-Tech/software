from PyPDF2 import PdfReader


class Controller:

    def __init__(self, person):
        self.person = person
        pass

    def print_hello_world(self):
        self.person.change_name()
        print(self.person.get_name())

    # PDF to Text reader
    reader = PdfReader("example.pdf")
    page = reader.pages[0]
    print(page.extract_text())
