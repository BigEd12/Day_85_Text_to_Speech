from PyPDF2 import PdfReader

class Reader:
    def reader(self):
        reader = PdfReader("story.pdf")
        page = reader.pages[0]
        text_to_use = page.extract_text()
        return text_to_use

