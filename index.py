import streamlit as st
import pandas as pd
import io
import re
import PyPDF2
import docx2txt
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity

# Set page config
st.set_page_config(
    page_title="مسار",
    page_icon="📚",
    layout="wide"
)

# Custom CSS for styling
st.markdown("""
<style>
    .main-header {
        font-size: 2.5rem;
        color: #1E88E5;
        text-align: center;
        margin-bottom: 2rem;
    }
    .section-header {
        font-size: 1.5rem;
        color: #1E88E5;
        margin-top: 1rem;
        margin-bottom: 0.5rem;
        padding-bottom: 0.5rem;
        border-bottom: 1px solid #e0e0e0;
    }
    .match-card {
        background-color: #f7f7f7;
        padding: 1rem;
        border-radius: 0.5rem;
        margin-bottom: 0.8rem;
        border-left: 4px solid #1E88E5;
    }
    .similar-card {
        background-color: #f7f7f7;
        padding: 1rem;
        border-radius: 0.5rem;
        margin-bottom: 0.8rem;
        border-left: 4px solid #43A047;
    }
    .other-card {
        background-color: #f7f7f7;
        padding: 1rem;
        border-radius: 0.5rem;
        margin-bottom: 0.8rem;
        border-left: 4px solid #FFA000;
    }
    .course-title {
        font-weight: bold;
        color: #333;
    }
    .match-percent {
        color: #1E88E5;
        font-weight: bold;
        float: right;
    }
    .similar-percent {
        color: #43A047;
        font-weight: bold;
        float: right;
    }
    .other-percent {
        color: #FFA000;
        font-weight: bold;
        float: right;
    }
    .stProgress > div > div > div > div {
        background-color: #1E88E5;
    }
</style>
""", unsafe_allow_html=True)

# Mock course data - in a real app, this would come from a database
courses = [
    {"id": 1, "title": "Advanced Python Programming", "description": "Master Python with advanced concepts and techniques", 
     "keywords": "python programming coding data structures algorithms object-oriented"},
    {"id": 2, "title": "Data Science Fundamentals", "description": "Introduction to data science with Python", 
     "keywords": "python data science pandas numpy matplotlib machine learning statistics"},
    {"id": 3, "title": "Web Development with Flask", "description": "Build web applications with Python Flask", 
     "keywords": "python web development flask html css javascript api rest"},
    {"id": 4, "title": "Machine Learning Engineering", "description": "Deep dive into ML models and deployment", 
     "keywords": "machine learning artificial intelligence deep learning neural networks tensorflow scikit-learn"},
    {"id": 5, "title": "Cloud Computing with AWS", "description": "Deploy applications on AWS cloud", 
     "keywords": "cloud aws amazon ec2 s3 lambda serverless devops"},
    {"id": 6, "title": "Front-end Development", "description": "Create modern user interfaces with React", 
     "keywords": "javascript react frontend user interface ui components html css"},
    {"id": 7, "title": "Database Management Systems", "description": "Learn SQL and NoSQL database systems", 
     "keywords": "database sql postgresql mysql mongodb nosql query data modeling"},
    {"id": 8, "title": "DevOps and CI/CD", "description": "Implement continuous integration and deployment", 
     "keywords": "devops docker kubernetes jenkins git github gitlab ci cd continuous integration deployment"},
    {"id": 9, "title": "Big Data Processing", "description": "Process large datasets with Spark", 
     "keywords": "big data hadoop spark scala distributed computing mapreduce"},
    {"id": 10, "title": "Mobile App Development", "description": "Build mobile apps for iOS and Android", 
     "keywords": "mobile android ios swift kotlin react native flutter app development"}
]

def extract_text_from_pdf(pdf_file):
    """Extract text from PDF file"""
    pdf_reader = PyPDF2.PdfReader(pdf_file)
    text = ""
    for page in pdf_reader.pages:
        text += page.extract_text()
    return text

def extract_text_from_docx(docx_file):
    """Extract text from DOCX file"""
    text = docx2txt.process(docx_file)
    return text

def extract_text_from_txt(txt_file):
    """Extract text from TXT file"""
    return txt_file.getvalue().decode("utf-8")

def extract_text_from_cv(cv_file):
    """Extract text from CV file (PDF, DOCX, TXT)"""
    file_extension = cv_file.name.split('.')[-1].lower()
    
    if file_extension == "pdf":
        return extract_text_from_pdf(cv_file)
    elif file_extension == "docx":
        return extract_text_from_docx(cv_file)
    elif file_extension == "txt":
        return extract_text_from_txt(cv_file)
    else:
        st.error("Unsupported file format. Please upload a PDF, DOCX, or TXT file.")
        return None

def match_cv_to_courses(cv_text, courses):
    """Match CV text to courses using cosine similarity"""
    # Create a list of all documents (CV and course descriptions)
    documents = [cv_text] + [f"{course['title']} {course['description']} {course['keywords']}" for course in courses]
    
    # Create the CountVectorizer
    vectorizer = CountVectorizer().fit_transform(documents)
    
    # Calculate cosine similarity between CV and each course
    cosine_similarities = cosine_similarity(vectorizer[0:1], vectorizer[1:]).flatten()
    
    # Add similarity scores to courses
    for i, course in enumerate(courses):
        course['match_score'] = round(cosine_similarities[i] * 100, 1)
    
    # Sort courses by match score in descending order
    sorted_courses = sorted(courses, key=lambda x: x['match_score'], reverse=True)
    
    return sorted_courses

def display_course_card(course, match_type="match"):
    """Display a course card with appropriate styling"""
    if match_type == "match":
        st.markdown(f"""
        <div class="match-card">
            <span class="course-title">{course['title']}</span>
            <span class="match-percent">{course['match_score']}% match</span>
            <p>{course['description']}</p>
        </div>
        """, unsafe_allow_html=True)
    elif match_type == "similar":
        st.markdown(f"""
        <div class="similar-card">
            <span class="course-title">{course['title']}</span>
            <span class="similar-percent">{course['match_score']}% match</span>
            <p>{course['description']}</p>
        </div>
        """, unsafe_allow_html=True)
    else:
        st.markdown(f"""
        <div class="other-card">
            <span class="course-title">{course['title']}</span>
            <span class="other-percent">{course['match_score']}% match</span>
            <p>{course['description']}</p>
        </div>
        """, unsafe_allow_html=True)

# Main app layout
st.markdown('<h1 class="main-header">CV Course Matcher</h1>', unsafe_allow_html=True)

# File uploader
cv_file = st.file_uploader("Upload your CV to find matching courses", 
                           type=["pdf", "docx", "txt"],
                           help="Upload your CV in PDF, DOCX, or TXT format")

if cv_file is not None:
    with st.spinner("Analyzing your CV..."):
        # Extract text from CV
        cv_text = extract_text_from_cv(cv_file)
        
        if cv_text:
            # Match CV to courses
            matched_courses = match_cv_to_courses(cv_text, courses.copy())
            
            # Display results
            st.success("Analysis complete! Here are your course recommendations:")
            
            # Create columns for layout
            col1, col2 = st.columns([3, 1])
            
            with col1:
                # Perfect matches (90% and above)
                perfect_matches = [c for c in matched_courses if c['match_score'] >= 90]
                if perfect_matches:
                    st.markdown('<h2 class="section-header">Perfect Matches for Your Skills</h2>', unsafe_allow_html=True)
                    for course in perfect_matches:
                        display_course_card(course, "match")
                
                # Similar matches (70% to 89%)
                similar_matches = [c for c in matched_courses if 70 <= c['match_score'] < 90]
                if similar_matches:
                    st.markdown('<h2 class="section-header">Similar to Your Skills</h2>', unsafe_allow_html=True)
                    for course in similar_matches:
                        display_course_card(course, "similar")
                
                # Other recommendations (below 70%)
                other_matches = [c for c in matched_courses if c['match_score'] < 70]
                if other_matches:
                    st.markdown('<h2 class="section-header">Other Recommendations</h2>', unsafe_allow_html=True)
                    for course in other_matches[:5]:  # Show only top 5 other recommendations
                        display_course_card(course, "other")
            
            with col2:
                st.markdown('<h3 style="margin-top: 3.7rem;">Skills Detected</h3>', unsafe_allow_html=True)
                
                # Extract skills from CV (simplified approach)
                common_skills = ["python", "javascript", "java", "c++", "sql", "mongodb", "react", 
                                "angular", "vue", "node.js", "html", "css", "aws", "azure", 
                                "docker", "kubernetes", "machine learning", "data science", 
                                "tensorflow", "pytorch", "nlp", "statistics", "git", "agile"]
                
                detected_skills = []
                for skill in common_skills:
                    if re.search(r'\b' + re.escape(skill) + r'\b', cv_text.lower()):
                        detected_skills.append(skill)
                
                if detected_skills:
                    for skill in detected_skills:
                        st.markdown(f"- **{skill.title()}**")
                else:
                    st.write("No specific skills detected. Try uploading a more detailed CV.")

else:
    # Instructions when no file is uploaded
    st.info("Please upload your CV to get personalized course recommendations.")
    
    # Placeholder images and sample results
    st.markdown('<h3 style="margin-top: 2rem;">How it works:</h3>', unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("""
        ### 1. Upload CV
        Upload your resume in PDF, DOCX, or TXT format to begin the analysis.
        """)
    
    with col2:
        st.markdown("""
        ### 2. AI Analysis
        Our system will analyze your skills, experience, and qualifications.
        """)
    
    with col3:
        st.markdown("""
        ### 3. Get Matches
        Receive personalized course recommendations based on your profile.
        """)

# Footer
st.markdown("""
---
<p style="text-align: center;">CV Course Matcher | Find the perfect courses for your career growth</p>
""", unsafe_allow_html=True)