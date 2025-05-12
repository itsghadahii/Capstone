
# from PIL import Image
# # --- Page Setup ---
# st.set_page_config(layout="wide", page_title="اقتراح مسارات")

# # --- Custom Styles ---
# st.markdown("""
#     <style>
#         .category-card {
#             background-color: #FDF6FF;
#             border-radius: 12px;
#             padding: 15px;
#             text-align: center;
#             margin: 8px;
#             height: 120px;
#             box-shadow: 0px 2px 6px rgba(0, 0, 0, 0.05);
#         }
#         .category-card img {
#             height: 40px;
#             margin-bottom: 5px;
#         }
#         .category-card-purple {
#             border: 3px solid #D6C2F0;
#         }
#     </style>
# """, unsafe_allow_html=True)

# # --- Section: Categories ---
# st.markdown("<h3 style='text-align:right;'>المجالات الرئيسية</h3>", unsafe_allow_html=True)

# categories = [
#     ("تطوير البرمجيات والتطبيقات", "https://cdn.tuwaiq.edu.sa/initiatives_admin/images/mgpdsgmm.alx.png"),
#     ("الحوسبة السحابية", "https://cdn.tuwaiq.edu.sa/initiatives_admin/images/lcbl2k2p.x5x.png"),
#     ("علم البيانات والذكاء الاصطناعي", "https://cdn.tuwaiq.edu.sa/initiatives_admin/images/pxhazeai.5tg.png"),
#     ("هندسة البرمجيات", "https://cdn.tuwaiq.edu.sa/initiatives_admin/images/t0ib4qly.bms.png"),
#     ("هندسة الميكاترونيكس", "https://cdn.tuwaiq.edu.sa/initiatives_admin/images/psvxh1jc.vwh.png"),
#     ("الأمن السيبراني", "https://cdn.tuwaiq.edu.sa/initiatives_admin/images/1x2x5g4e.hlo.png"),
#     ("أنظمة الشبكات", "https://cdn.tuwaiq.edu.sa/initiatives_admin/images/h4zvr2tr.0pu.png"),
#     ("الكل", "")  # Last one has purple border
# ]

# cols = st.columns(len(categories))

# for i, (label, img_url) in enumerate(categories):
#     css_class = "category-card"
#     if label == "الكل":
#         css_class += " category-card-purple"
#     with cols[i]:
#         st.markdown(f"""
#         <div class="{css_class}">
#             <img src="{img_url if img_url else 'https://via.placeholder.com/40'}" />
#             <div>{label}</div>
#         </div>
#         """, unsafe_allow_html=True)

# # --- Button Section ---
# st.markdown("###", unsafe_allow_html=True)
# if st.button("اقترح لي"):
#     st.markdown("<hr>", unsafe_allow_html=True)

#     # --- Section: Recommendations ---
#     col1, col2, col3 = st.columns(3)

#     with col3:
#         st.markdown("<div class='section-title'>طور مهاراتك في مجالك</div>", unsafe_allow_html=True)
#         st.markdown("<div class='recommend-box'>", unsafe_allow_html=True)
#         st.markdown("<div class='item-title'>اسم المسار</div>", unsafe_allow_html=True)
#         st.markdown("<div class='item-card'>معسكر</div>", unsafe_allow_html=True)
#         st.markdown("<div class='item-card'>برنامج</div>", unsafe_allow_html=True)
#         st.markdown("</div>", unsafe_allow_html=True)

#     with col2:
#         st.markdown("<div class='section-title'>غير مسارك لمسار مشابه</div>", unsafe_allow_html=True)
#         st.markdown("<div class='recommend-box'>", unsafe_allow_html=True)
#         st.markdown("<div class='item-title'>اسم المسار</div>", unsafe_allow_html=True)
#         st.markdown("<div class='item-card'>معسكر</div>", unsafe_allow_html=True)
#         st.markdown("<div class='item-card'>برنامج</div>", unsafe_allow_html=True)
#         st.markdown("</div>", unsafe_allow_html=True)

#     with col1:
#         st.markdown("<div class='section-title'>أخرى</div>", unsafe_allow_html=True)
#         st.markdown("<div class='recommend-box'>", unsafe_allow_html=True)
#         st.markdown("<div class='item-title'>اسم المسار</div>", unsafe_allow_html=True)
#         st.markdown("<div class='item-card'>معسكر</div>", unsafe_allow_html=True)
#         st.markdown("<div class='item-card'>برنامج</div>", unsafe_allow_html=True)
#         st.markdown("</div>", unsafe_allow_html=True)



# import streamlit as st
# from PIL import Image

# # --- Page Setup ---
# st.set_page_config(layout="wide", page_title="اقتراح مسارات")

# # --- Custom Styles ---
# st.markdown("""
#     <style>
#         .category-card {
#             background-color: #FDF6FF;
#             border-radius: 12px;
#             padding: 15px;
#             text-align: center;
#             margin: 8px;
#             height: 120px;
#             box-shadow: 0px 2px 6px rgba(0, 0, 0, 0.05);
#         }
#         .category-card img {
#             height: 40px;
#             margin-bottom: 5px;
#         }
#         .category-card-purple {
#             border: 3px solid #D6C2F0;
#         }
#         .recommend-section {
#             background-color: #FAFAFA;
#             border-radius: 10px;
#             padding: 15px;
#             margin: 10px;
#             text-align: right;
#         }
#         .recommend-section .item-card {
#             background-color: #FFFFFF;
#             border: 1px solid #DDD;
#             border-radius: 6px;
#             padding: 10px;
#             margin: 6px 0;
#             font-size: 15px;
#             font-family: 'IBM Plex Sans Arabic', sans-serif;
#         }
#         .recommend-section .section-title {
#             color: #2F195F;
#             font-weight: bold;
#             font-size: 18px;
#             margin-bottom: 8px;
#         }
#     </style>
# """, unsafe_allow_html=True)

# # --- Section: Categories ---
# st.markdown("<h3 style='text-align:right;'>المجالات الرئيسية</h3>", unsafe_allow_html=True)

# categories = [
#     ("تطوير البرمجيات والتطبيقات", "https://cdn.tuwaiq.edu.sa/initiatives_admin/images/mgpdsgmm.alx.png"),
#     ("الحوسبة السحابية", "https://cdn.tuwaiq.edu.sa/initiatives_admin/images/lcbl2k2p.x5x.png"),
#     ("علم البيانات والذكاء الاصطناعي", "https://cdn.tuwaiq.edu.sa/initiatives_admin/images/pxhazeai.5tg.png"),
#     ("هندسة البرمجيات", "https://cdn.tuwaiq.edu.sa/initiatives_admin/images/t0ib4qly.bms.png"),
#     ("هندسة الميكاترونيكس", "https://cdn.tuwaiq.edu.sa/initiatives_admin/images/psvxh1jc.vwh.png"),
#     ("الأمن السيبراني", "https://cdn.tuwaiq.edu.sa/initiatives_admin/images/1x2x5g4e.hlo.png"),
#     ("أنظمة الشبكات", "https://cdn.tuwaiq.edu.sa/initiatives_admin/images/h4zvr2tr.0pu.png"),
#     #("الكل", "")
# ]
# cols = st.columns(len(categories))

# for i, (label, img_url) in enumerate(categories):
#     css_class = "category-card"
#     if label == "الكل":
#         css_class += " category-card-purple"
#     with cols[i]:
#         st.markdown(f"""
#         <div class="{css_class}">
#             <img src="{img_url}" />
#             <div>{label}</div>
#         </div>
#         """, unsafe_allow_html=True)


# # --- Button Section ---
# if st.button("اقترح لي"):
#     st.markdown("<hr>", unsafe_allow_html=True)

#     col1, col2, col3 = st.columns(3)
#     titles = ["طور مهاراتك في مجالك", "غير مسارك لمسار مشابه", "أخرى"]

#     # Styles block (only shown once)
#     st.markdown("""
#     <style>
#         .recommend-box {
#             background-color: #F9F9F9;
#             padding: 24px;
#             border-radius: 16px;
#             box-shadow: 0 4px 10px rgba(0,0,0,0.04);
#             font-family: 'IBM Plex Sans Arabic', sans-serif;
#             min-height: 200px;
#         }
#         .recommend-title {
#             font-size: 22px;
#             font-weight: 700;
#             color: #2F195F;
#             text-align: center;
#             margin-bottom: 24px;
#         }
#         .recommend-item {
#             background-color: #E3D8FF;
#             border-radius: 10px;
#             padding: 16px;
#             margin-bottom: 14px;
#             font-size: 16px;
#             font-weight: 400;
#             color: #000;
#             text-align: center;
#         }
#     </style>
#     """, unsafe_allow_html=True)

#     # Render cards
#     for col, title in zip([col3, col2, col1], titles):
#         with col:
#             st.markdown(f"""
#             <div class='recommend-box'>
#                 <div class='recommend-title'>{title}</div>
#                 <div class='recommend-item'>معسكر</div>
#                 <div class='recommend-item'>برنامج</div>
#             </div>
#             """, unsafe_allow_html=True)



import streamlit as st
from PIL import Image
#import os
#from dotenv import load_dotenv

# Required fix for protobuf
#os.environ["PROTOCOL_BUFFERS_PYTHON_IMPLEMENTATION"] = "python"

# Load .env keys (OpenAI & Weaviate)
#load_dotenv()

#from sttest import best_courses, render_course_card_ar



# --- Page Setup ---
st.set_page_config(layout="wide", page_title="اقتراح مسارات")


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


# --- Custom Styles ---
st.markdown("""
    <style>
        .category-card {
            background-color: #FDF6FF;
            border-radius: 12px;
            padding: 15px;
            text-align: center;
            margin: 8px;
            height: 120px;
            box-shadow: 0px 2px 6px rgba(0, 0, 0, 0.05);
        }
        .category-card img {
            height: 40px;
            margin-bottom: 5px;
        }
        .category-card-purple {
            border: 3px solid #D6C2F0;
        }
        .recommend-section {
            background-color: #FAFAFA;
            border-radius: 10px;
            padding: 15px;
            margin: 10px;
            text-align: right;
        }
        .recommend-section .item-card {
            background-color: #FFFFFF;
            border: 1px solid #DDD;
            border-radius: 6px;
            padding: 10px;
            margin: 6px 0;
            font-size: 15px;
            font-family: 'IBM Plex Sans Arabic', sans-serif;
        }
        .recommend-section .section-title {
            color: #2F195F;
            font-weight: bold;
            font-size: 18px;
            margin-bottom: 8px;
        }
    </style>
""", unsafe_allow_html=True)

# --- Section: Categories ---
st.markdown("<h3 style='text-align:right;'>المجالات الرئيسية</h3>", unsafe_allow_html=True)

categories = [
    ("تطوير البرمجيات والتطبيقات", "https://cdn.tuwaiq.edu.sa/initiatives_admin/images/mgpdsgmm.alx.png"),
    ("الحوسبة السحابية", "https://cdn.tuwaiq.edu.sa/initiatives_admin/images/lcbl2k2p.x5x.png"),
    ("علم البيانات والذكاء الاصطناعي", "https://cdn.tuwaiq.edu.sa/initiatives_admin/images/pxhazeai.5tg.png"),
    ("هندسة البرمجيات", "https://cdn.tuwaiq.edu.sa/initiatives_admin/images/t0ib4qly.bms.png"),
    ("هندسة الميكاترونيكس", "https://cdn.tuwaiq.edu.sa/initiatives_admin/images/psvxh1jc.vwh.png"),
    ("الأمن السيبراني", "https://cdn.tuwaiq.edu.sa/initiatives_admin/images/1x2x5g4e.hlo.png"),
    ("أنظمة الشبكات", "https://cdn.tuwaiq.edu.sa/initiatives_admin/images/h4zvr2tr.0pu.png"),
    #("الكل", "")
]

cols = st.columns(len(categories))


for i, (label, img_url) in enumerate(categories):
    css_class = "category-card"
    with cols[i]:
        st.markdown(f"""
        <div class="{css_class}">
            <img src="{img_url}" />
            <div>{label}</div>
        </div>
        """, unsafe_allow_html=True)


# --- Recommendation Dropdown & Box Section ---
st.markdown("""
    <style>
        .dropdown-container {
            display: flex;
            justify-content: flex-end;
            margin-top: 30px;
            margin-bottom: 20px;
            direction: rtl;
        }
        .dropdown-container p {
            font-size: 20px;
            color: #2F195F;
            font-weight: bold;
            margin-left: 15px;
        }
        .stSelectbox {
            width: 280px !important;
            direction: rtl;
        }
        div[data-baseweb="select"] {
            background-color: #E3D8FF !important;
            border: 2px solid #D6C2F0 !important;
            border-radius: 12px !important;
            font-size: 18px !important;
            color: #2F195F !important;
            text-align: right !important;
            font-family: 'IBM Plex Sans Arabic', sans-serif !important;
        }
        .recommend-box-single {
            background-color: #F9F9F9;
            padding: 30px;
            border-radius: 20px;
            margin-top: 20px;
            box-shadow: 0 4px 12px rgba(0,0,0,0.03);
            font-family: 'IBM Plex Sans Arabic', sans-serif;
            direction: rtl;
            text-align: right;
        }
        .recommend-title {
            font-size: 22px;
            font-weight: bold;
            color: #2F195F;
            margin-bottom: 20px;
            text-align: right;
        }
        .recommend-item {
            background-color: #E3D8FF;
            border-radius: 12px;
            padding: 16px;
            margin-bottom: 12px;
            font-size: 18px;
            text-align: right;
            color: #000;
        }
    </style>
""", unsafe_allow_html=True)

# --- Dropdown in RTL container ---
# --- Dropdown aligned to right using columns ---

col1, col2, col3 = st.columns([6, 2, 2])
with col3:

    st.markdown('<p style="font-size:20px; color:#2F195F; font-weight:bold; text-align:right;">اختر نوع الاقتراح</p>', unsafe_allow_html=True)
    option = st.selectbox("", ["اختر", "طور مهاراتك في مجالك", "غير مسارك"])




if option and option != "اختر":
    st.markdown(f"""
        <div class='recommend-box-single'>
            <div class='recommend-title'>{option}</div>
            <div class='recommend-item'>&nbsp;</div>
            <div class='recommend-item'>&nbsp;</div>
            <div class='recommend-item'>&nbsp;</div>
        </div>
    """, unsafe_allow_html=True)



# Dropdown my 
# with st.container():
#     st.markdown('<div class="dropdown-container"><p>اختر نوع الاقتراح</p>', unsafe_allow_html=True)
#     option = st.selectbox("", ["اختر", "طور مهاراتك في مجالك", "غير مسارك"])
#     st.markdown("</div>", unsafe_allow_html=True)

# # Show recommendations if option selected
# if option != "اختر":
#     st.markdown(f"""
#         <div class='recommend-box-single'>
#             <div class='recommend-title'>{option}</div>
#     """, unsafe_allow_html=True)

#     # Static query for demo (you can make this dynamic)
#     query_text = "الذكاء الاصطناعي" if option == "غير مسارك" else "تحليل البيانات"

#     try:
#         recommendations = best_courses(query_text)
#         for rec in recommendations:
#             st.markdown(render_course_card_ar(rec), unsafe_allow_html=True)
#     except Exception as e:
#         st.error(f" خطأ أثناء جلب التوصيات: {e}")

#     st.markdown("</div>", unsafe_allow_html=True)


# Dropdown
# col1, col2, col3 = st.columns([6, 2, 2])
# with col3:
#     st.markdown('<p style="font-size:20px; color:#2F195F; font-weight:bold; text-align:right;">اختر نوع الاقتراح</p>', unsafe_allow_html=True)
#     option = st.selectbox("", ["اختر", "طور مهاراتك في مجالك", "غير مسارك"])

# # Render courses if selected
# if option != "اختر":
#     courses = best_courses("""Your CV text here""")  

#     col1, col2, col3 = st.columns([1, 1, 1])
#     col1_content = col2_content = col3_content = ""

#     for i, course in enumerate(courses):
#         card = f"""<div class="course-card">{render_course_card_ar(course)}</div>"""
#         if i % 3 == 0:
#             col1_content += card
#         elif i % 3 == 1:
#             col2_content += card
#         else:
#             col3_content += card

#     with col1: st.markdown(col1_content, unsafe_allow_html=True)
#     with col2: st.markdown(col2_content, unsafe_allow_html=True)
#     with col3: st.markdown(col3_content, unsafe_allow_html=True)
