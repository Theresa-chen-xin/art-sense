import json
import os
import time
import google.generativeai as genai
import re

GOOGLE_API_KEY = os.environ.get('GOOGLE_API_KEY')
genai.configure(api_key=GOOGLE_API_KEY)

def fetch_aesthetic_analysis(category, photo_id):
    for model_name in ['gemini-1.5-flash-latest', 'gemini-pro']:
        try:
            model = genai.GenerativeModel(model_name)
            # 💡 核心升级：强制输出极其客观、理性的结构化美学分析
            prompt = f"""
            你是一位秉持“客观、理性”原则的大学视觉艺术教授。
            请向零基础小白深度拆解【{category}】领域的顶尖作品(ID:{photo_id})。
            
            要求：抛弃所有感性废话（如“太美了”、“绝绝子”），完全从底层美学逻辑出发，字数极度详实。
            
            必须输出纯 JSON，格式如下：
            {{
                "id": "pro_{photo_id}",
                "category": "{category}",
                "imageUrl": "https://images.unsplash.com/photo-{photo_id}?w=1000&q=80",
                "title": "（客观且学术的提炼标题，如：对角线构图与冷暖色调的平衡）",
                "brief": "（一句话总结它的核心视觉逻辑）",
                "detailedAnalysis": "<div class='space-y-6'><section><h4 class='text-sm font-bold text-black border-b border-gray-200 pb-2 mb-3'>📐 构图法则 (Composition)</h4><p class='text-gray-600 text-sm leading-relaxed'>（详细说明视线是如何被引导的，比例关系，负空间的使用等）</p></section><section><h4 class='text-sm font-bold text-black border-b border-gray-200 pb-2 mb-3'>🎨 色彩动力 (Color Dynamics)</h4><p class='text-gray-600 text-sm leading-relaxed'>（客观分析色相、明度、饱和度，互补色或同色系是如何影响视觉心理的）</p></section><section><h4 class='text-sm font-bold text-black border-b border-gray-200 pb-2 mb-3'>💡 光影与材质 (Light & Texture)</h4><p class='text-gray-600 text-sm leading-relaxed'>（分析光源方向，材质对比产生的视觉张力）</p></section><section><h4 class='text-sm font-bold text-black border-b border-gray-200 pb-2 mb-3'>🚀 审美内化 (Practical Application)</h4><p class='text-gray-600 text-sm leading-relaxed'>（普通人如何在日常排版、穿搭或拍摄中，提炼并套用该图的一个具体美学公式）</p></section></div>"
            }}
            """
            response = model.generate_content(prompt)
            match = re.search(r'\{.*\}', response.text, re.DOTALL)
            if match: return json.loads(match.group())
        except: continue
    return None

def update():
    # 这里放置了12张图用于快速测试。测试成功后你可以随意增加。
    ids_map = {
        "女性穿搭": ["1485230895905-efd5b757fb45", "1550614000-4b95d4662d59", "1539106723-b7ad4176adad", "1434389678232-04e21dca1ef3"],
        "页面排版": ["1503694978374-8a2fa686963a", "1586075010923-2dd4570fb338", "1611162617474-5b21e879e113", "1561070791-2526d30994b5"],
        "家居装饰": ["1600210492486-724fe5c67fb0", "1618221195710-dd6b41faaea6", "1586023492125-27b2c045efd7", "1505691938895-1758d7feb511"]
    }
    
    results = []
    print("🚀 启动学术级审美拆解引擎...")
    
    for cat, pids in ids_map.items():
        for pid in pids:
            data = fetch_aesthetic_analysis(cat, pid)
            if data:
                results.append(data)
                print(f"✅ 完成深度拆解: {data['title']}")
                time.sleep(2) 
            
    if results:
        with open('aesthetic_data.json', 'w', encoding='utf-8') as f:
            json.dump(results, f, ensure_ascii=False, indent=4)

if __name__ == "__main__":
    update()
