from PyPDF2 import PdfReader

class Reader:
    def reader(self, pdf_name):
        reader = PdfReader(f"{pdf_name}.pdf")
        page = reader.pages[0]
        text_to_use = page.extract_text()
        return text_to_use

