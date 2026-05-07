import json
import datetime
import os
import time
import google.generativeai as genai

# 从系统环境获取钥匙
GOOGLE_API_KEY = os.environ.get('GOOGLE_API_KEY')
genai.configure(api_key=GOOGLE_API_KEY)
model = genai.GenerativeModel('gemini-1.5-flash')

def analyze_pro(category, photo_id):
    timestamp = datetime.datetime.now().strftime("%H%M%S")
    prompt = f"""
    Role: 视觉艺术教授。风格：客观理性。
    Task: 深度拆解【{category}】领域的视觉标杆（ID: {photo_id}）。
    要求：从底层逻辑、视觉锚点、细节叙事、批判性提升四个维度拆解。
    输出格式：JSON。
    """
    try:
        response = model.generate_content(prompt)
        clean_text = response.text.replace('```json', '').replace('```', '').strip()
        return json.loads(clean_text)
    except:
        return None

def update():
    ids_map = {
        "女性穿搭": ["1485230895905-efd5b757fb45", "1550614000-4b95d4662d59", "1539106723-b7ad4176adad", "1434389678232-04e21dca1ef3"],
        "页面排版": ["1503694978374-8a2fa686963a", "1586075010923-2dd4570fb338", "1611162617474-5b21e879e113", "1561070791-2526d30994b5"],
        "家居装饰": ["1600210492486-724fe5c67fb0", "1618221195710-dd6b41faaea6", "1586023492125-27b2c045efd7", "1505691938895-1758d7feb511"]
    }
    results = []
    for cat, ids in ids_map.items():
        for pid in ids:
            data = analyze_pro(cat, pid)
            if data: results.append(data)
            time.sleep(1)
            
    with open('aesthetic_data.json', 'w', encoding='utf-8') as f:
        json.dump(results, f, ensure_ascii=False, indent=4)

if __name__ == "__main__":
    update()
