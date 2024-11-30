from text_extraction import DocumentExtractor

class DocumentProcessor:
    def __init__(self):
        self.extractor = DocumentExtractor()
        
    def process_document(self, file_path):
        try:
            text = self.extractor.extract_text_from_file(file_path)
            print(f"Text extracted successfully from {file_path}")
            return text
        except Exception as e:
            return f"Error extracting text from {file_path}: {e}"
        
    def extract_from_multiple_documents(self, file_paths):
        texts = []
        for file_path in file_paths:
            text = self.process_document(file_path)
            if text:
                texts.append(text)
        return texts
    
    def save_processed_text(self, file_path, output_file):
        try:
            text = self.process_document(file_path)
            if text:
                with open(output_file, 'w') as f:
                    f.write(text)
                print(f"Text saved to {output_file}")
        except Exception as e:
            print(f"Error saving text to {output_file}: {e}")