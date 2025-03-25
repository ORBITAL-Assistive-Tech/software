import docx2txt


class Controller:

    def __init__(self):
        pass

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
