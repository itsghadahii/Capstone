# Masar 👩‍💻👨‍💻

## Overview

Masar is an intelligent career guidance system that utilizes artificial intelligence 
to help users find the most suitable training programs based on their current skills and interests. 
Masar aims to empower individuals by mapping their competencies to relevant learning opportunities offered by **Tuwaiq Academy**.

## Features

- **CV Analysis**: Upload and intelligent parsing of resume/CV documents
- **AI-Powered Skill Matching**: Automated extraction and analysis of user skills
- **Personalized Recommendations**: Tailored training program suggestions based on individual profiles
- **Training Path Creation**: Clear visualization of potential career development paths

## Technology Stack

**Web Application:**  
- **Streamlit** for building the interactive user interface.

**Data Storage and Search:**  
- **weaviate** as a vector database for semantic search and similarity matching.  

**Data Handling:**  
- **json**, **csv**, and **collections.OrderedDict** for structured data management.  

- **OCR CVs**:
**Tesseract** OCR (via pytesseract) is used to extract text from scanned PDF pages and images.
**PyMuPDF** (fitz) is used to read PDF files and render pages as images for OCR processing.

**Natural Language Processing:**  
- **sentence-transformers** and **langchain** for generating and handling text embeddings.  
- **openai** for AI-powered recommendations and analysis.
- also **spaCy**, **NLTK**
- **Backend & Processing**: Python mainly and several libraries

## Project Structure



```
Capstone/
│
├── docs/                   # Contains Masar presentation, poster and blind-link QR
├── Jsons/                  # Contains JSON files for data retrieval
├── images/                 # UI images and other static assets
├── pages/                  # Source code for different app pages
│
├── README.md               # Project documentation
├── home.py                 # Main application entry point
├── requirements.txt        # Python dependencies
└── webscraping_tuwaiq.py   # Script for scraping Tuwaiq Academy data
```
## Installation

```bash
# Clone the repository
git clone https://github.com/AI-bootcamp/capstone-project-batch3-masar

# Navigate to the project directory
cd masar

# Install dependencies
pip install -r requirements.txt  

# Start the app
streamlit run home.py
```

## Configuration

1. Create a `.env` file in the root directory
2. Configure the following variables:
   ```
   API_KEY=your_api_key
   DATABASE_URL=your_database_connection_string
   TUWAIQ_API_ENDPOINT=https://api.tuwaiq.edu.sa/programs
   ```

## Usage

1. Users register or log in to the system
2. Upload their CV/resume 
3. The system analyzes the document and extracts relevant skills and experience
4. Based on the analysis, Masar recommends suitable bootcamps and programs from Tuwaiq Academy
5. Users can view detailed information about each recommended program

## Future Enhancements

Include a feedback loop to improve AI recommendations.

Integrate with Tuwaiq Academy live API.

Expand to include job matching or internship suggestions.

## Poster
Link: https://n9.cl/tkqpq


## License

All right to Masar team

## Contact

https://bind.link/@masar

## Acknowledgments

- Tuwaiq Academy 

---
