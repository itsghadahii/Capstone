from openai import OpenAI
import os
from dotenv import load_dotenv
load_dotenv()
client = OpenAI(
  api_key= os.environ["OPENAI_API_KEY"]
)

completion = client.chat.completions.create(
  model="gpt-4o-mini",
  store=True,
  messages=[
    {"role": "user", "content": "hello i am faisal write me a story about me"}
  ]
)

print(completion.choices[0].message)