import streamlit as st

# Set page configuration
st.set_page_config(layout="wide")

# Define the layout: left sidebar (1 part) and main area (3 parts)
col1, col2 = st.columns([1, 3])

# ---- Left Sidebar Mimic ----
with col1:
    st.markdown("""
    <div style="background-color: #f8f9fa; padding: 20px; border-radius: 12px; height: 100vh; overflow-y: auto;">
        <h4 style="color:#5f4dee; margin-bottom: 10px;">🎯 فرصة مميزة لك</h4>
        <p style="font-size: 15px; color: #555;">معسكرات وبرامج مقترحة لك</p>

        <div style="margin-top: 30px;">
            <img src="https://via.placeholder.com/300x150" style="width: 100%; border-radius: 10px;" />
            <h5 style="margin-top: 10px;">أساسيات لحام الدوائر الإلكترونية</h5>
            <p style="font-size: 14px;">تقدم هذه الدورة نظرة شاملة على...</p>
            <p style="font-size: 13px; color: gray;">📅 18 مايو - 22 مايو</p>
            <p style="font-size: 13px; color: gray;">📍 الرياض - المقر الرئيسي</p>
        </div>

        <div style="margin-top: 40px;">
            <img src="https://via.placeholder.com/300x150" style="width: 100%; border-radius: 10px;" />
            <h5 style="margin-top: 10px;">اسم معسكر آخر</h5>
            <p style="font-size: 14px;">تفاصيل المعسكر الثاني المقترح...</p>
            <p style="font-size: 13px; color: gray;">📅 قريبًا</p>
            <p style="font-size: 13px; color: gray;">📍 عبر الإنترنت</p>
        </div>
    </div>
    """, unsafe_allow_html=True)

# ---- Main Dashboard Area (Dummy) ----
with col2:
    st.title("📊 لوحة التحكم التجريبية")
    st.write("هذه المساحة مخصصة لتجربة العناصر الأخرى لاحقًا.")
    st.write("يمكنك هنا تطوير الكروت أو عرض نسب التقدم أو أي محتوى آخر.")
