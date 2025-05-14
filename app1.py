import streamlit as st

# Add support for loading local image files
import os
from PIL import Image
import base64

# Function to get image as base64 for embedding
def get_image_as_base64(image_path):
    if os.path.exists(image_path):
        with open(image_path, "rb") as img_file:
            return base64.b64encode(img_file.read()).decode('utf-8')
    else:
        # Return empty string if file not found
        st.warning(f"Image file {image_path} not found. Please place the logo file in the same directory as this script.")
        return ""

# Try to get the logo image
logo_path = "tw.jpg"  # Path to the logo file
logo_base64 = get_image_as_base64(logo_path)
st.set_page_config(
    page_title="أكاديمية طويق",
    page_icon="🧠",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Arabic RTL CSS
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Tajawal:wght@400;700&display=swap');
    
    * {
        font-family: 'Tajawal', sans-serif !important;
    }
    
    .rtl {
        direction: rtl;
        text-align: right;
    }
    
    .css-18e3th9 {
        padding-top: 0;
    }
    
    .st-emotion-cache-16txtl3 h1 {
        font-weight: 700;
        text-align: right;
    }
    
    .header-container {
        display: flex;
        justify-content: space-between;
        align-items: center;
        margin-bottom: 20px;
    }
    
    .logo {
        max-height: 60px;
    }
    
    .profile-container {
        display: flex;
        align-items: center;
        gap: 10px;
        background-color: #f8f9fa;
        padding: 5px 10px;
        border-radius: 10px;
    }
    
    .profile-image {
        width: 40px;
        height: 40px;
        border-radius: 50%;
    }
    
    /* Right sidebar menu - the most important part */
    .menu-container {
        position: fixed;
        right: 0;
        top: 0;
        height: 100vh;
        background-color: white;
        box-shadow: -2px 0 5px rgba(0,0,0,0.1);
        padding: 20px;
        z-index: 1000;
        width: 230px;
        overflow-y: auto;
        direction: rtl;
    }
    
    .menu-item {
        display: flex;
        align-items: center;
        justify-content: flex-start;
        gap: 10px;
        padding: 10px;
        border-radius: 5px;
        margin-bottom: 5px;
        cursor: pointer;
        text-decoration: none;
        color: inherit;
    }
    
    .menu-item:hover {
        background-color: #f8f9fa;
    }
    
    .menu-item.active {
        background-color: #6c5ce7;
        color: white;
    }
    
    .menu-icon {
        width: 20px;
        height: 20px;
    }
    
    .menu-divider {
        font-size: 0.8em;
        color: #666;
        text-align: center;
        margin: 15px 0 5px;
    }
    
    .content-container {
        margin-right: 250px;
        padding: 20px;
    }
    
    /* Dummy placeholder content */
    .placeholder-box {
        background-color: #f8f9fa;
        border-radius: 10px;
        padding: 40px;
        margin-bottom: 20px;
        text-align: center;
        color: #aaa;
    }
    
    @media (max-width: 768px) {
        .content-container {
            margin-right: 0;
        }
        
        .menu-container {
            display: none;
        }
    }
</style>
""", unsafe_allow_html=True)

# Create HTML for logo image
if logo_base64:
    logo_html = f'<img src="data:image/jpeg;base64,{logo_base64}" style="max-width: 120px;" alt="Tuwaiq Academy Logo">'
else:
    # Fallback to a placeholder if image not found
    logo_html = '<div style="width: 120px; height: 40px; background-color: #f1f1f1; display: flex; align-items: center; justify-content: center;">LOGO</div>'

# Content container
st.markdown('<div class="content-container rtl">', unsafe_allow_html=True)

# Header
col1, col2 = st.columns([3, 1])
with col2:
    st.markdown("""
    <div style="text-align: left;">
        {logo_html}
    </div>
    """, unsafe_allow_html=True)
    
with col1:
    st.markdown("""
    <div class="profile-container">
        <div>
            <div style="font-weight: bold;">ازدهار سعود التميمي</div>
            <div style="font-size: 0.8em; color: #666;">ezdharaltamimi@gmail.com</div>
        </div>
        <img src="https://img.icons8.com/color/96/000000/user-male-circle--v1.png" class="profile-image">
    </div>
    """, unsafe_allow_html=True)

# Placeholder content for main area
st.markdown('<h2 class="rtl">محتوى الصفحة</h2>', unsafe_allow_html=True)
st.markdown('<div class="placeholder-box">محتوى تجريبي للصفحة الرئيسية</div>', unsafe_allow_html=True)
st.markdown('<div class="placeholder-box" style="height: 200px;">محتوى إضافي</div>', unsafe_allow_html=True)
st.markdown('<div class="placeholder-box" style="height: 400px;">مزيد من المحتوى</div>', unsafe_allow_html=True)

st.markdown('</div>', unsafe_allow_html=True)

# Right sidebar menu (appears on the left in RTL)
st.markdown("""
<div class="menu-container">
    <div style="text-align: center; margin-bottom: 20px;">
        {logo_html}
    </div>
    
    <div>
        <a href="#" class="menu-item active">
            <img src="https://img.icons8.com/fluency-systems-regular/48/000000/dashboard-layout.png" class="menu-icon">
            <span>نظرة عامة</span>
        </a>
        <a href="#" class="menu-item">
            <img src="https://img.icons8.com/fluency-systems-regular/48/000000/resume.png" class="menu-icon">
            <span>السيرة الذاتية</span>
        </a>
        <a href="#" class="menu-item">
            <img src="https://img.icons8.com/fluency-systems-regular/48/000000/diploma.png" class="menu-icon">
            <span>السجل الأكاديمي</span>
        </a>
        <a href="#" class="menu-item">
            <img src="https://img.icons8.com/fluency-systems-regular/48/000000/medal.png" class="menu-icon">
            <span>المبادرات والشهادات</span>
        </a>
        <a href="#" class="menu-item">
            <img src="https://img.icons8.com/fluency-systems-regular/48/000000/code.png" class="menu-icon">
            <span>المبادرات</span>
        </a>
        <a href="#" class="menu-item">
            <img src="https://img.icons8.com/fluency-systems-regular/48/000000/certificate.png" class="menu-icon">
            <span>الشهادات والأوسمة</span>
            <div style="font-size: 0.7em; color: #888; margin-right: auto;">روابط مهمة</div>
        </a>
        
        <div class="menu-divider">روابط مهمة</div>
        
        <a href="#" class="menu-item">
            <img src="https://img.icons8.com/fluency-systems-regular/48/000000/home.png" class="menu-icon">
            <span>الصفحة الرئيسية</span>
        </a>
        <a href="#" class="menu-item">
            <img src="https://img.icons8.com/fluency-systems-regular/48/000000/graduation-cap.png" class="menu-icon">
            <span>المعسكرات والبرامج</span>
        </a>
    </div>
</div>
""", unsafe_allow_html=True)