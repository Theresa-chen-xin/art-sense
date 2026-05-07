import json
import datetime

def fetch_trending():
    timestamp = datetime.datetime.now().strftime("%Y%m%d")
    
    # 这里的名字必须和网页里的 filterData('名字') 保持绝对一致
    categories = {
        "女性穿搭": ["fashion", "style", "editorial", "outfit", "vogue", "streetwear", "couture", "minimalist-fashion"],
        "页面排版": ["layout", "typography", "graphic-design", "poster", "swiss-design", "branding", "ui", "minimalism"],
        "家居装饰": ["interior", "home-decor", "architecture", "modern-living", "furniture", "loft", "wabi-sabi", "room"]
    }
    
    all_results = []
    
    for category, keywords in categories.items():
        for i in range(8): # 精准补齐：每个板块 8 个
            keyword = keywords[i]
            # 使用更稳定的动态图片接口
            img_url = f"https://images.unsplash.com/featured/800x1000?{keyword}&sig={timestamp}{category}{i}"
            
            all_results.append({
                "id": f"{category}_{i}_{timestamp}",
                "category": category, # 这里的标签现在和网页按钮完美匹配了
                "imageUrl": img_url,
                "title": f"今日热点 - {keyword.replace('-', ' ').title()}",
                "brief": f"来自【{category}】领域的全球视觉前沿。",
                "detailedAnalysis": "1. 视觉重心：构图严谨，聚焦核心。<br>2. 质感表达：利用材质对比提升高级感。<br>3. 留白艺术：给视觉呼吸的空间。",
                "suggestion": "建议收藏并分析其中的构图比例。"
            })
            
    return all_results

try:
    print("正在精准补货：3 大板块 x 8 条 = 24 条灵感...")
    data = fetch_trending()
    with open('aesthetic_data.json', 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=4)
    print("补货成功！所有货架已对齐。")
except Exception as e:
    print(f"补货出错: {e}")
