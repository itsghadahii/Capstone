import json
import weaviate
from sentence_transformers import SentenceTransformer
from langchain_huggingface import HuggingFaceEmbeddings  # Updated import
from uuid import uuid4
import os
from weaviate.collections.classes.config import DataType

# Best practice: store your credentials in environment variables
weaviate_url = os.environ["WEAVIATE_URL"]
weaviate_api_key = os.environ["WEAVIATE_API_KEY"]
# COLLECTION_NAME = "Bootcamp_en"
# COLLECTION_NAME = "Bootcamp"
COLLECTION_NAME = "COMBINE_BP"

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
            return_properties=["title","title_en","initiativeCategoryName_en", "content", "language", "location", "startDate","index","slug"]
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






















# save_weaviate()
# save_weaviate_combine()




# Example queries
example_queries = [
    """Name: Ameen Alrashid
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
Available upon request""",
    # "تطوير تطبيقات الويب",  # Web application development
    # "الذكاء الاصطناعي",     # Artificial intelligence
    # "تعلم الآلة",          # Machine learning
    # "تطوير تطبيقات الجوال", # Mobile app development
    # "سايبر سكيورتي"        # Cybersecurity
]

# Run searches for each example query
for query in example_queries:
    print(f"\n\n===== Searching for: '{query}' =====")
    results = search_similar_bootcamps(query, limit=5)
    print_search_results(results)









client.close()  # Properly close connection