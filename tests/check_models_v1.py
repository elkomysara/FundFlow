import google.generativeai as genai

api_key = "AIzaSyCbPZ29ijBiAebd-ChRvkds2suYV3xblW8"

try:
    genai.configure(api_key=api_key)
    print("✅ API Key is valid. Available models:")
    for m in genai.list_models():
        if 'generateContent' in m.supported_generation_methods:
            print(f"  - {m.name}")
except Exception as e:
    print(f"❌ Error: {e}")
