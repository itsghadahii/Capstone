import streamlit as st
import fitz  # PyMuPDF
import pytesseract
from PIL import Image
import io
import os
import tempfile
import hashlib

# Configure pytesseract path if needed
# pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

@st.cache_data
def extract_text_from_resume(pdf_content):
    """
    Extract text from a resume PDF using PyMuPDF and OCR if needed.
    This function is cached to improve performance.
    """
    # Create a temporary file to work with
    with tempfile.NamedTemporaryFile(delete=False, suffix='.pdf') as tmp_file:
        tmp_file.write(pdf_content)
        pdf_path = tmp_file.name

    try:
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
    finally:
        # Clean up the temporary file
        os.unlink(pdf_path)

def main():
    # Set page configuration
    st.set_page_config(page_title="مسار", page_icon="🏫", layout="centered")

    # Custom CSS with animations and enhanced design
    st.markdown("""
    <style>
    .stApp {
    background-color: #f4f6f9;
    font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
    margin: 0;
    padding: 0;
    }

    /* Main Title */
    .main-title {
    text-align: center;
    color: #333;
    font-weight: bold;
    font-size: 2.5em;
    margin-bottom: 15px;
    animation: fadeIn 1.5s ease-in-out;
    }

    /* Subtitle */
    .subtitle {
    text-align: center;
    color: #777;
    font-size: 1.2em;
    margin-bottom: 25px;
    animation: fadeIn 2s ease-in-out;
    }

    /* Upload Box */
    .upload-box {
    border: 2px dashed #6a11cb;
    border-radius: 15px;
    padding: 40px;
    background-color: #fff;
    box-shadow: 0 4px 10px rgba(0, 0, 0, 0.1);
    text-align: center;
    transition: transform 0.3s ease;
    display: flex;
    justify-content: center;
    align-items: center;
    flex-direction: column;
    min-height: 200px;
    margin-bottom: 20px;
    }

    /* Hover effect for upload box */
    .upload-box:hover {
    transform: translateY(-10px);
    }

    /* File Uploader */
    .stFileUploader {
    display: block;
    width: 100%;
    border: 2px dashed #6a11cb;
    padding: 20px;
    border-radius: 10px;
    background-color: #f8f9fa;
    text-align: center;
    cursor: pointer;
    }

    /* Button Styling */
    .stButton>button {
    background-color: #6a11cb;
    color: white;
    width: 100%;
    padding: 12px;
    border-radius: 10px;
    font-size: 1.1em;
    transition: background-color 0.3s ease, transform 0.3s ease;
    cursor: pointer;
    }

    /* Hover effect for button */
    .stButton>button:hover {
    background-color: #5a0db3;
    transform: scale(1.05);
    }

    /* Logo */
    .tuwaiq-logo {
    position: top;
    top: 10px;
    right: 20px;
    width: 150px;
    animation: logoAnimation 2s ease-in-out;
    }

    /* Fade-in animation for elements */
    @keyframes fadeIn {
    0% {
    opacity: 0;
    }
    100% {
    opacity: 1;
    }
    }

    /* Animation for logo */
    @keyframes logoAnimation {
    0% {
    transform: translateY(-50px);
    opacity: 0;
    }
    100% {
    transform: translateY(0);
    opacity: 1;
    }
    }

    /* Text result box */
    .result-box {
    background-color: white;
    border-radius: 10px;
    padding: 20px;
    margin-top: 20px;
    box-shadow: 0 4px 10px rgba(0, 0, 0, 0.1);
    }

    /* Cache info */
    .cache-info {
    font-size: 0.8em;
    color: #888;
    text-align: center;
    margin-top: 10px;
    }
    </style>
    """, unsafe_allow_html=True)

    

    # Create a session state to store the extracted text
    if 'extracted_text' not in st.session_state:
        st.session_state.extracted_text = ""

    if 'cache_hit' not in st.session_state:
        st.session_state.cache_hit = False

    # File uploader
    uploaded_file = st.file_uploader("ارفع السيرة الذاتية هنا", type=['pdf'])

    # Process button
    if st.button('استخراج النص'):
        if uploaded_file is not None:
            with st.spinner('جاري معالجة الملف...'):
                # Get the file content
                pdf_content = uploaded_file.getvalue()

                # Check if this file has been processed before (for UI feedback only)
                file_hash = hashlib.md5(pdf_content).hexdigest()
                if 'last_processed_hash' in st.session_state and st.session_state.last_processed_hash == file_hash:
                    st.session_state.cache_hit = True
                else:
                    st.session_state.cache_hit = False
                    st.session_state.last_processed_hash = file_hash

                try:
                    # Extract text from the PDF using the cached function
                    extracted_text = extract_text_from_resume(pdf_content)
                    st.session_state.extracted_text = extracted_text

                    if st.session_state.cache_hit:
                        st.success('تم استخراج النص من الذاكرة المؤقتة!')
                    else:
                        st.success('تم استخراج النص بنجاح!')
                except Exception as e:
                    st.error(f'حدث خطأ أثناء معالجة الملف: {str(e)}')
        else:
            st.warning('يرجى رفع السيرة الذاتية أولاً')

    # Display the extracted text if available
    if st.session_state.extracted_text:
        st.markdown('<div class="result-box">', unsafe_allow_html=True)
        st.subheader("النص المستخرج:")
        st.text_area("", st.session_state.extracted_text, height=300)

        if st.session_state.cache_hit:
            st.markdown('<p class="cache-info">تم استرجاع النتائج من الذاكرة المؤقتة</p>', unsafe_allow_html=True)

        st.markdown('</div>', unsafe_allow_html=True)

        # Add a download button for the extracted text
        st.download_button(
            label="تحميل النص",
            data=st.session_state.extracted_text,
            file_name="extracted_text.txt",
            mime="text/plain"
        )

if __name__ == "__main__":
    main()