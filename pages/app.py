
import json
import weaviate
from sentence_transformers import SentenceTransformer
from langchain.embeddings import HuggingFaceEmbeddings  # Updated import
from uuid import uuid4
import os
from weaviate.collections.classes.config import DataType
from openai import OpenAI
import os
from dotenv import load_dotenv
import sqlite3
from datetime import datetime
load_dotenv()

def serialize_date(value):
    if isinstance(value, datetime):
        return value.isoformat()
    return value


client = OpenAI(
  api_key= os.environ["OPENAI_API_KEY"]
)

# Best practice: store your credentials in environment variables
weaviate_url = os.environ["WEAVIATE_URL"]
weaviate_api_key = os.environ["WEAVIATE_API_KEY"]
# COLLECTION_NAME = "Bootcamp_en"
# COLLECTION_NAME = "Bootcamp"
COLLECTION_NAME = "COMBINE_BP"

# 1. Connect to the database (creates one if it doesn't exist)
conn = sqlite3.connect('resume_database.db')

# 2. Create a cursor object
cursor = conn.cursor()

# ---- Load JSON ----
with open('Jsons/bootcamps_programs.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

# ---- Set up LangChain Embeddings (using local model) ----
embedder = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")

# Connect to Weaviate
client = weaviate.connect_to_weaviate_cloud(
    cluster_url=weaviate_url,
    auth_credentials=weaviate.auth.AuthApiKey(api_key=weaviate_api_key)
)

print(client.is_ready())  # Should print: `True`

def format_json_item(item):
    text = f"""
    المجال: {item['initiativeScopeName']}

    العنوان: {item['title']}
    
    الوصف: {item['description']}
    
    الأهداف: {'; '.join(item.get('goals', []))}
    
    المميزات: {'; '.join(item.get('features', []))}
    
    المتطلبات: {'; '.join(item.get('requirements', []))}
    
    الأسئلة الشائعة: {'; '.join([f'{q} {a}' for q, a in item.get('faqs', {}).items()])}
    """
    return text.strip()

def format_json_item_en(item):
    text = f"""
    Major: {item['initiativeScopeName']}

    Title: {item['title']}
    
    Description: {item['description']}
    
    Goals: {'; '.join(item.get('goals', []))}
    
    Features: {'; '.join(item.get('features', []))}
    
    Requirements: {'; '.join(item.get('requirements', []))}
    """
    # Faqs: {'; '.join([f'{q} {a}' for q, a in item.get('faqs', {}).items()])}
    return text.strip()

def save_weaviate():
    # Delete existing collection if needed
    try:
        client.collections.delete(COLLECTION_NAME)
    except:
        pass

    # Create new collection with proper DataType objects
    bootcamp_collection = client.collections.create(
        name=COLLECTION_NAME,
        properties=[
            {
                "name": "index", 
                "data_type": DataType.INT
            },
            {
                "name": "initiativeScopeName", 
                "data_type": DataType.TEXT
            },
            {
                "name": "initiativeCategoryName", 
                "data_type": DataType.TEXT
            },
            {
                "name": "initiativeAgeName", 
                "data_type": DataType.TEXT
            },
            {
                "name": "title", 
                "data_type": DataType.TEXT
            },
            {
                "name": "description", 
                "data_type": DataType.TEXT
            },
            {
                "name": "language", 
                "data_type": DataType.TEXT
            },
            {
                "name": "location", 
                "data_type": DataType.TEXT
            },
            {
                "name": "isRegistrationOpen", 
                "data_type": DataType.BOOL
            },
            {
                "name": "registrationEndDate", 
                "data_type": DataType.DATE
            },
            {
                "name": "startDate", 
                "data_type": DataType.DATE
            },
            {
                "name": "endDate", 
                "data_type": DataType.DATE
            },
            {
                "name": "startTime", 
                "data_type": DataType.TEXT
            },
            {
                "name": "endTime", 
                "data_type": DataType.TEXT
            },
            {
                "name": "goals", 
                "data_type": DataType.TEXT_ARRAY  # Array type
            },
            {
                "name": "features", 
                "data_type": DataType.TEXT_ARRAY
            },
            {
                "name": "requirements", 
                "data_type": DataType.TEXT_ARRAY  # Array type
            },
            {
                "name": "faqs", 
                "data_type": DataType.TEXT
            },
            {
                "name": "slug", 
                "data_type": DataType.TEXT
            },
            {
                "name": "content", 
                "data_type": DataType.TEXT
            }
        ]
    )

    # Insert data
    for i,item in enumerate(data):
        if COLLECTION_NAME == "Bootcamp_en":
            content = format_json_item_en(item)
        else:
            content = format_json_item(item)
        properties = {
            "index": i,
            "initiativeScopeName": item["initiativeScopeName"],
            "initiativeCategoryName": item["initiativeCategoryName"],
            "initiativeAgeName": item["initiativeAgeName"],
            "title": item["title"],
            "description": item["description"],
            "language": item["language"],
            "location": item["locationName"],
            "isRegistrationOpen": item["isRegistrationOpen"],
            "registrationEndDate": item["registrationEndDate"],
            "startDate": item["startDate"],
            "endDate": item["endDate"],
            "startTime": item["startTimeText"],
            "endTime": item["endTimeText"],

            "goals": item.get("goals", []),
            "features": item.get("features", []),
            "requirements": item.get("requirements", []),
            "faqs": json.dumps(item.get("faqs", {}), ensure_ascii=False),
            
            "slug": item["slug"],

            # "content": format_json_item(item)
            # "content": format_json_item_en(item)
            "content": content
        }
        print(f"\n\n====prop\n\n{properties['index']} : {properties['title']}")
        # print(f"\n====\nchunk\n\n{properties['content']}\n\n====\n")
        embedding = embedder.embed_query(properties["content"])
        
        bootcamp_collection.data.insert(
            properties=properties,
            vector=embedding
        )

def format_json_item_combine(item):
    text = f"""
    Major: {item['initiativeScopeName_en']}

    Title: {item['title_en']}
    
    Description: {item['description_en']}
    
    Goals: {'; '.join(item.get('goals_en', []))}
    
    Features: {'; '.join(item.get('features_en', []))}
    
    Requirements: {'; '.join(item.get('requirements_en', []))}
    """
    # Faqs: {'; '.join([f'{q} {a}' for q, a in item.get('faqs', {}).items()])}
    return text.strip()

def save_weaviate_combine():
    # Delete existing collection if needed
    try:
        client.collections.delete(COLLECTION_NAME)
    except:
        pass

    # Create new collection with proper DataType objects
    bootcamp_collection = client.collections.create(
        name=COLLECTION_NAME,
        properties=[
            {
                "name": "index", 
                "data_type": DataType.INT
            },
            {
                "name": "initiativeScopeName", 
                "data_type": DataType.TEXT
            },
            {
                "name": "initiativeScopeName_en", 
                "data_type": DataType.TEXT
            },
            {
                "name": "initiativeCategoryName", 
                "data_type": DataType.TEXT
            },
            {
                "name": "initiativeCategoryName_en", 
                "data_type": DataType.TEXT
            },
            {
                "name": "initiativeAgeName", 
                "data_type": DataType.TEXT
            },
            {
                "name": "title", 
                "data_type": DataType.TEXT
            },
            {
                "name": "title_en", 
                "data_type": DataType.TEXT
            },
            {
                "name": "description", 
                "data_type": DataType.TEXT
            },
            {
                "name": "description_en", 
                "data_type": DataType.TEXT
            },
            {
                "name": "language", 
                "data_type": DataType.TEXT
            },
            {
                "name": "location", 
                "data_type": DataType.TEXT
            },
            {
                "name": "location_en", 
                "data_type": DataType.TEXT
            },
            {
                "name": "isRegistrationOpen", 
                "data_type": DataType.BOOL
            },
            {
                "name": "registrationEndDate", 
                "data_type": DataType.DATE
            },
            {
                "name": "startDate", 
                "data_type": DataType.DATE
            },
            {
                "name": "endDate", 
                "data_type": DataType.DATE
            },
            {
                "name": "startTime", 
                "data_type": DataType.TEXT
            },
            {
                "name": "startTime_en", 
                "data_type": DataType.TEXT
            },
            {
                "name": "endTime", 
                "data_type": DataType.TEXT
            },
            {
                "name": "endTime_en", 
                "data_type": DataType.TEXT
            },
            {
                "name": "goals", 
                "data_type": DataType.TEXT_ARRAY
            },
            {
                "name": "goals_en", 
                "data_type": DataType.TEXT_ARRAY
            },
            {
                "name": "features", 
                "data_type": DataType.TEXT_ARRAY
            },
            {
                "name": "features_en", 
                "data_type": DataType.TEXT_ARRAY
            },
            {
                "name": "requirements", 
                "data_type": DataType.TEXT_ARRAY
            },
            {
                "name": "requirements_en", 
                "data_type": DataType.TEXT_ARRAY
            },
            {
                "name": "faqs", 
                "data_type": DataType.TEXT
            },
            {
                "name": "slug", 
                "data_type": DataType.TEXT
            },
            {
                "name": "content", 
                "data_type": DataType.TEXT
            }
        ]
    )

    # Insert data
    for i,item in enumerate(data):

        content = format_json_item_combine(item)
        properties = {
            "index": i,
            "initiativeScopeName": item["initiativeScopeName"],
            "initiativeScopeName_en": item.get("initiativeScopeName_en", ""),

            "initiativeCategoryName": item["initiativeCategoryName"],
            "initiativeCategoryName_en": item.get("initiativeCategoryName_en", ""),

            "initiativeAgeName": item["initiativeAgeName"],

            "title": item["title"],
            "title_en": item.get("title_en", ""),

            "description": item["description"],
            "description_en": item.get("description_en", ""),

            "language": item["language"],

            "location": item["locationName"],
            "location_en": item.get("locationName_en", ""),

            "isRegistrationOpen": item["isRegistrationOpen"],

            "registrationEndDate": item["registrationEndDate"],

            "startDate": item["startDate"],

            "endDate": item["endDate"],

            "startTime": item["startTimeText"],
            "startTime_en": item.get("startTimeText_en", ""),

            "endTime": item["endTimeText"],
            "endTime_en": item.get("endTimeText_en", ""),

            "goals": item["goals"],
            "goals_en": item.get("goals_en", []),

            "features": item["features"],
            "features_en": item.get("features_en", []),
            
            "requirements": item["requirements"],
            "requirements_en": item.get("requirements_en", []),
            
            "faqs": json.dumps(item.get("faqs", {}), ensure_ascii=False),
            
            "slug": item["slug"],

            "content": content
        }
        print(f"\n\n====prop\n\n{properties['index']} : {properties['title']} : {properties['title_en']}")
        # print(f"\n====\nchunk\n\n{properties['content']}\n\n====\n")
        embedding = embedder.embed_query(properties["content"])
        
        bootcamp_collection.data.insert(
            properties=properties,
            vector=embedding
        )

def search_similar_bootcamps(query, limit=5):
    """
    Search for bootcamps similar to the query.
    
    Args:
        query (str): The search query
        limit (int): Number of results to return
        
    Returns:
        list: List of similar bootcamps
    """
    # Generate query embedding
    query_embedding = embedder.embed_query(query)
    
    try:
        # Get the collection
        bootcamp_collection = client.collections.get(COLLECTION_NAME)
        
        # Perform vector search - use 'near_vector' instead of 'vector'
        results = bootcamp_collection.query.hybrid(
            query=query,
            vector=query_embedding,  # Changed from 'vector' to 'near_vector'
            limit=limit,
            return_properties=["title","title_en","initiativeCategoryName","initiativeCategoryName_en","initiativeScopeName","initiativeScopeName_en" ,"content", "language", "location","isRegistrationOpen","registrationEndDate", "startDate","endDate","index","slug","initiativeAgeName"]
        )
        
        return results.objects
    except Exception as e:
        print(f"Error during search: {e}")
        return []
    
    
def print_search_results(results):
    """Print formatted search results"""
    if not results:
        print("No results found")
        return
    
    print(f"\n=== Found {len(results)} similar bootcamps ===\n")
    
    for i, result in enumerate(results, 1):
        props = result.properties
        
        # Check if certainty exists before formatting
        certainty = getattr(result.metadata, 'certainty', None)
        if certainty is not None:
            score_str = f"Score: {certainty:.4f}"
        else:
            score_str = "Score: N/A"
        
        print(f"Result #{i} - {score_str}")
        print(f"index: {props.get('index', 'N/A')}")
        print(f"Title: {props.get('title', 'N/A')}")
        print(f"Title: {props.get('title_en', 'N/A')}")
        print(f"initiativeCategoryName_en: {props.get('initiativeCategoryName_en', 'N/A')}")
        print(f"Language: {props.get('language', 'N/A')}")
        print(f"Location: {props.get('location', 'N/A')}")
        print(f"Start Date: {props.get('startDate', 'N/A')}")
        # print(f"faqs: {props.get('faqs', 'N/A')}")
        
        # Get content safely and truncate it
        content = props.get('content', 'N/A')
        if content != 'N/A':
            print(f"Excerpt: {content}...")
        else:
            print("Excerpt: N/A")
        slug= props.get('slug', 'N/A')
        if slug != 'N/A':
            print(f"URL: https://tuwaiq.edu.sa/bootcamp/{slug}/view")
        else:
            print("URL: N/A")
        
            
        print("\n" + "-"*50 + "\n")

def results_json(results):
    
    if not results:
        print("No results found")
        return
    
    # print(f"\n=== Found {len(results)} similar bootcamps ===\n")
    all_jsons = []
    for i, result in enumerate(results, 1):
        props = result.properties
        url = f"https://tuwaiq.edu.sa/bootcamp/{props.get('slug', 'N/A')}/view"
        json = {
                "title": props.get('title', 'N/A'),
                "title_en": props.get('title_en', 'N/A'),
                "initiativeCategoryName": props.get('initiativeCategoryName', 'N/A'),
                "initiativeCategoryName_en": props.get('initiativeCategoryName_en', 'N/A'),
                "initiativeScopeName": props.get('initiativeScopeName', 'N/A'),
                "initiativeScopeName_en": props.get('initiativeScopeName_en', 'N/A'),
                "content": props.get('content', 'N/A'),
                "language": props.get('language', 'N/A'),
                "location": props.get('location', 'N/A'),
                "isRegistrationOpen": props.get('isRegistrationOpen', 'N/A'),
                "registrationEndDate": serialize_date(props.get('registrationEndDate', 'N/A')),
                "startDate": serialize_date(props.get('startDate', 'N/A')),
                "endDate": serialize_date(props.get('endDate', 'N/A')),
                "initiativeAgeName": props.get('initiativeAgeName', 'N/A'),
                # "index": props.get('index', 'N/A'),
                "URL": url
            }
        all_jsons.append(json)
    return all_jsons


def career_openai_call(content):
    
    completion = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": "You will be given CVs/Resumes. Your task is to first extract the field and career level based on skills or education. Then, write a description that highlights **only missing skills, techniques, or areas of growth** that will help the user progress in their career. The description should focus on the **next step in their learning**, ensuring it is specific to the user’s career path and will help them advance. **DO NOT mention completed courses, certifications, or personal information (e.g., name, email, phone)**. Do not provide general career advice or narrative about their past experience. Only suggest skills, tools, or techniques they might need to learn or improve upon."},
            {"role": "user", "content": content}
        ]
    )

    return completion.choices[0].message.content 


def get_cv_by_id(id):
    query = "SELECT extracted_text FROM resumes s WHERE s.id = ?"
    cursor.execute(query, (id,))  # Safe parameterized query
    row = cursor.fetchone()
    if row:
        print(row[0])
        return row[0]
    return None












# save_weaviate()
# save_weaviate_combine()




# Example queries
# example_queries = [
#     """""",
#     # "تطوير تطبيقات الويب",  # Web application development
#     # "الذكاء الاصطناعي",     # Artificial intelligence
#     # "تعلم الآلة",          # Machine learning
#     # "تطوير تطبيقات الجوال", # Mobile app development
#     # "سايبر سكيورتي"        # Cybersecurity
# ]

# # Run searches for each example query
# for query in example_queries:
#     print(f"\n\n===== Searching for: '{query}' =====")
#     results = search_similar_bootcamps(query, limit=5)
#     print_search_results(results)

# input = input("id:")
# input = 11
# query= get_cv_by_id(input)
# print(f"\n\n-------Query: {query}\n\n---------\n\n")
# llmoutput = career_openai_call(query)
# print(f"\n\n-------Query: {llmoutput}\n\n---------\n\n")

def best_courses(query):
    print(f"\n\n===== Searching for: '{query}' =====")
    results = search_similar_bootcamps(query, limit=5)
    print(results_json(results))
    return results_json(results)


# cv= extracted_text



import streamlit as st
import fitz  # PyMuPDF
import pytesseract
from PIL import Image
import io
import os
import tempfile
import hashlib
from datetime import datetime

from datetime import datetime
from dateutil.parser import parse  # Handles timezones and complex formats

@st.cache_data
def extract_text_from_resume(pdf_content):
    """
    Extract text from a resume PDF using PyMuPDF and OCR if needed.
    This function is cached to improve performance.
    """
    # Create a temporary file to work with
    with tempfile.NamedTemporaryFile(delete=False, suffix='.pdf') as tmp_file:
        tmp_file.write(pdf_content)
        pdf_path = tmp_file.name

    try:
        doc = fitz.open(pdf_path)
        text = ""

        for page_num in range(len(doc)):
            page = doc.load_page(page_num)

            # Try to get text directly first
            page_text = page.get_text()

            # If little or no text was extracted, try OCR
            if len(page_text.strip()) < 100:  # Arbitrary threshold
                # Get the page as an image
                pix = page.get_pixmap(matrix=fitz.Matrix(300/72, 300/72))  # 300 DPI
                img = Image.open(io.BytesIO(pix.tobytes("png")))

                # Use OCR to extract text from the image
                page_text = pytesseract.image_to_string(img)

            text += page_text + "\n\n"

        doc.close()
        return text
    finally:
        # Clean up the temporary file
        os.unlink(pdf_path)

def calculate_duration(start_date_str, end_date_str):
    # Default if dates are missing/invalid
    if not start_date_str or not end_date_str or start_date_str == "N/A" or end_date_str == "N/A":
        return "غير محدد"
    
    try:
        # Parse ISO 8601 dates with timezones (e.g., "2025-06-15T10:00:00+03:00")
        start_date = parse(start_date_str)
        end_date = parse(end_date_str)
        
        delta = end_date - start_date
        days = delta.days
        
        if days < 0:
            return "تاريخ غير صحيح"
        
        # Weeks
        if days <= 6:
            return "أسبوع"
        elif 7 <= days <= 13:
            return "أسبوع"
        elif 14 <= days <= 20:
            return "أسبوعين"
        elif 21 <= days <= 27:
            return "٣ أسابيع"
        
        # Months (approximate)
        months = round(days / 30)  # 30 days ≈ 1 month
        
        if months == 1:
            return "شهر"
        elif months == 2:
            return "شهرين"
        elif 3 <= months <= 11:
            # Convert Western numerals to Arabic (e.g., 3 → ٣)
            arabic_nums = str(months).translate(str.maketrans('0123456789', '٠١٢٣٤٥٦٧٨٩'))
            return f"{arabic_nums} شهور"
        else:
            return "سنة"  # 12+ months
    
    except (ValueError, TypeError):
        return "تنسيق التاريخ غير صحيح"
    

def render_course_card_ar(course):
    title = course.get("title", "—")
    image_url = "data:image/png;base64,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"
    audience = course.get("initiativeAgeName", "كبار")
    type_ = course.get("initiativeCategoryName", "-")

    if course.get("isRegistrationOpen", "N/A") == True:
        status = "متاح التسجيل"
    else:
        status = "مغلق"

    start_date_str = course.get("startDate", "-")

    if start_date_str != "-":
        dt = datetime.fromisoformat(start_date_str)
        formatted_date = f"{dt.year}-{dt.month}-{dt.day}"
    else:
        formatted_date = "-"
    end_date = course.get("endDate", "N/A")  # Make sure to get endDate from course

    # Calculate duration properly
    duration = calculate_duration(course.get("startDate"), course.get("endDate"))

    url = course.get("URL", "#")


    html = f"""
    <div style="width: 100%; border-radius: 20px; overflow: hidden; border: 1px solid #eee;
                background-color: #fff; box-shadow: 0 4px 6px rgba(0,0,0,0.1); height: 100%;">
        <a href="{url}" target="_blank" style="text-decoration: none; color: inherit;">
            <img src="{image_url}" style="width: 100%; height: 170px; object-fit: cover;" />
            <div style="padding: 15px; direction: rtl;">
                <div style="margin-bottom: 8px;">
                    <span style="background-color: #fef3c7; color: #b45309; padding: 4px 10px; border-radius: 999px; font-size: 12px; margin-left: 5px;">{type_}</span>
                    <span style="background-color: #e0f2fe; color: #0369a1; padding: 4px 10px; border-radius: 999px; font-size: 12px; margin-left: 5px;">{audience}</span>
                    <span style="color: green; font-size: 13px;">● {status}</span>
                </div>
                <h4 style="margin: 0 0 10px 0; font-weight: 600;">{title}</h4>
                <div style="font-size: 13px; color: #6b7280;">
                    يبدأ من <strong>{formatted_date}</strong> — المدة <strong>{duration}</strong>
                </div>
            </div>
        </a>
    </div>
    """
    return html



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

col1, col2, col3 = st.columns([6, 3, 2])
with col2:
    st.markdown('<p style="font-size:20px; color:#2F195F; font-weight:bold; text-align:right;">رفع ملف PDF</p>', unsafe_allow_html=True)
    uploaded_file = st.file_uploader("", type="pdf", label_visibility="collapsed")
    if uploaded_file is not None:
            with st.spinner('جاري معالجة الملف...'):
                # Get the file content
                pdf_content = uploaded_file.getvalue()

                # Check if this file has been processed before (for UI feedback only)
                file_hash = hashlib.md5(pdf_content).hexdigest()
                if 'last_processed_hash' in st.session_state and st.session_state.last_processed_hash == file_hash:
                    st.session_state.cache_hit = True
                else:
                    st.session_state.cache_hit = False
                    st.session_state.last_processed_hash = file_hash

                try:
                    # Extract text from the PDF using the cached function
                    extracted_text = extract_text_from_resume(pdf_content)
                    cv= extracted_text
                    st.session_state.extracted_text = extracted_text

                    if st.session_state.cache_hit:
                        st.success('تم استخراج النص من الذاكرة المؤقتة!')
                    else:
                        st.success('تم استخراج النص بنجاح!')
                except Exception as e:
                    st.error(f'حدث خطأ أثناء معالجة الملف: {str(e)}')

with col3:

    st.markdown('<p style="font-size:20px; color:#2F195F; font-weight:bold; text-align:right;">اختر نوع الاقتراح</p>', unsafe_allow_html=True)
    option = st.selectbox("", ["اختر", "طور مهاراتك في مجالك", "غير مسارك"])



# Add full-width layout CSS first
    st.markdown("""
    <style>
        /* Make Streamlit use full width */
        .block-container {
            max-width: 100% !important;
            padding-top: 1rem;
            padding-right: 1rem;
            padding-left: 1rem;
            padding-bottom: 1rem;
        }
        /* Make the header also use full width */
        header {
            max-width: 100% !important;
        }
        /* Fix content areas */
        .css-18e3th9, .css-1d391kg {
            padding-left: 1rem;
            padding-right: 1rem;
        }
        /* Add some space between columns */
        .stColumn > div {
            padding: 0 5px;
        }
        /* Add vertical space between cards */
        .course-card {
            margin-bottom: 20px;
            display: block;
        }
        /* Set background and text direction */
        .main {
            background-color: #f9fafb;
            direction: rtl;
        }
    </style>
    """, unsafe_allow_html=True)















    
if option and option != "اختر":
    # Sample courses
    courses = best_courses(cv)
        
    



    # # Page title
    # st.title("الدورات المتاحة")

    # Create three columns
    col1, col2, col3 = st.columns([1, 1, 1])

    # Initialize empty content for each column
    col1_content = ""
    col2_content = ""
    col3_content = ""

    # Add course cards to different columns in a loop
    for i, course in enumerate(courses):
        course_html = f"""<div class="course-card" style="margin-bottom: 20px;">{render_course_card_ar(course)}</div>"""
        
        # Determine which column to use based on index
        if i % 3 == 0:
            col1_content += course_html
        elif i % 3 == 1:
            col2_content += course_html
        else:
            col3_content += course_html

    # Display the content in each column
    with col1:
        st.markdown(col1_content, unsafe_allow_html=True)
        
    with col2:
        st.markdown(col2_content, unsafe_allow_html=True)
        
    with col3:
        st.markdown(col3_content, unsafe_allow_html=True)












    client.close()  # Properly close connection
    # Close the connection
    conn.close()


