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

**Frontend & UI**: Streamlit
- **Backend & Processing**: Python
- **NLP Libraries**: spaCy, NLTK 
- **Web Scraping**: `BeautifulSoup`, `Requests`
- **Data Storage**: JSON / SQLite 

## Project Structure

masar/
│
├── backend/
│ ├── app.py
│ └── models/
│
├── frontend/
│ ├── public/
│ ├── src/
│ └── components/
│
├── data/
│ └── tuwaiq_programs.json
│
├── README.md
└── requirements.txt

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

## License

All right to Masar team

## Contact

https://bind.link/@masar

## Acknowledgments

- Tuwaiq Academy 

---
