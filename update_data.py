import json
import datetime
import os
import time
import google.generativeai as genai
import re

# 获取钥匙
GOOGLE_API_KEY = os.environ.get('GOOGLE_API_KEY')
genai.configure(api_key=GOOGLE_API_KEY)
# 使用更稳健的模型配置
model = genai.GenerativeModel('gemini-1.5-flash')

def analyze_pro(category, photo_id):
    timestamp = datetime.datetime.now().strftime("%H%M%S")
    # 强化 Prompt，强制要求纯 JSON
    prompt = f"""
    分析【{category}】领域图片 (ID: {photo_id})。
    请作为顶级视觉专家，从设计逻辑、视觉锚点、材质细节、批判性提升四个维度拆解。
    输出必须是一个纯 JSON 字符串，包含以下键：id, category, imageUrl, title, brief, detailedAnalysis, suggestion。
    imageUrl统一使用: https://i0.wp.com/images.unsplash.com/photo-{photo_id}?w=1000&q=80
    """
    
    try:
        response = model.generate_content(prompt)
        # 核心改进：使用正则提取 JSON 块，防止 AI 话多
        match = re.search(r'\{.*\}', response.text, re.DOTALL)
        if match:
            json_str = match.group()
            data = json.loads(json_str)
            return data
        else:
            print(f"警告：AI 回复格式不对 -> {response.text[:50]}...")
            return None
    except Exception as e:
        print(f"AI 分析出错 (ID: {photo_id}): {e}")
        return None

def update():
    # 锁定 12 张核心大片
    ids = {
        "女性穿搭": ["1485230895905-efd5b757fb45", "1550614000-4b95d4662d59", "1539106723-b7ad4176adad", "1434389678232-04e21dca1ef3"],
        "页面排版": ["1503694978374-8a2fa686963a", "1586075010923-2dd4570fb338", "1611162617474-5b21e879e113", "1561070791-2526d30994b5"],
        "家居装饰": ["1600210492486-724fe5c67fb0", "1618221195710-dd6b41faaea6", "1586023492125-27b2c045efd7", "1505691938895-1758d7feb511"]
    }
    
    results = []
    print("🚀 审美进阶系统：开始深度寻猎...")
    
    for cat, pids in ids.items():
        for pid in pids:
            data = analyze_pro(cat, pid)
            if data:
                results.append(data)
                print(f"✅ 已收录: {data['title']}")
            # 关键：每张图休息 2 秒，防止被 AI 封禁
            time.sleep(2) 
            
    if results:
        with open('aesthetic_data.json', 'w', encoding='utf-8') as f:
            json.dump(results, f, ensure_ascii=False, indent=4)
        print(f"🎉 成功补货 {len(results)} 条深度审美分析！")
    else:
        print("❌ 严重错误：未能获取任何有效数据，请检查 API Key 或网络。")

if __name__ == "__main__":
    update()
