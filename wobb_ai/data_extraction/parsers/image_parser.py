import pytesseract
from PIL import Image
class ImageParser:
    def parse(self, file_path):
        image = Image.open(file_path)
        return pytesseract.image_to_string(image)