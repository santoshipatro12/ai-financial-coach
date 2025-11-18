from config import Config

print("Testing Config...")
print(f"HOST: {Config.HOST}")
print(f"PORT: {Config.PORT}")
print(f"DEBUG: {Config.DEBUG}")
print(f"GOOGLE_API_KEY: {'Set' if Config.GOOGLE_API_KEY else 'NOT SET'}")
print(f"UPLOAD_FOLDER: {Config.UPLOAD_FOLDER}")