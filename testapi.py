from openai import OpenAI
import os
from dotenv import load_dotenv
load_dotenv()



client = OpenAI(
  api_key= os.environ["OPENAI_API_KEY"]
)

import sqlite3

# 1. Connect to the database (creates one if it doesn't exist)
conn = sqlite3.connect('resume_database.db')

# 2. Create a cursor object
cursor = conn.cursor()

# 3. Write your SELECT query
query = "SELECT extracted_text FROM resumes s WHERE s.id =11"
cursor.execute(query)  # parameterized to avoid SQL injection

# 4. Fetch results
rows = cursor.fetchall()
# print(f"\n\n\n========{rows}\n\n\n==========")
# 5. Print results
for row in rows:
    print(row[0])
    cv=row[0]

# 6. Close the connection
conn.close()


completion = client.chat.completions.create(
    model="gpt-4o-mini",
    messages=[
        {"role": "system", "content": "You will be given CVs/Resumes. Your task is to first extract the field and career level based on skills or education. Then, write a description that highlights **only missing skills, techniques, or areas of growth** that will help the user progress in their career. The description should focus on the **next step in their learning**, ensuring it is specific to the user’s career path and will help them advance. **DO NOT mention completed courses, certifications, or personal information (e.g., name, email, phone)**. Do not provide general career advice or narrative about their past experience. Only suggest skills, tools, or techniques they might need to learn or improve upon."},
        {"role": "user", "content": cv}
    ]
)

print(completion.choices[0].message)
