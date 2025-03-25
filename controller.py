class Controller:
    """
    This class is controls the interaction between the model and view
    """

    def __init__(self, reader):
        self.reader = reader

    def docx_to_text(docx_path, txt_path):
        try:
            text = docx2txt.process(docx_path)
            with open(txt_path, 'w', encoding='utf-8') as text_file:
            text_file.write(text)
            print(f"Successfully converted '{docx_path}' to '{txt_path}'")
        except Exception as e:
            print(f"An error occurred: {e}")

    def text_to_braille(self, text):
        pass

    def upload_text_file(self, path):
        with open(path, "r") as f:
            text = "".join(f.readlines())
            braille = brl.translate(text)
            braille_file = BrailleFile(text, braille, path)
            self.reader.add_document(braille_file)
            self.save_braille_file(text, braille)

    def load_braille_file(self, path_to_braille_file):
        with open(path_to_braille_file, "r+") as f:
            data = json.load(f)
            braille_file = BrailleFile(
                data["text"], data["braille"], path_to_braille_file
            )
            self.reader.add_document(braille_file)

    def save_braille_file(self, text, braille):
        data = {"text": text, "braille": braille}
        with open("documents/test.txt", "w") as f:
            json.dump(data, f, ensure_ascii=False)
