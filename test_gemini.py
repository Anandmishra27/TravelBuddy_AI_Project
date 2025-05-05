import google.generativeai as genai
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

# Use the working model
model = genai.GenerativeModel("models/gemini-1.5-pro")

# Test content generation
try:
    response = model.generate_content("Give me 3 fun travel facts.")
    print("\n".join(response.text.split("\n")))
except Exception as e:
    print("ERROR:", e)