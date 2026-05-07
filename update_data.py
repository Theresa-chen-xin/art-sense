import json
import requests
import datetime

def fetch_trending():
    # 模拟从高质量图库接口获取今日最火的 8 张图
    # 我们使用了特定的审美标签来过滤
    timestamp = datetime.datetime.now().strftime("%Y%m%d")
    topics = ["minimalist", "editorial", "modern-interior", "avant-garde"]
    results = []
    
    for i in range(8):
        topic = topics[i % len(topics)]
        results.append({
            "id": f"top_{i}_{timestamp}",
            "category": "视觉灵感",
            "imageUrl": f"https://images.unsplash.com/photo-1512295767273-ac109cb3a5f6?auto=format&fit=crop&w=800&q=80&sig={timestamp}{i}",
            "title": f"今日热榜 No.{i+1} - {topic.title()}",
            "brief": "全网高讨论度视觉标杆，由 Art Sense 自动捕捉。",
            "detailedAnalysis": "1. 几何平衡：严格的网格构图。<br>2. 色彩逻辑：采用极简的中性色调。",
            "suggestion": "建议尝试高留白排版。"
        })
    return results

# 写入文件
data = fetch_trending()
with open('aesthetic_data.json', 'w', encoding='utf-8') as f:
    json.dump(data, f, ensure_ascii=False, indent=4)
print("今日 Top 8 数据库已更新！")
