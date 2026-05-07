import json
import requests
import datetime
import os
import time
import google.generativeai as genai

# 获取钥匙
GOOGLE_API_KEY = os.environ.get('GOOGLE_API_KEY')
genai.configure(api_key=GOOGLE_API_KEY)
# 使用更快速稳定的模型
model = genai.GenerativeModel('gemini-1.5-flash')

def analyze_pro(category, photo_id):
    timestamp = datetime.datetime.now().strftime("%H%M%S")
    prompt = f"""
    Role: 你是一位拥有20年经验的艺术学院教授，风格“绝对理性且客观”。
    Task: 深度拆解【{category}】领域的视觉标杆（图片ID: {photo_id}）。
    要求：从底层逻辑（Why）、视觉锚点（Where）、细节叙事、批判性提升四个维度进行拆解。禁止感性废话。
    输出JSON格式：
    {{
        "id": "pro_{photo_id}_{timestamp}",
        "category": "{category}",
        "imageUrl": "https://i0.wp.com/images.unsplash.com/photo-{photo_id}?w=1000&q=80",
        "title": "学术级标题",
        "brief": "视觉逻辑总结",
        "detailedAnalysis": "四点技术拆解，用.<br>分割",
        "suggestion": "小白实战建议"
    }}
    """
    try:
        response = model.generate_content(prompt)
        clean_text = response.text.replace('```json', '').replace('```', '').strip()
        return json.loads(clean_text)
    except:
        return None

def update():
    professional_ids = {
        "女性穿搭": ["1485230895905-efd5b757fb45", "1550614000-4b95d4662d59", "1539106723-b7ad4176adad", "1434389678232-04e21dca1ef3", "1529139574466-a303027c1d8b", "1515886657613-9f3515b0c78f", "1469334031218-e382a71b716b", "1532453288672-3a27e9be9efd"],
        "页面排版": ["1503694978374-8a2fa686963a", "1586075010923-2dd4570fb338", "1611162617474-5b21e879e113", "1561070791-2526d30994b5", "1541462608143-67571c6738dd", "1499951360447-b19be8fe80f5", "1512295767273-ac109cb3a5f6", "1626785774573-4b799315345d"],
        "家居装饰": ["1600210492486-724fe5c67fb0", "1618221195710-dd6b41faaea6", "1586023492125-27b2c045efd7", "1505691938895-1758d7feb511", "1554995207-c18c203602cb", "1616486338812-3dadae4b4ace", "1631679706909-1844bbd07221", "1522708323590-d24dbb6b0267"]
    }
    
    results = []
    for cat, ids in professional_ids.items():
        for pid in ids:
            print(f"深度拆解: {cat} - {pid}")
            data = analyze_pro(cat, pid)
            if data: 
                results.append(data)
                time.sleep(1) # 频率控制
            
    with open('aesthetic_data.json', 'w', encoding='utf-8') as f:
        json.dump(results, f, ensure_ascii=False, indent=4)

if __name__ == "__main__":
    update()
