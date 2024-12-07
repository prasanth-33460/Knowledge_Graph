import fitz  # PyMuPDF


def detect_table_bbox(page):
    """
    Detect the bounding box of a table on the page by locating headers like 'No.', 'PARAMETERS', etc.
    """
    words = page.get_text("words")  # Extract words with their bounding boxes
    headers = {"No.", "PARAMETERS", "COMPONENTS", "REQUIREMENTS"}
    table_bbox = None

    for word in words:
        text = word[4]  # Extract the word text
        if text in headers:
            # Initialize or expand the bounding box to include the header
            if table_bbox is None:
                table_bbox = [word[0], word[1], word[2], word[3]]  # x0, y0, x1, y1
            else:
                table_bbox[0] = min(table_bbox[0], word[0])  # Update x0
                table_bbox[1] = min(table_bbox[1], word[1])  # Update y0
                table_bbox[2] = max(table_bbox[2], word[2])  # Update x1
                table_bbox[3] = max(table_bbox[3], word[3])  # Update y1

    # Expand the bounding box vertically to include rows below the headers
    if table_bbox:
        table_bbox[3] += 500  # Adjust this value based on expected table row heights
    return table_bbox


def extract_table_text_from_bbox(page, bbox):
    """
    Extract text within a specific bounding box on the page.
    """
    if bbox is None:
        return None
    text = page.get_text("text", clip=fitz.Rect(*bbox))
    return text.strip()


def process_pdf_for_tables(pdf_path, output_file):
    """
    Process the PDF to extract tables and save their content to a file.
    """
    doc = fitz.open(pdf_path)
    with open(output_file, "w") as f:
        for page_num in range(len(doc)):
            page = doc[page_num]

            # Detect table bounding box
            table_bbox = detect_table_bbox(page)
            if table_bbox:
                table_text = extract_table_text_from_bbox(page, table_bbox)
                if table_text:
                    f.write(f"Extracted Table from Page {page_num + 1}:\n")
                    f.write(table_text + "\n")
                    f.write("\n" + "-" * 50 + "\n")
                else:
                    f.write(f"No table content found in detected area on Page {page_num + 1}.\n")
            else:
                f.write(f"No table detected on Page {page_num + 1}.\n")


# Path to your PDF file
pdf_file = "ASEAN.pdf"  # Replace with your PDF path
output_file = "output_tables_bounded.txt"  # File to save extracted tables

# Process the PDF
process_pdf_for_tables(pdf_file, output_file)
print(f"Extraction complete. Results saved to {output_file}.")
