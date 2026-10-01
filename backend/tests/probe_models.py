import os, sys
sys.path.insert(0, r'D:\Heritage_Intelligence_Platform\trendforge-ai\backend')
os.chdir(r'D:\Heritage_Intelligence_Platform\trendforge-ai\backend')
from dotenv import load_dotenv
load_dotenv(dotenv_path=r'D:\Heritage_Intelligence_Platform\trendforge-ai\backend\.env', override=True)
from google import genai

client = genai.Client(api_key=os.environ['GEMINI_API_KEY'])
candidates = [
    'gemini-3.1-flash-lite-preview',
    'gemini-2.5-flash-lite',
    'gemini-3.1-flash-lite',
    'gemini-flash-lite-latest',
    'gemini-2.5-flash',
    'gemini-3-flash-preview',
]
for m in candidates:
    try:
        r = client.models.generate_content(model=m, contents='Reply with OK only')
        print('OK:' + m + ' -> ' + r.text[:20].strip())
    except Exception as e:
        print('FAIL:' + m + ' -> ' + str(e)[:80])
