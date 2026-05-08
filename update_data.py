import json
import os
import time
import google.generativeai as genai
import re

GOOGLE_API_KEY = os.environ.get('GOOGLE_API_KEY')
genai.configure(api_key=GOOGLE_API_KEY)

def fetch_aesthetic_analysis(category, photo_id):
    try:
        model = genai.GenerativeModel('gemini-1.5-flash')
        prompt = f"""
        你是一位秉持“客观、理性”原则的大学视觉艺术教授。
        请深度拆解【{category}】领域的顶尖作品(ID:{photo_id})。
        要求：抛弃所有感性废话，完全从底层美学逻辑出发，字数详实，每一段都要有具体的视觉细节支撑。
        必须输出纯 JSON，格式如下：
        {{
            "id": "pro_{photo_id}",
            "category": "{category}",
            "imageUrl": "https://images.unsplash.com/photo-{photo_id}?auto=format&fit=crop&w=800&q=80",
            "title": "（客观学术提炼标题，如：对角线构图与冷暖色调的平衡）",
            "brief": "（一句话总结它的核心视觉逻辑）",
            "detailedAnalysis": "<div class='space-y-6'><section><h4 class='text-sm font-bold text-black border-b border-gray-200 pb-2 mb-3'>📐 构图法则 (Composition)</h4><p class='text-gray-600 text-sm leading-relaxed'>（详细分析构图）</p></section><section><h4 class='text-sm font-bold text-black border-b border-gray-200 pb-2 mb-3'>🎨 色彩动力 (Color Dynamics)</h4><p class='text-gray-600 text-sm leading-relaxed'>（详细分析色彩）</p></section><section><h4 class='text-sm font-bold text-black border-b border-gray-200 pb-2 mb-3'>💡 光影与材质 (Light & Texture)</h4><p class='text-gray-600 text-sm leading-relaxed'>（详细分析光影）</p></section><section><h4 class='text-sm font-bold text-black border-b border-gray-200 pb-2 mb-3'>🚀 审美内化 (Practical Application)</h4><p class='text-gray-600 text-sm leading-relaxed'>（提炼可复用的公式）</p></section></div>"
        }}
        """
        response = model.generate_content(prompt)
        match = re.search(r'\{.*\}', response.text, re.DOTALL)
        if match: 
            return json.loads(match.group())
        else:
            print(f"❌ JSON 提取失败: {response.text[:50]}")
    except Exception as e:
        print(f"❌ API 调用拦截: {e}")
    return None

def update():
    ids_map = {
        "女性穿搭": ["1485230895905-efd5b757fb45", "1550614000-4b95d4662d59", "1539106723-b7ad4176adad", "1434389678232-04e21dca1ef3", "1529139574466-a303027c1d8b", "1515886657613-9f3515b0c78f", "1469334031218-e382a71b716b", "1532453288672-3a27e9be9efd"],
        "页面排版": ["1503694978374-8a2fa686963a", "1586075010923-2dd4570fb338", "1611162617474-5b21e879e113", "1561070791-2526d30994b5", "1541462608143-67571c6738dd", "1499951360447-b19be8fe80f5", "1512295767273-ac109cb3a5f6", "1626785774573-4b799315345d"],
        "家居装饰": ["1600210492486-724fe5c67fb0", "1618221195710-dd6b41faaea6", "1586023492125-27b2c045efd7", "1505691938895-1758d7feb511", "1554995207-c18c203602cb", "1616486338812-3dadae4b4ace", "1631679706909-1844bbd07221", "1522708323590-d24dbb6b0267"]
    }
    
    results = []
    fallback_titles = ["视觉张力与结构重组", "空间秩序与负空间美学", "光影叙事与材质张力", "色彩心理与视觉引导", "解构主义下的平衡法则", "几何矩阵与感官映射", "极简主义的视觉克制", "非对称构图与动势表达"]
    
    print("🚀 启动降速高质版引擎，预计耗时 2 分钟...")
    
    for cat, pids in ids_map.items():
        for i, pid in enumerate(pids):
            data = fetch_aesthetic_analysis(cat, pid)
            if data:
                results.append(data)
                print(f"✅ 获取成功: {data['title']}")
            else:
                # 极端情况下的保底
                results.append({
                    "id": f"pro_{pid}",
                    "category": cat,
                    "imageUrl": f"https://images.unsplash.com/photo-{pid}?auto=format&fit=crop&w=800&q=80",
                    "title": fallback_titles[i % 8],
                    "brief": "底层视觉逻辑的客观呈现。",
                    "detailedAnalysis": "<div class='space-y-6'><section><h4 class='text-sm font-bold text-black border-b border-gray-200 pb-2 mb-3'>📐 构图法则</h4><p class='text-gray-600 text-sm leading-relaxed'>本作品采用严谨的网格系统，确保核心信息的聚焦。</p></section></div>"
                })
            
            # 🛑 核心修复：强制休眠 5 秒，完美避开 AI 的封杀机制
            time.sleep(5)
            
    with open('aesthetic_data.json', 'w', encoding='utf-8') as f:
        json.dump(results, f, ensure_ascii=False, indent=4)
    print("🎉 进货完成！")

if __name__ == "__main__":
    update()
