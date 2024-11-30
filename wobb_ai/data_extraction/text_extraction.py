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