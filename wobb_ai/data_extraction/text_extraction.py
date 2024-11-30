import os
import pandas as pd 
import json
import csv
import PyPDF2
import pytesseract
from PIL import Image
from pdfminer.high_level import extract_text
import pdfplumber 
import docx
from bs4 import BeautifulSoup

class DocumentExtractor:
    def __init__(self):
        pass
    
    def extract_text_from_pdf(self, file_path):
        try:
            with pdfplumber.open(file_path) as pdf:
                text = ' '
                for page in pdf.pages:
                    text += page.extract_text()
            return text if text else self.extract_text_from_pdf_alter(file_path)
        except Exception as e:
            print(f"Error trying to extract from PDf(using pdfplumber): {e}")
            return self.extract_text_from_pdf_alter(file_path)
        
    def extract_text_from_pdf_alter(self, file_path):
        try:
            with open(file_path, 'rb') as pdf_file:
                reader = PyPDF2.PdfReader(pdf_file)
                text = ' '
                for page in reader.pages:
                    text += page.extract_text()
            return text
        except Exception as e:
            return f"Error trying to extract from PDF(using PyPDF2): {e}"
        
    
    def extract_text_from_docx(self, file_path):
        try:
            doc = docx.Document(file_path)
            text = '\n'.join([para.text for para in doc.paragraphs])
            return text
        except Exception as e:
            return f"Error extracting the docx file: {e}"
        
    def extract_text_from_csv(self, file_path):
        try:
            df = pd.read_csv(file_path)
            text = df.to_string(index=False)
            return text
        except Exception as e:
            return f"Error trying to extract from CSV: {e}"
        
    def extract_text_from_html(self, file_path):
        try:
            with open(file_path, 'r', encoding='UTF-8') as html:
                soup = BeautifulSoup(html, 'html.parser')
                text = soup.get_text()
            return text
        except Exception as e:
            return f"Error trying to extract from HTML: {e}"
        
    def extract_text_from_image(self, file_path):
        try:
            img = Image.open(file_path)
            text = pytesseract.image_to_string(img)
            return text
        except Exception as e:
            return f"Error trying to extract from IMAGE: {e}"
        
    def extract_text_from_json(self, file_path):
        try:
            with open(file_path, 'r', encoding='utf-8',)as json:
                data = json.load(json)
            text = self.json_to_text(data)
        except Exception as e:
            return f"Error extracting from Json: {e}"
        
    def json_to_text(self, data, og_key=''):
        text = ''
        if isinstance(data,dict):
            for key,value in data.items():
                new = f"{og_key}{key}_" if og_key else key
                text+=self.json_to_text(value,new)
        elif isinstance(data, list):
            for item in data:
                text+=self.json_to_text(item, og_key)
        else:
            text+=f"{og_key}:{str(data)}\n"
            return text
        
    def choose_from_file(self,  file_path):
        ext = os.path.splitext(file_path)
        if ext.lower() in ['.pdf']:
            return self.extract_text_from_pdf(file_path)
        elif ext.lower() in ['.docx']:
            return self.extract_text_from_docx(file_path)
        elif ext.lower() in ['.csv']:
            return self.extract_text_from_csv(file_path)
        elif ext.lower() in ['.html', '.htm']:
            return self.extract_text_from_html(file_path)
        elif ext.lower() in ['.jpg', '.jpeg', '.png']:
            return self.extract_text_from_image(file_path)
        elif ext.lower() in ['.json']:
            return self.extract_text_from_json(file_path)
        else:
            return f"Unsupported file format: {ext}"