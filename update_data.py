import json
import datetime
import os
import time
import google.generativeai as genai
import re

# 从环境变量获取 API Key
GOOGLE_API_KEY = os.environ.get('GOOGLE_API_KEY')
genai.configure(api_key=GOOGLE_API_KEY)

def get_ai_response(prompt):
    """双模型备份机制：确保进货不走空"""
    # 尝试的模型列表，按优先级排序
    model_names = ['gemini-1.5-flash', 'gemini-pro']
    
    for name in model_names:
        try:
            model = genai.GenerativeModel(name)
            response = model.generate_content(prompt)
            return response.text
        except Exception as e:
            print(f"模型 {name} 尝试失败: {e}")
            continue
    return None

def analyze_pro(category, photo_id):
    timestamp = datetime.datetime.now().strftime("%H%M%S")
    prompt = f"""
    分析【{category}】领域图片 (ID: {photo_id})。
    作为顶级视觉专家，请从设计逻辑、视觉锚点、材质细节、批判性提升四个维度深度客观拆解。
    输出必须是纯 JSON，包含：id, category, imageUrl, title, brief, detailedAnalysis, suggestion。
    imageUrl: https://i0.wp.com/images.unsplash.com/photo-{photo_id}?w=1000&q=80
    """
    
    text = get_ai_response(prompt)
    if not text: return None
    
    try:
        # 正则提取 JSON 块，彻底解决格式问题
        match = re.search(r'\{.*\}', text, re.DOTALL)
        if match:
            return json.loads(match.group())
    except Exception as e:
        print(f"解析 JSON 出错: {e}")
    return None

def update():
    # 精选 12 张核心大片
    ids_map = {
        "女性穿搭": ["1485230895905-efd5b757fb45", "1550614000-4b95d4662d59", "1539106723-b7ad4176adad", "1434389678232-04e21dca1ef3"],
        "页面排版": ["1503694978374-8a2fa686963a", "1586075010923-2dd4570fb338", "1611162617474-5b21e879e113", "1561070791-2526d30994b5"],
        "家居装饰": ["1600210492486-724fe5c67fb0", "1618221195710-dd6b41faaea6", "1586023492125-27b2c045efd7", "1505691938895-1758d7feb511"]
    }
    
    results = []
    print("🚀 审美寻猎机器人启动...")
    
    for cat, pids in ids_map.items():
        for pid in pids:
            data = analyze_pro(cat, pid)
            if data:
                results.append(data)
                print(f"✅ 成功拆解: {data['title']}")
            time.sleep(2) # 保护 API 频率
            
    if results:
        with open('aesthetic_data.json', 'w', encoding='utf-8') as f:
            json.dump(results, f, ensure_ascii=False, indent=4)
        print(f"🎉 进货完毕，共计 {len(results)} 条导师级拆解！")
    else:
        print("❌ 警告：所有模型均未返回数据，请检查 API Key 权限。")

if __name__ == "__main__":
    update()
