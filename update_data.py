import json
import datetime

def fetch_trending():
    timestamp = datetime.datetime.now().strftime("%Y%m%d")
    
    # 精选 24 张顶级视觉 ID
    stable_ids = {
        "女性穿搭": [
            "1485230895905-efd5b757fb45", "1550614000-4b95d4662d59", "1539106723-b7ad4176adad", "1434389678232-04e21dca1ef3",
            "1529139574466-a303027c1d8b", "1515886657613-9f3515b0c78f", "1469334031218-e382a71b716b", "1532453288672-3a27e9be9efd"
        ],
        "页面排版": [
            "1503694978374-8a2fa686963a", "1586075010923-2dd4570fb338", "1611162617474-5b21e879e113", "1561070791-2526d30994b5",
            "1541462608143-67571c6738dd", "1499951360447-b19be8fe80f5", "1512295767273-ac109cb3a5f6", "1626785774573-4b799315345d"
        ],
        "家居装饰": [
            "1600210492486-724fe5c67fb0", "1618221195710-dd6b41faaea6", "1586023492125-27b2c045efd7", "1505691938895-1758d7feb511",
            "1554995207-c18c203602cb", "1616486338812-3dadae4b4ace", "1631679706909-1844bbd07221", "1522708323590-d24dbb6b0267"
        ]
    }
    
    all_results = []
    for category, id_list in stable_ids.items():
        for i, photo_id in enumerate(id_list):
            # --- 核心改进：在原始链接前加入 weserv 中转代理，实现国内加速 ---
            original_url = f"https://images.unsplash.com/photo-{photo_id}?w=800&q=80"
            proxy_url = f"https://images.weserv.nl/?url={original_url}"
            
            all_results.append({
                "id": f"{category}_{i}_{timestamp}",
                "category": category,
                "imageUrl": proxy_url, # 现在使用加速后的链接
                "title": f"审美热榜 No.{i+1}",
                "brief": f"捕捉【{category}】领域的全球顶级视觉范式。",
                "detailedAnalysis": "1. 视觉重心：利用黄金分割点聚焦核心。<br>2. 线条逻辑：画面极具延伸感。<br>3. 色彩平衡：高阶的中性色调。",
                "suggestion": "建议收藏并拆解其构图比例，作为短视频封面参考。"
            })
    return all_results

try:
    data = fetch_trending()
    with open('aesthetic_data.json', 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=4)
    print("加速引擎已部署！24个货架已全部更新。")
except Exception as e:
    print(f"补货出错: {e}")
