
from dotenv import load_dotenv
import requests
import json
import os
i=1
all_bootcamps = []
all_programs = []
load_dotenv()
cookie = os.getenv("COOKIE")
verification= os.getenv("REQUEST_VERIFICATION_TOKEN")
user =os.getenv("USER_AGENT")
# print(f"\n\n {cookie}\n\n {verification}\n\n {user}")
selected_fields = [
        'title', 'description', 'startDate', 'endDate', 'isRegistrationOpen', 
        'isRegistrationClosed', 'language', 'video', 'initiativeAgeName',
        'initiativeCategoryName', 'locationName',
        'initiativeScopeName', 'goals',
        'features', 'requirements', 'faqs', 'initiativeProCertificate', 'slug', 'registrationEndDate', 'minimumAge',
        'maximumAge', 'locationText', 'startDateText', 'endDateText',
        'startTimeText', 'endTimeText', 'durationText'
    ]
while i <=4:
    url = f"https://tuwaiq.edu.sa/api/GetInitiativePublishesShorten/9/{i}"
    params1 = {
        "category": "ac41152d-f228-8af4-8406-e0cda6df6c35",
        "type": "NORMAL"
    }
    params2 = {
        "category": "8836bde0-68ae-3600-92a2-23dce3c487ca",
        "type": "NORMAL"
    }

    headers1 = {
        "accept": "application/json, text/plain, */*",
        "accept-language": "ar-AE,ar;q=0.9,en-US;q=0.8,en;q=0.7",
        "cookie": cookie,
        "referer": "https://tuwaiq.edu.sa/bootcamps",
        "requestverificationtoken": verification,
        "sec-ch-ua": '"Google Chrome";v="135", "Not-A.Brand";v="8", "Chromium";v="135"',
        "sec-ch-ua-mobile": "?0",
        "sec-ch-ua-platform": '"Windows"',
        "sec-fetch-dest": "empty",
        "sec-fetch-mode": "cors",
        "sec-fetch-site": "same-origin",
        "user-agent": user
    }
    headers2 = {
        "accept": "application/json, text/plain, */*",
        "accept-language": "ar-AE,ar;q=0.9,en-US;q=0.8,en;q=0.7",
        "cookie": cookie,
        "referer": "https://tuwaiq.edu.sa/bootcamps",
        "requestverificationtoken": verification,
        "sec-ch-ua": '"Google Chrome";v="135", "Not-A.Brand";v="8", "Chromium";v="135"',
        "sec-ch-ua-mobile": "?0",
        "sec-ch-ua-platform": '"Windows"',
        "sec-fetch-dest": "empty",
        "sec-fetch-mode": "cors",
        "sec-fetch-site": "same-origin",
        "user-agent": user
    }

    # Remove accept-encoding or let requests handle it automatically
    response_bootcamp = requests.get(url, params=params1, headers=headers1)
    response_programs = requests.get(url, params=params2, headers=headers2)

    # print(f"Status Code: {response.status_code}")
    # print("Response:")
    # print(response.text)
    
    
    if response_bootcamp.status_code == 200 and response_programs.status_code == 200:
        try:
            data1 = response_bootcamp.json()
            data2 = response_programs.json()
            # print(f"\n\n====={data}\n\n=====")
        except ValueError:
            print("Could not decode JSON, response text:")
            print(response_bootcamp.text)
            print(response_programs.text)
            exit()
        
        for item1,item2 in zip(data1["data"], data2["data"]):
            # print(f"\nITEM:\n==={item}\n\n===")
            # print(f"\nITEM:\n==={item}\n\n===")
            slug1 = item1["slug"]
            slug2 = item2["slug"]
            print(f"\n\nFetching details for slug: {slug1}\n\n")
            print(f"\n\nFetching details for slug: {slug2}\n\n")
            
            # Step 2: Use the slug to fetch detailed data
            detail_url1 = f"https://tuwaiq.edu.sa/api/GetInitiativePublishBySlug/{slug1}"
            detail_url2 = f"https://tuwaiq.edu.sa/api/GetInitiativePublishBySlug/{slug2}"
            
            # Optionally update referer if it's slug-specific
            headers1["referer"] = f"https://tuwaiq.edu.sa/bootcamp/{slug1}/view"
            headers2["referer"] = f"https://tuwaiq.edu.sa/bootcamp/{slug2}/view"
            
            detail_response1 = requests.get(detail_url1, headers=headers1)
            detail_response2 = requests.get(detail_url2, headers=headers2)
            # bootcamps
            if detail_response1.status_code == 200:
                try:
                    detailed_data = detail_response1.json()
                    # Create filtered dictionary with only the selected fields
                    print(detailed_data)
                    if detailed_data.get('isRegistrationOpen', False):
                        filtered_data = {
                            field: detailed_data.get(field) 
                            for field in selected_fields 
                            if field in detailed_data
                        }
                        all_bootcamps.append(filtered_data)
                    else:
                        print(f"Skipping {slug1} - registration closed")
                except ValueError:
                    print(f"Could not decode JSON for slug: {slug1}")
                    print("Response text:")
                    print(detail_response1.text)

            # programs
            if detail_response1.status_code == 200:
                try:
                    detailed_data = detail_response2.json()
                    # Create filtered dictionary with only the selected fields
                    if detailed_data.get('isRegistrationOpen', False):
                        filtered_data = {
                            field: detailed_data.get(field) 
                            for field in selected_fields 
                            if field in detailed_data
                        }
                        all_programs.append(filtered_data)
                    else:
                        print(f"Skipping {slug2} - registration closed")
                except ValueError:
                    print(f"Could not decode JSON for slug: {slug2}")
                    print("Response text:")
                    print(detail_response2.text)
                    
                # print(f"\n\nResponse\n{detailed_data}\n\n=========")
                

            else:
                print(f"Failed to fetch details for slug {slug1} or {slug2}")
                break
        
    # Write the collected data to a text file
        with open('bootcamps_data_api.json', 'w', encoding='utf-8') as f:
            # Using json.dumps for pretty formatting with 2-space indentation
            f.write(json.dumps(all_bootcamps, ensure_ascii=False, indent=2))
        with open('programs_data_api.json', 'w', encoding='utf-8') as f:
            # Using json.dumps for pretty formatting with 2-space indentation
            f.write(json.dumps(all_programs, ensure_ascii=False, indent=2))

    else:
        print("Failed to retrieve list data.")
    
    i= i+1
