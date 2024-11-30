from docx import Document
class DocxParser:
    def parse(self, file_path):
        doc = Document(file_path)
        text = "\n".join([para.text for para in doc.paragraphs])
        return text