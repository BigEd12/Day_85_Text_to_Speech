from PyPDF2 import PdfReader

reader = PdfReader("story.pdf")
page = reader.pages[0]
story_text = page.extract_text()