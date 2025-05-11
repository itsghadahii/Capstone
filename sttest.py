import json
import weaviate
from sentence_transformers import SentenceTransformer
from langchain_huggingface import HuggingFaceEmbeddings  # Updated import
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


cv="""Name: Ameen Alrashid
Email: ameen.alrashid@email.com
Phone: +966-5XXXXXXX
Location: Dammam, Saudi Arabia
LinkedIn: linkedin.com/in/ameenalrashid
GitHub: github.com/ameenalrashid

Professional Summary:
Cybersecurity analyst with a strong background in securing enterprise systems, performing risk assessments, and implementing defense strategies. Experienced in monitoring network activity, mitigating threats, and enhancing information security compliance. Passionate about protecting digital infrastructure and staying current with emerging security trends.

Education:
Bachelor of Science in Computer Science – Imam Abdulrahman Bin Faisal University
Graduation: May 2024

Certifications:
- CompTIA Security+
- Certified Ethical Hacker (CEH)
- IBM Cybersecurity Analyst Professional Certificate

Technical Skills:
- Security Tools: Snort, Nmap, Nessus, Splunk
- Languages: Python, PowerShell, JavaScript
- Networking: TCP/IP, DNS, VPN, NAT, OSI Model
- Platforms: Windows Server, Kali Linux, Ubuntu
- Practices: Penetration Testing, SIEM, Incident Response, Threat Hunting

Projects:
Web App Penetration Testing Simulation
- Identified and exploited OWASP Top 10 vulnerabilities in a test application
- Documented flaws and provided remediation strategies
- Demonstrated XSS, SQLi, and CSRF attacks in a live demo

Security Information and Event Management (SIEM) Dashboard
- Built custom SIEM dashboard using Splunk
- Created real-time alerts for unusual login patterns and port scans
- Reduced detection time for incidents by 40%

Experience:
Cybersecurity Intern – Aramco Cyber Defense Center
Jul 2023 – Sep 2023
- Conducted internal vulnerability scans and documented findings
- Analyzed phishing attempts and contributed to monthly threat reports
- Assisted in deploying endpoint detection and response (EDR) solutions

Languages:
- Arabic: Native
- English: Professional Proficiency

Interests:
- Capture the Flag (CTF) challenges
- Malware analysis
- Threat intelligence platforms

References:
Available upon request"""













import streamlit as st
from datetime import datetime

from datetime import datetime
from dateutil.parser import parse  # Handles timezones and complex formats

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
    image_url = "https://via.placeholder.com/400x200.png?text=Course+Image"
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

# Sample courses
courses = best_courses(cv)

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

# Page title
st.title("الدورات المتاحة")

# Create three columns
col1, col2, col3 = st.columns([1, 1, 1])

# Initialize empty content for each column
col1_content = ""
col2_content = ""
col3_content = ""

# Add course cards to different columns in a loop
for i, course in enumerate(courses):
    course_html = f"""
    <div class="course-card" style="margin-bottom: 20px;">
        {render_course_card_ar(course)}
    </div>
    """
    
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