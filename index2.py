import streamlit as st

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
        right: px;
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

    </style>
    """, unsafe_allow_html=True)

    # Logo and Title
    # st.image("logo.jpg", width=50 , )  # Ensure the image is in the correct directory

    st.markdown('<div class="tuwaiq-logo">', unsafe_allow_html=True)
    st.image("logo.svg", width=150)  # Make sure the image path is correct
    st.markdown('</div>', unsafe_allow_html=True)

    # st.markdown('<img src="logo.jpg" class="tuwaiq-logo" alt="Tuwaiq Academy Logo">', unsafe_allow_html=True)
    st.markdown('<h1 class="main-title">مسار</h1>', unsafe_allow_html=True)
    st.markdown('<h3 class="subtitle">برفع السيرة الذاتية بصيغة PDF</h3>', unsafe_allow_html=True)

    # Upload Box with file uploader inside
    st.markdown("""
    <div class="upload-box">
        <label for="file-upload" class="stFileUploader">
            ارفع السيرة الذاتية هنا
        </label>
        <input type="file" id="file-upload" style="display:none" accept="application/pdf"/>
    </div>
    """, unsafe_allow_html=True)

    # # Simulate the file uploader functionality
    # uploaded_file = st.file_uploader("ارفق الملف هنا", type=['pdf'])
    
    # Next/Continue Button
    if st.button('التالي'):
        if uploaded_file is not None:
            # Process the uploaded file
            st.success('تم رفع السيرة الذاتية بنجاح!')
        else:
            st.warning('يرجى رفع السيرة الذاتية أولاً')

if __name__ == "__main__":
    main()
