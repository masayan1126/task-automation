from dotenv import load_dotenv
import os

load_dotenv()


api_key = os.getenv("API_KEY")
print(api_key)
