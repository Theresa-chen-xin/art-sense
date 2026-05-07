import json
import datetime
import os
import time
import google.generativeai as genai
import re

# 配置 API Key
GOOGLE_API_KEY = os.environ.get('GOOGLE_API_KEY')
genai.configure(api_key=GOOGLE_API_KEY)

def fetch_with_fallback(prompt):
    """三级保底：确保总能有一个模型给咱们干活"""
    models = ['gemini-1.5-flash', 'gemini-pro', 'gemini-1.0-pro']
    for model_name in models:
        try:
            print(f"正在尝试使用模型: {model_name}")
            model = genai.GenerativeModel(model_name)
            response = model.generate_content(prompt)
            return response.text
        except Exception as e:
            print(f"模型 {model_name} 暂不可用: {e}")
            continue
    return None

def analyze_pro(category, photo_id):
    prompt = f"""
    分析【{category}】领域的视觉标杆图片(ID: {photo_id})。
    请以客观理性的视觉专家身份，从设计逻辑、视觉锚点、材质细节、批判性提升四个维度拆解。
    必须返回纯 JSON，包含：id, category, imageUrl, title, brief, detailedAnalysis, suggestion。
    imageUrl统一使用: https://i0.wp.com/images.unsplash.com/photo-{photo_id}?w=1000&q=80
    """
    
    raw_text = fetch_with_fallback(prompt)
    if not raw_text: return None
    
    try:
        # 强力清洗：只提取 { } 之间的内容
        match = re.search(r'\{.*\}', raw_text, re.DOTALL)
        if match:
            return json.loads(match.group())
    except Exception as e:
        print(f"解析 AI 结果出错: {e}")
    return None

def update():
    # 锁定 12 张顶级审美 ID
    ids_map = {
        "女性穿搭": ["1485230895905-efd5b757fb45", "1550614000-4b95d4662d59", "1539106723-b7ad4176adad", "1434389678232-04e21dca1ef3"],
        "页面排版": ["1503694978374-8a2fa686963a", "1586075010923-2dd4570fb338", "1611162617474-5b21e879e113", "1561070791-2526d30994b5"],
        "家居装饰": ["1600210492486-724fe5c67fb0", "1618221195710-dd6b41faaea6", "1586023492125-27b2c045efd7", "1505691938895-1758d7feb511"]
    }
    
    all_data = []
    print("🚀 审美进阶系统：开始深度寻猎...")
    
    for category, pids in ids_map.items():
        for pid in pids:
            data = analyze_pro(category, pid)
            if data:
                all_data.append(data)
                print(f"✅ 成功录入: {data['title']}")
            time.sleep(2) # 保护频率，防止被封
            
    if all_data:
        with open('aesthetic_data.json', 'w', encoding='utf-8') as f:
            json.dump(all_data, f, ensure_ascii=False, indent=4)
        print(f"🎉 货架补满！共录入 {len(all_data)} 条导师级拆解内容。")
    else:
        print("❌ 警告：所有模型均未能返回有效数据。")

if __name__ == "__main__":
    update()
