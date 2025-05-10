import fitz  # PyMuPDF
import pytesseract
from PIL import Image
import io
import os
import sqlite3
import datetime

# Configure pytesseract path if needed
# pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

def view_database(conn):
    """Display all records in the resume database."""
    cursor = conn.cursor()
    cursor.execute("SELECT id, file_name, file_path, processed_date FROM resumes")
    records = cursor.fetchall()

    if not records:
        print("No records found in the database.")
        return

    print(f"Found {len(records)} records:")
    print("-" * 80)
    for record in records:
        id, file_name, file_path, date = record
        print(f"ID: {id}")
        print(f"File: {file_name}")
        print(f"Path: {file_path}")
        print(f"Date: {date}")
        print("-" * 80)

    return records

def create_database():
    """Create SQLite database to store resume text and metadata."""
    conn = sqlite3.connect('resume_database.db')
    cursor = conn.cursor()

    # Create table for resume data
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS resumes (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        file_path TEXT UNIQUE,
        file_name TEXT,
        extracted_text TEXT,
        processed_date TIMESTAMP
    )
    ''')

    conn.commit()
    return conn

def extract_text_from_resume(pdf_path):
    """Extract text from a resume PDF using PyMuPDF and OCR if needed."""
    doc = fitz.open(pdf_path)
    text = ""

    for page_num in range(len(doc)):
        page = doc.load_page(page_num)

        # Try to get text directly first
        page_text = page.get_text()

        # If little or no text was extracted, try OCR
        if len(page_text.strip()) < 100:  # Arbitrary threshold
            # Get the page as an image
            pix = page.get_pixmap(matrix=fitz.Matrix(300/72, 300/72))  # 300 DPI
            img = Image.open(io.BytesIO(pix.tobytes("png")))

            # Use OCR to extract text from the image
            page_text = pytesseract.image_to_string(img)

        text += page_text + "\n\n"

    doc.close()
    return text

def store_resume_in_db(conn, file_path, extracted_text):
    """Store resume text and metadata in the database."""
    cursor = conn.cursor()
    file_name = os.path.basename(file_path)
    processed_date = datetime.datetime.now()

    try:
        cursor.execute(
            "INSERT OR REPLACE INTO resumes (file_path, file_name, extracted_text, processed_date) VALUES (?, ?, ?, ?)",
            (file_path, file_name, extracted_text, processed_date)
        )
        conn.commit()
        return True
    except Exception as e:
        print(f"Error storing in database: {e}")
        return False

def process_resumes_recursively(directory, conn):
    """Process all PDF files in a directory and its subdirectories and store in database."""
    results = []

    # Walk through all directories and subdirectories
    for root, dirs, files in os.walk(directory):
        for filename in files:
            if filename.lower().endswith('.pdf'):
                file_path = os.path.join(root, filename)
                print(f"Processing {file_path}...")

                try:
                    text = extract_text_from_resume(file_path)
                    success = store_resume_in_db(conn, file_path, text)
                    results.append((filename, success))
                except Exception as e:
                    print(f"Error processing {filename}: {e}")
                    results.append((filename, False))

    return results

def search_resume_database(conn, search_term):
    """Search for resumes containing the search term."""
    cursor = conn.cursor()
    cursor.execute(
        "SELECT file_name, file_path FROM resumes WHERE extracted_text LIKE ?",
        (f"%{search_term}%",)
    )
    return cursor.fetchall()

# Example usage
if __name__ == "__main__":
    # Create or connect to the database
    db_conn = create_database()

    # Process a directory of resumes recursively
    resume_dir = "/Users/mohammad/Downloads/resumes"
    results = process_resumes_recursively(resume_dir, db_conn)

    view_database(db_conn)

    # # Print processing results
    # for filename, success in results:
    #    status = "Success" if success else "Failed"
    #    print(f"{filename}: {status}")

    # # Example search
    # print("\nSearch results for 'Python':")
    # search_results = search_resume_database(db_conn, "Python")
    # for file_name, file_path in search_results:
    #    print(f"- {file_name} ({file_path})")

    # Close the database connection
    db_conn.close()