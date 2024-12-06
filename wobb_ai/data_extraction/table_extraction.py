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
                        x0 = min(x0, word['x0'])
                        y0 = min(y0, word['top'])
                        x1 = max(x1, word['x1'])
                        y1 = max(y1, word['bottom'])

    # Expand the bounding box further to ensure it captures the entire table
    x0 -= 30  # Expand more on the left side
    y0 -= 30  # Expand more on the top side
    x1 += 30  # Expand more on the right side
    y1 += 30  # Expand more on the bottom side

    # Return the expanded bounding box as [x0, y0, x1, y1]
    return [x0, y0, x1, y1]

# Function to process the PDF and extract valid tables
def process_pdf(pdf_path, output_file):
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
                    
                    # Get the expanded bounding box of the table
                    bbox = get_table_bbox(page, cleaned_table)

                    # Print the bounding box for debugging purposes
                    print(f"Bounding Box for Table on Page {page_num + 1}: {bbox}")

                    # Extract the contents of the table using PyMuPDF for detailed text
                    extracted_text = extract_table_text_using_pymupdf(pdf_path, page_num, bbox)

                    # Store extracted table data with content
                    all_tables.append((page_num, table, extracted_text))

                    # Write output to text file
                    with open(output_file, "a") as f:
                        f.write(f"\nExtracted Table from Page {page_num + 1}:\n")
                        for row in table:
                            f.write(f"{row}\n")
                        
                        f.write("\nExtracted Table Text from Page:\n")
                        f.write(f"{extracted_text}\n")
                        f.write("\n" + "-"*50 + "\n")

    return all_tables

# Path to your PDF file
pdf_file = "ASEAN.pdf"  # Update this with your actual PDF path
output_file = "output_tables.txt"  # File to store the output

# Call the function to process the PDF and store output in the text file
valid_tables = process_pdf(pdf_file, output_file)

# Confirm that the output has been written to the file
print(f"Extraction complete. Data written to {output_file}.")
