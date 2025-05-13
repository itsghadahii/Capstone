import streamlit as st
import pandas as pd
from io import StringIO
import base64

# Page config
st.set_page_config(layout="wide", page_title="مسار", initial_sidebar_state="collapsed")

with open("images/masar.svg", "rb") as f:
    masar_svg_base64 = base64.b64encode(f.read()).decode()

# Header
st.markdown("""
    <style>
        .main-title {
            font-size: 32px;
            font-weight: bold;
            text-align: right;
            direction: rtl;
            margin-bottom: 20px;
        }
        .course-box {
            border: 1px solid #eee;
            border-radius: 15px;
            padding: 20px;
            text-align: right;
            direction: rtl;
            background-color: #f9f9ff;
            box-shadow: 0px 0px 10px rgba(0,0,0,0.05);
        }
        .course-title {
            font-weight: bold;
            font-size: 20px;
            margin-bottom: 10px;
            text-align: right;
        }
        .course-details {
            font-size: 14px;
            color: #666;
            text-align: right;
        }
        .enroll-button {
            background-color: #ec407a;
            color: white;
            padding: 10px 20px;
            border-radius: 10px;
            text-align: center;
            font-size: 16px;
            margin-bottom: 20px;
            display: inline-block;
        }
    </style>
""", unsafe_allow_html=True)

# Top navigation bar
st.markdown(f"""
    <style>
        .top-nav-wrapper {{
            display: flex;
            background-color: #f8f9ff;
            border-bottom: 1px solid #eee;
            border-radius: 20px;
            justify-content: center;
        }}
        .top-nav {{
            padding: 15px 30px;
            display: flex;
            justify-content: space-between;
            align-items: center;
            direction: rtl;
            width: 100%;
            max-width: 1100px;
        }}
        .top-nav .nav-left {{
            display: flex;
            gap: 50px;
            font-weight: 600;
            font-size: 14px;
        }}
        .top-nav .nav-left div {{
            cursor: pointer;
        }}
        .top-nav .nav-left .active {{
            background-color: #5034b4;
            color: white;
            padding: 6px 14px;
            border-radius: 10px;
        }}
        .top-nav .nav-right {{
            display: flex;
            align-items: center;
            gap: 15px;
        }}
        .top-nav .lang-select {{
            background-color: #eee;
            padding: 6px 12px;
            border-radius: 8px;
            font-weight: bold;
        }}
        .top-nav .login-btn {{
            background-color: #6c47ff;
            color: white;
            padding: 8px 20px;
            border-radius: 10px;
            font-weight: bold;
        }}
    </style>

    <div class="top-nav-wrapper">
        <div class="top-nav">
            <div class="nav-left">
                <img src="data:image/svg+xml;base64,{masar_svg_base64}" width="80" alt="Masar Logo">
                <img src="https://tuwaiq.edu.sa/img/logo.svg" width="130" alt="Tuwaiq Logo">
                <div class="active">الرئيسية</div>
                <div>حول الأكاديمية</div>
                <div>الأكاديميات التابعة</div>
                <div>مركز الاختبارات</div>
                <div>الشراكات</div>
                <div>الاعتمادات</div>
            </div>
        </div>
    </div>
""", unsafe_allow_html=True)

# spacer
st.markdown('<div style="height: 50px; "></div>', unsafe_allow_html=True)

# Title
st.markdown('<div class="main-title">تعرف على خدمة مسار</div>', unsafe_allow_html=True)

# spacer
st.markdown('<div style="height: 30px; "></div>', unsafe_allow_html=True)

# Load example images (replace with actual images or logos if available)
lock_icon = "images/T1.png"
network_icon = "images/T2.png"
flutter_icon = "images/T1.png"

# Course cards
col1, col2, col3 = st.columns(3)

with col1:
    st.image("images/T1.png")
    st.markdown(f"""
            <div class="course-title">🎯 لماذا "مسار"؟</div>
            <div class="course-details">مع "مسار"، لن تضيع وقتك في دورات لا تناسب مستواك أو أهدافك. هذا النظام يزيد من كفاءة التعلم، ويوجهك نحو ما تحتاجه فعلًا لتطوير مهاراتك. ببساطة، هو مساعدك الذكي الذي يعرف ما يناسبك قبل أن تسأل.
            </div>
    """, unsafe_allow_html=True)

with col2:
    st.image("images/T2.png")
    st.markdown(f"""
            <div class="course-title">⚙️ كيف يعمل؟</div>
            <div class="course-details">يقرأ "مسار" ملفك الشخصي أو سيرتك الذاتية، ويفهم مهاراتك الحالية واهتماماتك، ثم يقارنها بمحتوى الدورات المتاحة في المنصة. من خلال تقنيات متقدمة في معالجة اللغة وتحليل البيانات، يقترح دورات ملائمة تمامًا.
            </div>
    """, unsafe_allow_html=True)

with col3:
    st.image("images/T3.png")
    st.markdown(f"""
            <div class="course-title"> 📌 ما هو "مسار"؟</div>
            <div class="course-details">"مسار" هو نظام توصية ذكي مدمج في منصة أكاديمية طويق، يساعد المتدربين على اختيار الدورات الأنسب لهم دون عناء البحث أو التخمين. يعتمد على تحليل المهارات والسيرة الذاتية باستخدام تقنيات الذكاء الاصطناعي، ويقترح مسارات تعليمية مخصصة ومتقدمة لكل مستخدم.

    """, unsafe_allow_html=True)

# spacer
st.markdown('<div style="height: 60px; "></div>', unsafe_allow_html=True) 

# # Button to switch to the app page
# left, middle, right = st.columns(3)

# if left.button("اقترح لي"):
#     st.switch_page("pages/app.py")

# Add custom CSS for the button
st.markdown("""
    <style>
        div.stButton > button {
            background-color: #5034b4;
            color: white;
            padding: 12px 50px;
            font-size: 18px;
            border: none;
            border-radius: 12px;
            cursor: pointer;
            transition: background-color 0.3s, color 0.3s;
        }
        div.stButton > button:hover {
            background-color: white;
            color: #5034b4;
        }
    </style>
""", unsafe_allow_html=True)

# Use layout to center the button
col1, col2, col3, col4, col5, col6, col7 = st.columns([1, 1, 1, 1, 1, 1, 1])
with col4:
    if st.button("اقترح لي"):
        st.switch_page("pages/app.py")


