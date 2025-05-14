
import streamlit as st
from PIL import Image

# --- Page Setup ---
st.set_page_config(layout="wide", page_title="اقتراح مسارات")

# --- Top Navigation ---
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

st.markdown('<div style="height: 40px;"></div>', unsafe_allow_html=True)

# --- Styles ---
st.markdown("""
    <style>
        .category-card {
            background-color: #FDF6FF;
            border-radius: 12px;
            padding: 10px 15px;
            height: 90px;
            box-shadow: 0px 2px 6px rgba(0, 0, 0, 0.05);
            display: flex;
            flex-direction: row-reverse;
            align-items: center;
            justify-content: space-between;
            text-align: right;
        }
        .category-card img {
            height: 40px;
            margin-left: 10px;
        }
        .category-card div {
            font-weight: bold;
            font-size: 14px;
            color: #2F195F;
            white-space: nowrap;
        }

        .section-title {
            text-align: right;
            color: #2F195F;
            font-weight: bold;
            font-size: 24px;
            padding: 20px 50px 10px 0;
        }

        .form-label {
            text-align: right;
            color: #2F195F;
            font-weight: bold;
            font-size: 20px;
            padding: 40px 50px 10px 0;
        }

        div[data-baseweb="select"] {
            background-color: #F3EEFF !important;
            border: 2px solid #D6C2F0 !important;
            border-radius: 12px !important;
            font-size: 16px !important;
            color: #2F195F !important;
            direction: rtl !important;
        }

        .block-container {
            padding-left: 50px !important;
            padding-right: 50px !important;
        }
    </style>
""", unsafe_allow_html=True)

# --- Title ---
st.markdown('<div class="section-title">المجالات الرئيسية</div>', unsafe_allow_html=True)

# --- Categories ---
categories = [
    ("تطوير البرمجيات والتطبيقات", "https://cdn.tuwaiq.edu.sa/initiatives_admin/images/mgpdsgmm.alx.png"),
    ("الحوسبة السحابية", "https://cdn.tuwaiq.edu.sa/initiatives_admin/images/lcbl2k2p.x5x.png"),
    ("علم البيانات والذكاء الاصطناعي", "https://cdn.tuwaiq.edu.sa/initiatives_admin/images/pxhazeai.5tg.png"),
    ("هندسة البرمجيات", "https://cdn.tuwaiq.edu.sa/initiatives_admin/images/t0ib4qly.bms.png"),
    ("هندسة الميكاترونيكس", "https://cdn.tuwaiq.edu.sa/initiatives_admin/images/psvxh1jc.vwh.png"),
    ("الأمن السيبراني", "https://cdn.tuwaiq.edu.sa/initiatives_admin/images/1x2x5g4e.hlo.png"),
    ("أنظمة الشبكات", "https://cdn.tuwaiq.edu.sa/initiatives_admin/images/h4zvr2tr.0pu.png"),
]

cols = st.columns(len(categories))

for i, (label, img_url) in enumerate(categories):
    with cols[i]:
        st.markdown(f"""
            <div class="category-card">
                <div>{label}</div>
                <img src="{img_url}" />
            </div>
        """, unsafe_allow_html=True)

# --- Upload CV ---
st.markdown('<div class="form-label">ارفع السيرة الذاتية</div>', unsafe_allow_html=True)
uploaded_file = st.file_uploader("", type=["pdf"])

# --- Recommendation Type ---
st.markdown('<div class="form-label">اختر نوع الاقتراح</div>', unsafe_allow_html=True)
selected_option = st.selectbox("", ["اختر", "طور مهاراتك في مجالك", "غير مسارك"])


