class Braille_file:

    def __init__(self, text, braille, file_path):
        self.file_path = file_path
        self.text = text
        self.braille = braille
        self.id = 0
        pass

    def get_braille(self):
        return self.braille

    def get_text(self):
        return self.text


class Reader:

    def __init__(self, documents=None):
        self.documents = []

    def add_document(self, document: Braille_file):
        self.documents.append(document)

    def remove_document(self, document: Braille_file):
        pass

    def get_document(self):
        pass

    def get_all_documents(self):
        return self.documents
