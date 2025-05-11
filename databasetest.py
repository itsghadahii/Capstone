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

# 5. Print results
for row in rows:
    print(row)

# 6. Close the connection
conn.close()