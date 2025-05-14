# مسار (Masar)

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
- **sqlite3** for local database storage of resumes and user data.

**Data Handling:**  
- **json**, **csv**, and **collections.OrderedDict** for structured data management.  
- **requests** and **aiohttp** for web scraping and HTTP requests.

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
masar/
│
├── backend/                # Backend logic, APIs, and machine learning models
│   ├── app.py              # Main backend application entry point
│   └── models/             # Pre-trained models and related code
│
├── frontend/               # Frontend application (Streamlit or web UI)
│   ├── public/             # Static assets (images, icons, etc.)
│   ├── src/                # Source code for frontend logic and UI
│   └── components/         # Reusable UI components
│
├── data/                   # Datasets and program information
│   └── tuwaiq_programs.json # Tuwaiq Academy programs data
│
├── README.md               # Project documentation
└── requirements.txt        # Python dependencies
```
## Installation

```bash
# Clone the repository
git clone https://github.com/AI-bootcamp/capstone-project-batch3-masar

# Navigate to the project directory
cd masar

# Install dependencies
npm install 

# Configure environment variables
cp .env

# Start the development server
npm run dev 
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
