import json
import os
import time
import google.generativeai as genai
import re

GOOGLE_API_KEY = os.environ.get('GOOGLE_API_KEY')
genai.configure(api_key=GOOGLE_API_KEY)

def get_academic_fallback(category, photo_id, index):
    titles = [
        "视觉张力与结构重组", "空间秩序与负空间美学", "光影叙事与材质张力", "色彩心理与视觉引导", 
        "解构主义下的平衡法则", "几何矩阵与感官映射", "极简主义的视觉克制", "非对称构图与动势表达"
    ]
    return {
        "id": f"pro_{photo_id}",
        "category": category,
        # 💡 核心修改：彻底去掉代理，直连 Unsplash 高清原图
        "imageUrl": f"https://images.unsplash.com/photo-{photo_id}?auto=format&fit=crop&w=800&q=80",
        "title": titles[index % 8],
        "brief": "底层视觉逻辑与核心美学要素的客观呈现。",
        "detailedAnalysis": "<div class='space-y-6'><section><h4 class='text-sm font-bold text-black border-b border-gray-200 pb-2 mb-3'>📐 构图法则 (Composition)</h4><p class='text-gray-600 text-sm leading-relaxed'>本作品采用严谨的网格系统与视觉引导线，确保了核心信息的绝对聚焦。负空间的克制使用有效缓解了视觉压迫感，建立了稳定的空间秩序。</p></section><section><h4 class='text-sm font-bold text-black border-b border-gray-200 pb-2 mb-3'>🎨 色彩动力 (Color Dynamics)</h4><p class='text-gray-600 text-sm leading-relaxed'>通过低饱和度的主色调与高明度的局部点缀形成剧烈反差，建立起理性的色彩秩序与特定的心理暗示，避免了视觉上的冗余。</p></section><section><h4 class='text-sm font-bold text-black border-b border-gray-200 pb-2 mb-3'>💡 光影与材质 (Light & Texture)</h4><p class='text-gray-600 text-sm leading-relaxed'>光源的指向性极大地增强了材质表面的颗粒感与物理属性，硬朗与柔和材质的碰撞在单一平面内产生了极高的审美势能与触觉联想。</p></section><section><h4 class='text-sm font-bold text-black border-b border-gray-200 pb-2 mb-3'>🚀 审美内化 (Practical Application)</h4><p class='text-gray-600 text-sm leading-relaxed'>客观规律提炼：在日常实践中，可直接套用此“主次结构分明、克制色彩运用、强调材质反差”的逻辑公式，建立高级视觉标准。</p></section></div>"
    }

def fetch_aesthetic_analysis(category, photo_id, index):
    for model_name in ['gemini-1.5-flash', 'gemini-pro']:
        try:
            model = genai.GenerativeModel(model_name)
            prompt = f"""
            你是一位秉持“客观、理性”原则的大学视觉艺术教授。请深度拆解【{category}】领域的顶尖作品(ID:{photo_id})。
            要求：完全从底层美学逻辑出发，字数详实，严禁废话。
            必须输出纯 JSON，格式如下：
            {{
                "id": "pro_{photo_id}",
                "category": "{category}",
                "imageUrl": "https://images.unsplash.com/photo-{photo_id}?auto=format&fit=crop&w=800&q=80",
                "title": "（客观学术提炼标题）",
                "brief": "（一句话总结它的核心视觉逻辑）",
                "detailedAnalysis": "<div class='space-y-6'><section><h4 class='text-sm font-bold text-black border-b border-gray-200 pb-2 mb-3'>📐 构图法则 (Composition)</h4><p class='text-gray-600 text-sm leading-relaxed'>（详细说明视线是如何被引导的，比例关系，负空间的使用等）</p></section><section><h4 class='text-sm font-bold text-black border-b border-gray-200 pb-2 mb-3'>🎨 色彩动力 (Color Dynamics)</h4><p class='text-gray-600 text-sm leading-relaxed'>（客观分析色相、明度、饱和度等）</p></section><section><h4 class='text-sm font-bold text-black border-b border-gray-200 pb-2 mb-3'>💡 光影与材质 (Light & Texture)</h4><p class='text-gray-600 text-sm leading-relaxed'>（分析光源方向，材质对比产生的视觉张力）</p></section><section><h4 class='text-sm font-bold text-black border-b border-gray-200 pb-2 mb-3'>🚀 审美内化 (Practical Application)</h4><p class='text-gray-600 text-sm leading-relaxed'>（如何提炼并套用该图的一个具体美学公式）</p></section></div>"
            }}
            """
            response = model.generate_content(prompt)
            match = re.search(r'\{.*\}', response.text, re.DOTALL)
            if match: return json.loads(match.group())
        except: continue
    return get_academic_fallback(category, photo_id, index)

def update():
    ids_map = {
        "女性穿搭": ["1485230895905-efd5b757fb45", "1550614000-4b95d4662d59", "1539106723-b7ad4176adad", "1434389678232-04e21dca1ef3", "1529139574466-a303027c1d8b", "1515886657613-9f3515b0c78f", "1469334031218-e382a71b716b", "1532453288672-3a27e9be9efd"],
        "页面排版": ["1503694978374-8a2fa686963a", "1586075010923-2dd4570fb338", "1611162617474-5b21e879e113", "1561070791-2526d30994b5", "1541462608143-67571c6738dd", "1499951360447-b19be8fe80f5", "1512295767273-ac109cb3a5f6", "1626785774573-4b799315345d"],
        "家居装饰": ["1600210492486-724fe5c67fb0", "1618221195710-dd6b41faaea6", "1586023492125-27b2c045efd7", "1505691938895-1758d7feb511", "1554995207-c18c203602cb", "1616486338812-3dadae4b4ace", "1631679706909-1844bbd07221", "1522708323590-d24dbb6b0267"]
    }
    
    results = []
    for cat, pids in ids_map.items():
        for i, pid in enumerate(pids):
            data = fetch_aesthetic_analysis(cat, pid, i)
            if data: results.append(data)
            time.sleep(1) # 加快进货速度
            
    with open('aesthetic_data.json', 'w', encoding='utf-8') as f:
        json.dump(results, f, ensure_ascii=False, indent=4)

if __name__ == "__main__":
    update()
