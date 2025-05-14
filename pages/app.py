
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
# COLLECTION_NAME = "COMBINE_BP2"

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
    
from weaviate.classes.query import Filter

def search_similar_bootcamps_other(query, field ,limit=5):
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
            filters=Filter.by_property("initiativeScopeName_en").not_equal(field),
            return_properties=["title","title_en","initiativeCategoryName","initiativeCategoryName_en","initiativeScopeName","initiativeScopeName_en" ,"content", "language", "location","isRegistrationOpen","registrationEndDate", "startDate","endDate","index","slug","initiativeAgeName"]
        )
        
        # print(f"\n\n\n===================\n{results}\n\n\n===================\n")
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
    results = search_similar_bootcamps(query, limit=6)
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
    
import random
from datetime import datetime  # Ensure this is imported if not already

# List of image URLs
image_urls = [
    "https://cdn.tuwaiq.edu.sa/initiatives_admin/images/pfx1rhso.dml.webp",
    "https://cdn.tuwaiq.edu.sa/initiatives_admin/images/jfbxz4lr.rek.webp",
    "https://cdn.tuwaiq.edu.sa/initiatives_admin/images/5izndcsu.hvs.webp",
    "https://cdn.tuwaiq.edu.sa/initiatives_admin/images/ybag2hv2.tuc.webp",
    "https://cdn.tuwaiq.edu.sa/initiatives_admin/images/0jf412u1.myl.webp",
    "https://cdn.tuwaiq.edu.sa/initiatives_admin/images/rlknjzz4.y5e.webp",
    "https://cdn.tuwaiq.edu.sa/initiatives_admin/images/2kcemtrl.t3i.webp",
    "https://cdn.tuwaiq.edu.sa/initiatives_admin/images/4luucy2v.510.webp",
    "https://cdn.tuwaiq.edu.sa/initiatives_admin/images/xeo0f3sd.wui.webp",
    "https://cdn.tuwaiq.edu.sa/initiatives_admin/images/ib0dwcjx.anq.webp",
    "https://cdn.tuwaiq.edu.sa/initiatives_admin/images/w002n5nl.ltb.webp",
    "https://cdn.tuwaiq.edu.sa/initiatives_admin/images/2pwnnfhv.qzt.webp"
]

def render_course_card_ar(course):
    title = course.get("title", "—")
    image_url = random.choice(image_urls)
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
st.set_page_config(layout="wide", page_title="اقتراح مسارات", initial_sidebar_state="collapsed")

st.markdown('<div style="height: 60px; "></div>', unsafe_allow_html=True) 

import base64

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

def split_courses(cv):
     # Sample courses
    courses = best_courses(cv)
    enhance=[]
 
    major=""
    for i,item in enumerate(courses):
        if i==0:
            major =item["initiativeScopeName_en"].strip().lower()
        if i <= 5:
            enhance.append(item)
    # titles=[]
    # for items in data:
    #     if items["initiativeScopeName_en"].strip().lower() != major.strip().lower():
    #         titles.append(items["title_en"])

    # print(f"\n\n\n\n==========================================titles:\n{titles}\n\n\n=====\n\n")
    other = results_json(search_similar_bootcamps_other(cv, major,limit=6 ))
    
    client.close()  # Properly close connection
    # Close the connection
    conn.close()
    return enhance,other            


col1, col2, col3 = st.columns([6, 3, 2])
with col2:
    st.markdown('<p style="font-size:20px; color:#2F195F; font-weight:bold; text-align:right;"> قم برفع سيرتك الذاتية</p>', unsafe_allow_html=True)
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
                    if 'enhance' not in st.session_state or 'other' not in st.session_state:
                        enhance, other = split_courses(cv)
                        st.session_state.enhance = enhance
                        st.session_state.other = other

                    # Now you can access the cached values
                    enhance = st.session_state.enhance
                    other = st.session_state.other

                    
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



    
# Check if an option is selected AND the CV is not uploaded
if option != "اختر" and 'extracted_text' not in st.session_state:
    st.markdown("""
        <style>
            .centered-warning {
                display: flex;
                justify-content: center;
                align-items: center;
                font-size: 18px;
                color: #ff4b4b;
                font-weight: bold;
                text-align: center;
                height: 50px;
            }
        </style>
        <div class="centered-warning">يرجى رفع السيرة الذاتية أولاً قبل اختيار نوع الاقتراح.</div>
    """, unsafe_allow_html=True)
else:
    if option and option != "اختر" and 'extracted_text' in st.session_state and option == "طور مهاراتك في مجالك":
        cv = st.session_state.extracted_text
        courses = best_courses(cv)

        col1, col2, col3 = st.columns([1, 1, 1])
        col1_content = ""
        col2_content = ""
        col3_content = ""

            
        # Add course cards to different columns in a loop
        for i, course in enumerate(enhance):
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

    if option and option != "اختر" and 'extracted_text' in st.session_state and option == "غير مسارك":

            
        # # Page title
        # st.title("الدورات المتاحة")

        # Create three columns
        col1, col2, col3 = st.columns([1, 1, 1])

        # Initialize empty content for each column
        col1_content = ""
        col2_content = ""
        col3_content = ""

        # Add course cards to different columns in a loop
        for i, course in enumerate(other):
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

