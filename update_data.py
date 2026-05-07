import json
import requests
import datetime
import os
import time
import google.generativeai as genai

GOOGLE_API_KEY = os.environ.get('GOOGLE_API_KEY')
genai.configure(api_key=GOOGLE_API_KEY)
# 使用更强的模型以获得更深度的分析
model = genai.GenerativeModel('gemini-1.5-flash')

def analyze_pro(category, photo_id):
    timestamp = datetime.datetime.now().strftime("%H%M%S")
    # --- 核心改进：极其严苛且专业的 Prompt ---
    prompt = f"""
    Role: 你是一位拥有 20 年经验的顶级视觉艺术评论家，风格‘绝对理性且客观’。
    Task: 分析【{category}】领域的全球视觉标杆（图片ID: {photo_id}）。
    
    你必须按照以下深度框架进行拆解，禁止使用“优美”、“高级”等感性词汇，必须使用设计工程学术语：
    
    1. 底层逻辑(The Why): 该作品好在哪？是利用了互补色的高频对比，还是采用了斐波那契螺旋线构图？
    2. 视觉锚点(The Where): 视觉的第一落点在哪？设计师利用了什么引导线（Leading Lines）或肌理对比（Texture Contrast）来吸引注意力？
    3. 细节叙事: 材质的漫反射、光影的冷暖交替、或者元素的留白比例（Negative Space）起到了什么作用？
    4. 批判性提升: 为了让审美更进一步，这个画面如果调整某个元素（如：增加暗部细节、改变字体克重、移动重心位置），会有什么质的飞跃？为什么？

    输出格式（必须严格执行 JSON，不要返回任何多余文字）：
    {{
        "id": "pro_{photo_id}_{timestamp}",
        "category": "{category}",
        "imageUrl": "https://i0.wp.com/images.unsplash.com/photo-{photo_id}?w=1000&q=90",
        "title": "（起一个具有学术气息的标题）",
        "brief": "（用设计法则总结核心视觉逻辑）",
        "detailedAnalysis": "（上述 4 点拆解，用.<br>连接成一段话。内容字数要求在 300 字左右，确保信息量极其致密）",
        "suggestion": "（给小白的实战避坑指南，说明为什么要这么做）"
    }}
    """
    try:
        response = model.generate_content(prompt)
        clean_text = response.text.replace('```json', '').replace('```', '').strip()
        return json.loads(clean_text)
    except:
        return None

def update():
    # 挑选了 12 张具有极高设计深度、非常耐拆解的图片 ID
    professional_ids = {{
        "女性穿搭": ["1485230895905-efd5b757fb45", "1550614000-4b95d4662d59", "1539106723-b7ad4176adad", "1434389678232-04e21dca1ef3"],
        "页面排版": ["1503694978374-8a2fa686963a", "1586075010923-2dd4570fb338", "1611162617474-5b21e879e113", "1561070791-2526d30994b5"],
        "家居装饰": ["1600210492486-724fe5c67fb0", "1618221195710-dd6b41faaea6", "1586023492125-27b2c045efd7", "1505691938895-1758d7feb511"]
    }}
    
    results = []
    for cat, ids in professional_ids.items():
        for pid in ids:
            print(f"正在进行深度导师级分析: {cat} - {pid}")
            data = analyze_pro(cat, pid)
            if data: results.append(data)
            time.sleep(2) # 增加延迟确保生成质量
            
    with open('aesthetic_data.json', 'w', encoding='utf-8') as f:
        json.dump(results, f, ensure_ascii=False, indent=4)

if __name__ == "__main__":
    update()
