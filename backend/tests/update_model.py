import os, sys
sys.path.insert(0, r'D:\Heritage_Intelligence_Platform\trendforge-ai\backend')
os.chdir(r'D:\Heritage_Intelligence_Platform\trendforge-ai\backend')
from dotenv import load_dotenv
load_dotenv(dotenv_path=r'D:\Heritage_Intelligence_Platform\trendforge-ai\backend\.env', override=True)

path = r'D:\Heritage_Intelligence_Platform\trendforge-ai\backend\.env'
with open(path, 'r', encoding='utf-8') as f:
    content = f.read()
content = content.replace('GEMINI_MODEL=gemini-3.1-flash-lite-preview', 'GEMINI_MODEL=gemini-3.1-flash-lite')
with open(path, 'w', encoding='utf-8') as f:
    f.write(content)
print('Updated .env GEMINI_MODEL to gemini-3.1-flash-lite')
