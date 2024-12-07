import fitz  # PyMuPDF


def detect_table_headers(page):
    """
    Detect if a page contains table-like headers such as 'No.', 'PARAMETERS', etc.
    """
    words = page.get_text("words")
    headers = {"No.", "PARAMETERS", "COMPONENTS", "REQUIREMENTS"}
    detected_headers = set()

    for word in words:
        text = word[4]  # Extract the word text
        if text in headers:
            detected_headers.add(text)

    # If we detect all headers, consider this page as containing a table
    return detected_headers == headers


def extract_table_text_from_page(page):
    """
    Extract all words from a page and dynamically group them into rows.
    """
    words = page.get_text("words")
    if not words:
        return None

    # Sort words by their y-coordinates, then by x-coordinates for alignment
    words.sort(key=lambda w: (w[1], w[0]))

    # Group words into rows based on their y-coordinates
    rows = []
    current_row = []
    last_y = None
    row_threshold = 5  # Adjust for your PDF's row spacing

    for word in words:
        x0, y0, x1, y1, text = word[:5]
        if last_y is None or abs(y0 - last_y) < row_threshold:
            current_row.append((x0, text))  # Group words in the same row
        else:
            # Sort the current row by x-coordinates to maintain column order
            current_row.sort(key=lambda w: w[0])
            rows.append(" ".join(w[1] for w in current_row))  # Append as a single row of text
            current_row = [(x0, text)]  # Start a new row
        last_y = y0

    # Append the last row
    if current_row:
        current_row.sort(key=lambda w: w[0])
        rows.append(" ".join(w[1] for w in current_row))

    return "\n".join(rows)


def process_pdf_for_tables(pdf_path, output_file):
    """
    Process the PDF and extract tables by analyzing all text dynamically.
    """
    doc = fitz.open(pdf_path)
    with open(output_file, "w") as f:
        for page_num in range(len(doc)):
            page = doc[page_num]

            # Check if the page contains table headers
            if detect_table_headers(page):
                table_text = extract_table_text_from_page(page)
                if table_text:
                    f.write(f"Extracted Table from Page {page_num + 1}:\n")
                    f.write(table_text + "\n")
                    f.write("\n" + "-" * 50 + "\n")
            else:
                print(f"Skipping page {page_num + 1}: No tables detected.")


# Path to your PDF file
pdf_file = "ASEAN.pdf"  # Replace with your PDF path
output_file = "output_tables_detected.txt"  # File to save extracted tables

# Process the PDF
process_pdf_for_tables(pdf_file, output_file)
print(f"Extraction complete. Results saved to {output_file}.")
