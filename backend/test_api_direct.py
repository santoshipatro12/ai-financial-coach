import os
from dotenv import load_dotenv

load_dotenv()

api_key = os.getenv('GOOGLE_API_KEY')

print("="*60)
print("🔍 TESTING GOOGLE API")
print("="*60)
print(f"API Key found: {bool(api_key)}")
if api_key:
    print(f"Key starts with: {api_key[:20]}")
    print(f"Key length: {len(api_key)}")
print("="*60)

# Test 1: Import package
try:
    import google.generativeai as genai
    print("✅ Package imported successfully")
except Exception as e:
    print(f"❌ Failed to import: {e}")
    exit()

# Test 2: Configure API
try:
    genai.configure(api_key=api_key)
    print("✅ API configured")
except Exception as e:
    print(f"❌ Configuration failed: {e}")
    exit()

# Test 3: List available models
try:
    print("\n📋 Available models:")
    for model in genai.list_models():
        if 'generateContent' in model.supported_generation_methods:
            print(f"   ✅ {model.name}")
except Exception as e:
    print(f"❌ Failed to list models: {e}")

# Test 4: Try different models
models_to_try = [
    'gemini-1.5-flash',
    'gemini-1.5-flash-latest',
    'gemini-1.5-pro',
    'gemini-1.0-pro',
    'models/gemini-1.5-flash',
    'models/gemini-pro'
]

print("\n🧪 Testing models:")
for model_name in models_to_try:
    try:
        model = genai.GenerativeModel(model_name)
        response = model.generate_content("Say hi")
        print(f"✅ {model_name}: {response.text[:50]}")
        print(f"\n🎉 SUCCESS! Use this model: {model_name}\n")
        break
    except Exception as e:
        print(f"❌ {model_name}: {str(e)[:80]}")

print("="*60)