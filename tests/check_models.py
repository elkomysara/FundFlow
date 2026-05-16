import google.generativeai as genai
from dotenv import load_dotenv
import os

load_dotenv()
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

print("🔍 Available Gemini models:")
try:
    for model in genai.list_models():
        if 'gemini' in model.name.lower():
            print(f"  ✅ {model.name}")
except Exception as e:
    print(f"❌ Error listing models: {e}")
