import pdfplumber
import fitz  # PyMuPDF

# Function to extract text within the bounding box using PyMuPDF (fitz)
def extract_table_text_using_pymupdf(pdf_path, page_num, bbox):
    doc = fitz.open(pdf_path)
    page = doc.load_page(page_num)  # page_num is zero-indexed
    # Extract text within the bounding box (bbox format: [x0, y0, x1, y1])
    text = page.get_text("text", clip=bbox)
    return text

# Function to calculate the bounding box of a table based on word positions
def get_table_bbox(page, table):
    # Extract words on the page with their bounding boxes
    words = page.extract_words()
    
    # Initialize the bounding box values
    x0, y0, x1, y1 = float('inf'), float('inf'), float('-inf'), float('-inf')
    
    # Iterate through the table to find the positions of the words (table cells)
    for row in table:
        for cell in row:
            if cell:  # Only process non-None cells
                # Find the position of the word (matching the cell content)
                for word in words:
                    if word['text'] == cell:  # Match the cell text with the word text
                        # Update the bounding box
                        x0 = min(x0, word['doctop'])
                        y0 = min(y0, word['bottom'])
                        x1 = max(x1, word['doctop'])
                        y1 = max(y1, word['top'])
    
    # Return the bounding box as [x0, y0, x1, y1]
    return [x0, y0, x1, y1]

# Function to process the PDF and extract valid tables
def process_pdf(pdf_path):
    all_tables = []
    
    with pdfplumber.open(pdf_path) as pdf:
        for page_num in range(len(pdf.pages)):  # Loop through all pages
            page = pdf.pages[page_num]
            
            # Extract tables on the current page
            tables = page.extract_tables()
            print(f"Extracted tables from page {page_num + 1}:")  # Debug print
            
            if tables:
                for table in tables:
                    # Print out every row of the table, including None values, and keep all rows
                    print(f"Raw Table from page {page_num + 1}:")
                    for row in table:
                        print(row)  # Print the raw table data (including rows with None values)
                    
                    # Clean up table by removing empty rows but process all rows
                    # Skip nothing, print all rows
                    cleaned_table = [row for row in table if row]  # Remove completely empty rows
                    
                    # Get the bounding box of the table
                    bbox = get_table_bbox(page, cleaned_table)
                    
                    # Extract the contents of the table using PyMuPDF for detailed text
                    extracted_text = extract_table_text_using_pymupdf(pdf_path, page_num, bbox)
                    
                    # Store extracted table data with content
                    all_tables.append((page_num, table, extracted_text))
    
    return all_tables

# Path to your PDF file
pdf_file = "ASEAN.pdf"  # Update this with your actual PDF path

# Call the function to process the PDF
valid_tables = process_pdf(pdf_file)

# Output the result
if valid_tables:
    for page_num, table, page_text in valid_tables:
        print(f"\nExtracted Table from Page {page_num + 1}:")
        for row in table:
            print(row)
        print("\nExtracted Table Text from Page:")
        print(page_text)
        print("\n" + "-"*50)
else:
    print("No valid tables found.")
