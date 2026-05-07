import json
import datetime

def fetch_trending():
    timestamp = datetime.datetime.now().strftime("%Y%m%d")
    
    # 定义三个板块及其对应的图片风格关键词
    categories = {
        "女性穿搭": ["fashion", "editorial", "style", "streetwear", "minimalist-fashion", "vogue", "outfit", "runway"],
        "页面排版": ["layout", "typography", "graphic-design", "poster", "swiss-design", "minimalism", "branding", "ui"],
        "家居装饰": ["interior", "architecture", "home-decor", "minimalist-home", "modern-living", "furniture", "loft", "wabi-sabi"]
    }
    
    all_results = []
    
    for category, keywords in categories.items():
        for i in range(8): # 每个板块生成 8 条，总计 24 条
            keyword = keywords[i]
            # 优化后的图片链接，加入更多随机因子和质量控制
            img_url = f"https://images.unsplash.com/featured/800x1000?{keyword}&sig={timestamp}{category}{i}"
            
            all_results.append({
                "id": f"{category}_{i}_{timestamp}",
                "category": category,
                "imageUrl": img_url,
                "title": f"今日热榜 No.{i+1} - {keyword.title()}",
                "brief": f"捕捉全网关于【{category}】的最高级审美趋势。",
                "detailedAnalysis": "1. 空间秩序：严格遵循视觉层级，核心信息秒抓眼球。<br>2. 色彩逻辑：采用极简配色方案，传递理性与专业感。<br>3. 构图艺术：利用留白引导视线移动，极具高级感。",
                "suggestion": "建议尝试此类风格的排版或穿搭，瞬间拉开与平庸的距离。"
            })
            
    return all_results

try:
    print("正在为 3 大板块补货，每份 8 条热点...")
    data = fetch_trending()
    with open('aesthetic_data.json', 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=4)
    print("补货完成！24 条审美灵感已上架。")
except Exception as e:
    print(f"补货失败: {e}")
