import streamlit as st
import pandas as pd
from io import StringIO

# Page config
st.set_page_config(layout="wide")

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
st.markdown("""
    <style>
        .top-nav-wrapper {
            display: flex;
            background-color: #f8f9ff;
            border-bottom: 1px solid #eee;
            border-radius: 20px;
        }
        .top-nav {
            padding: 15px 30px;
            display: flex;
            justify-content: space-between;
            align-items: center;
            direction: rtl;
            width: 100%;
            max-width: 1100px;
        }
        .top-nav .nav-left {
            display: flex;
            gap: 60px;
            font-weight: 600;
            font-size: 15px;
        }
        .top-nav .nav-left div {
            cursor: pointer;
        }
        .top-nav .nav-left .active {
            background-color: #6c47ff;
            color: white;
            padding: 6px 14px;
            border-radius: 10px;
        }
        .top-nav .nav-right {
            display: flex;
            align-items: center;
            gap: 15px;
        }
        .top-nav .lang-select {
            background-color: #eee;
            padding: 6px 12px;
            border-radius: 8px;
            font-weight: bold;
        }
        .top-nav .login-btn {
            background-color: #6c47ff;
            color: white;
            padding: 8px 20px;
            border-radius: 10px;
            font-weight: bold;
        }
    </style>

    <div class="top-nav-wrapper">
        <div class="top-nav">
            <div class="nav-left">
                <img src="https://tuwaiq.edu.sa/img/logo.svg" width="130" alt="Logo">
                <div>حول الأكاديمية</div>
                <div>الأكاديميات التابعة</div>
                <div>مركز الاختبارات</div>
                <div>الشراكات</div>
                <div>الاعتمادات</div>
            </div>
        </div>
    </div>
""", unsafe_allow_html=True)


st.markdown('<div style="height: 50px;"></div>', unsafe_allow_html=True)  # Spacer

# Title
st.markdown('<div class="main-title">تعرف على خدمة مسار</div>', unsafe_allow_html=True)

# Load example images (replace with actual images or logos if available)
lock_icon = "images/T1.png"
network_icon = "images/T2.png"
flutter_icon = "images/T1.png"

# Course cards
col1, col2, col3 = st.columns(3)

with col1:
    # st.markdown('<div class="course-box">', unsafe_allow_html=True)
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
st.markdown('<div style="height: 80px; "></div>', unsafe_allow_html=True) 

uploaded_file = st.file_uploader("اختر ملف السيرة الذاتية", type=["txt", "pdf"], label_visibility="visible")
if uploaded_file is not None:
    st.success("تم تحميل الملف بنجاح!")


left, middle, right = st.columns(3)
if middle.button("اقترح لي", icon=None, type="secondary", use_container_width=True):
    middle.markdown("You clicked the button.")
