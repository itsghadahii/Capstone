
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



import streamlit as st
from PIL import Image

# --- Page Setup ---
st.set_page_config(layout="wide", page_title="اقتراح مسارات")

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
    if label == "الكل":
        css_class += " category-card-purple"
    with cols[i]:
        st.markdown(f"""
        <div class="{css_class}">
            <img src="{img_url}" />
            <div>{label}</div>
        </div>
        """, unsafe_allow_html=True)


# --- Button Section ---
if st.button("اقترح لي"):
    st.markdown("<hr>", unsafe_allow_html=True)

    col1, col2, col3 = st.columns(3)
    titles = ["طور مهاراتك في مجالك", "غير مسارك لمسار مشابه", "أخرى"]

    # Styles block (only shown once)
    st.markdown("""
    <style>
        .recommend-box {
            background-color: #F9F9F9;
            padding: 24px;
            border-radius: 16px;
            box-shadow: 0 4px 10px rgba(0,0,0,0.04);
            font-family: 'IBM Plex Sans Arabic', sans-serif;
            min-height: 200px;
        }
        .recommend-title {
            font-size: 22px;
            font-weight: 700;
            color: #2F195F;
            text-align: center;
            margin-bottom: 24px;
        }
        .recommend-item {
            background-color: #E3D8FF;
            border-radius: 10px;
            padding: 16px;
            margin-bottom: 14px;
            font-size: 16px;
            font-weight: 400;
            color: #000;
            text-align: center;
        }
    </style>
    """, unsafe_allow_html=True)

    # Render cards
    for col, title in zip([col3, col2, col1], titles):
        with col:
            st.markdown(f"""
            <div class='recommend-box'>
                <div class='recommend-title'>{title}</div>
                <div class='recommend-item'>معسكر</div>
                <div class='recommend-item'>برنامج</div>
            </div>
            """, unsafe_allow_html=True)


