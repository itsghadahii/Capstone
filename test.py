import streamlit as st
import pandas as pd
import io
import re
import PyPDF2
import docx2txt
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity

#2F195F – Primary Purple  
#4F29B7 – Highlight Purple  
#D6C2F0 – Accent Purple (borders)  
#FDF6FF – Card Background (categories)  
#E3D8FF – Box Background 
#F9F9F9 – Section Background  
#E0E0E0 – Light Border  
#000000 – Main Text  
#777777 – Secondary Text

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

# Main app layout
st.markdown('<h1 class="main-header">CV Course Matcher</h1>', unsafe_allow_html=True)

# File uploader
cv_file = st.file_uploader("Upload your CV to find matching courses", 
                           type=["pdf","txt"],
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