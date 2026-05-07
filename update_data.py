import json
import requests
import datetime
import os
import time
import google.generativeai as genai

GOOGLE_API_KEY = os.environ.get('GOOGLE_API_KEY')
genai.configure(api_key=GOOGLE_API_KEY)
model = genai.GenerativeModel('gemini-pro')

def analyze_pro(category, photo_id):
    timestamp = datetime.datetime.now().strftime("%H%M%S")
    prompt = f"""
    Role: 你是一位拥有 20 年经验的、任职于国际顶尖艺术学院的视觉分析专家，风格‘客观且理性’。
    Task: 分析今日关于【{category}】领域的视觉标杆（图片ID: {photo_id}）。
    
    分析要求：
    1. 抛弃肤浅的赞美，从视觉分层、构图黄金分割、色彩对比度、材质质感、光线流动方向进行技术性拆解。
    2. 使用高信息密度的专业术语（如：负空间、色温平衡、肌理对比、视觉锚点）。
    
    输出格式（必须严格执行）：
    {{
        "id": "item_{photo_id}_{timestamp}",
        "category": "{category}",
        "imageUrl": "https://i0.wp.com/images.unsplash.com/photo-{photo_id}?w=800&q=80",
        "title": "专业视角下的审美趋势标题",
        "brief": "一句话概括其核心视觉价值",
        "detailedAnalysis": "四点深度技术拆解，用.<br>分割",
        "suggestion": "给专业人士的实战建议"
    }}
    """
    try:
        response = model.generate_content(prompt)
        # 清洗可能存在的 Markdown 格式
        clean_text = response.text.replace('```json', '').replace('```', '').strip()
        return json.loads(clean_text)
    except:
        return None

def update():
    stable_ids = {
        "女性穿搭": ["1485230895905-efd5b757fb45", "1550614000-4b95d4662d59", "1539106723-b7ad4176adad", "1434389678232-04e21dca1ef3"],
        "页面排版": ["1503694978374-8a2fa686963a", "1586075010923-2dd4570fb338", "1611162617474-5b21e879e113", "1561070791-2526d30994b5"],
        "家居装饰": ["1600210492486-724fe5c67fb0", "1618221195710-dd6b41faaea6", "1586023492125-27b2c045efd7", "1505691938895-1758d7feb511"]
    }
    
    results = []
    for cat, ids in stable_ids.items():
        for pid in ids:
            print(f"正在深度拆解: {cat} - {pid}")
            data = analyze_pro(cat, pid)
            if data: results.append(data)
            time.sleep(1) # 频率限制
            
    with open('aesthetic_data.json', 'w', encoding='utf-8') as f:
        json.dump(results, f, ensure_ascii=False, indent=4)

if __name__ == "__main__":
    update()
