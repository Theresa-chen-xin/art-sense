import json
import os
import time
import google.generativeai as genai
import re

GOOGLE_API_KEY = os.environ.get('GOOGLE_API_KEY')
genai.configure(api_key=GOOGLE_API_KEY)

def fetch_pedagogical_data(category, photo_id):
    for model_name in ['gemini-1.5-flash-latest', 'gemini-pro']:
        try:
            model = genai.GenerativeModel(model_name)
            # 💡 核心修改：强制AI使用保姆级带教格式
            prompt = f"""
            你是一位专门教新手提升审美的实战导师。
            请拆解【{category}】领域的标杆图片(ID:{photo_id})。
            严禁使用干瘪的学术词汇！必须用大白话，像拆解公式一样告诉小白怎么看、怎么学。
            
            必须输出纯 JSON，格式如下：
            {{
                "id": "pro_{photo_id}",
                "category": "{category}",
                "imageUrl": "https://images.unsplash.com/photo-{photo_id}?w=1000&q=80",
                "title": "（起一个像小红书爆款的干货标题）",
                "brief": "（一句话总结这张图的万能公式）",
                "detailedAnalysis": "<p><b>🎯 视觉抓手（第一眼看哪）：</b><br>（解释这张图最吸引人的点）</p><br><p><b>📐 解构高级感（为什么好看）：</b><br>（拆解它的色彩搭配、光影或排版规律）</p><br><p><b>💡 新手实操（你怎么抄）：</b><br>（如果小白自己实操，直接可以套用的3个步骤）</p>"
            }}
            """
            response = model.generate_content(prompt)
            match = re.search(r'\{.*\}', response.text, re.DOTALL)
            if match: return json.loads(match.group())
        except: continue
    return None

def update():
    ids_map = {
        "女性穿搭": ["1485230895905-efd5b757fb45", "1550614000-4b95d4662d59", "1539106723-b7ad4176adad", "1434389678232-04e21dca1ef3"],
        "页面排版": ["1503694978374-8a2fa686963a", "1586075010923-2dd4570fb338", "1611162617474-5b21e879e113", "1561070791-2526d30994b5"],
        "家居装饰": ["1600210492486-724fe5c67fb0", "1618221195710-dd6b41faaea6", "1586023492125-27b2c045efd7", "1505691938895-1758d7feb511"]
    }
    
    results = []
    print("🚀 审美导师系统：正在生成保姆级拆解教程...")
    
    for cat, pids in ids_map.items():
        for pid in pids:
            data = fetch_pedagogical_data(cat, pid)
            if data:
                results.append(data)
                print(f"✅ 生成教程: {data['title']}")
                time.sleep(2) 
            
    if results:
        with open('aesthetic_data.json', 'w', encoding='utf-8') as f:
            json.dump(results, f, ensure_ascii=False, indent=4)

if __name__ == "__main__":
    update()
