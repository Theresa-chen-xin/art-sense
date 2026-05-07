import json
import datetime
import os
import time
import google.generativeai as genai
import re

# 1. 钥匙配置
GOOGLE_API_KEY = os.environ.get('GOOGLE_API_KEY')
genai.configure(api_key=GOOGLE_API_KEY)

def fetch_ai_data(category, photo_id):
    # 按照优先级尝试 AI 接口
    for model_name in ['gemini-1.5-flash-latest', 'gemini-pro']:
        try:
            model = genai.GenerativeModel(model_name)
            # 强化 Prompt：追求学术精密度，剔除商业建议
            prompt = f"""
            你是一位拥有30年资历的顶级视觉艺术策展人。
            请对【{category}】领域作品(ID:{photo_id})进行深度学术拆解。
            
            要求：
            1. 语气必须客观、理性、专业。
            2. 使用艺术史或设计学专业术语。
            3. 拆解维度：底层构图逻辑、色彩动力学、材质叙事、视觉锚点。
            4. 字数要求：不少于 300 字，信息密度极高。
            
            输出纯 JSON：
            {{
                "id": "pro_{photo_id}",
                "category": "{category}",
                "imageUrl": "https://i0.wp.com/images.unsplash.com/photo-{photo_id}?w=1200&q=90",
                "title": "（学术级标题）",
                "brief": "（核心审美逻辑总结）",
                "detailedAnalysis": "（详细、专业、深度的四段式拆解，每段用.<br><br>分割）"
            }}
            """
            response = model.generate_content(prompt)
            match = re.search(r'\{.*\}', response.text, re.DOTALL)
            if match: return json.loads(match.group())
        except: continue
    return None

def update():
    ids_map = {
        "女性穿搭": ["1485230895905-efd5b757fb45", "1550614000-4b95d4662d59", "1539106723-b7ad4176adad", "1434389678232-04e21dca1ef3", "1529139574466-a303027c1d8b", "1515886657613-9f3515b0c78f", "1469334031218-e382a71b716b", "1532453288672-3a27e9be9efd"],
        "页面排版": ["1503694978374-8a2fa686963a", "1586075010923-2dd4570fb338", "1611162617474-5b21e879e113", "1561070791-2526d30994b5", "1541462608143-67571c6738dd", "1499951360447-b19be8fe80f5", "1512295767273-ac109cb3a5f6", "1626785774573-4b799315345d"],
        "家居装饰": ["1600210492486-724fe5c67fb0", "1618221195710-dd6b41faaea6", "1586023492125-27b2c045efd7", "1505691938895-1758d7feb511", "1554995207-c18c203602cb", "1616486338812-3dadae4b4ace", "1631679706909-1844bbd07221", "1522708323590-d24dbb6b0267"]
    }
    
    results = []
    print("🚀 审美寻猎机器人：正在进行深度学术拆解...")
    
    for cat, pids in ids_map.items():
        for i, pid in enumerate(pids):
            data = fetch_ai_data(cat, pid)
            if data:
                results.append(data)
                print(f"✅ 深度录入: {data['title']}")
                time.sleep(2) 
            
    if results:
        with open('aesthetic_data.json', 'w', encoding='utf-8') as f:
            json.dump(results, f, ensure_ascii=False, indent=4)

if __name__ == "__main__":
    update()
