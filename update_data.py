import json
import datetime
import os
import time
import google.generativeai as genai
import re

# 获取 API Key
GOOGLE_API_KEY = os.environ.get('GOOGLE_API_KEY')
genai.configure(api_key=GOOGLE_API_KEY)

def get_ai_analysis(category, photo_id):
    # 按照稳定性排序的模型列表
    models_to_try = ['gemini-pro', 'gemini-1.5-flash', 'gemini-1.0-pro']
    
    prompt = f"""
    分析【{category}】领域标杆图片 (ID: {photo_id})。
    请以客观理性的视觉专家身份，从设计逻辑、视觉锚点、材质细节、批判性提升四个维度拆解。
    输出必须是纯 JSON，包含：id, category, imageUrl, title, brief, detailedAnalysis, suggestion。
    imageUrl统一使用: https://i0.wp.com/images.unsplash.com/photo-{photo_id}?w=1000&q=80
    """

    for model_name in models_to_try:
        try:
            print(f"正在尝试模型: {model_name}...")
            model = genai.GenerativeModel(model_name)
            response = model.generate_content(prompt)
            # 提取 JSON 块
            match = re.search(r'\{.*\}', response.text, re.DOTALL)
            if match:
                return json.loads(match.group())
        except Exception as e:
            print(f"模型 {model_name} 失败: {e}")
            continue
    return None

def update():
    # 锁定 12 张核心大片，确保 Fashion, Layout, Home Decor 都有货
    ids_map = {
        "女性穿搭": ["1485230895905-efd5b757fb45", "1550614000-4b95d4662d59", "1539106723-b7ad4176adad", "1434389678232-04e21dca1ef3"],
        "页面排版": ["1503694978374-8a2fa686963a", "1586075010923-2dd4570fb338", "1611162617474-5b21e879e113", "1561070791-2526d30994b5"],
        "家居装饰": ["1600210492486-724fe5c67fb0", "1618221195710-dd6b41faaea6", "1586023492125-27b2c045efd7", "1505691938895-1758d7feb511"]
    }
    
    results = []
    for cat, pids in ids_map.items():
        for pid in pids:
            data = get_ai_analysis(cat, pid)
            if data:
                results.append(data)
                print(f"✅ 成功录入: {data['title']}")
            time.sleep(2) # 避开频率限制
            
    if results:
        with open('aesthetic_data.json', 'w', encoding='utf-8') as f:
            json.dump(results, f, ensure_ascii=False, indent=4)
        print(f"🎉 进货完成！共计 {len(results)} 条数据。")
    else:
        print("❌ 严重错误：未能获取任何数据，请检查 API Key。")

if __name__ == "__main__":
    update()
