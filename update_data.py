import json
import datetime
import os
import time
import google.generativeai as genai
import re

# 1. 配置钥匙
GOOGLE_API_KEY = os.environ.get('GOOGLE_API_KEY')
genai.configure(api_key=GOOGLE_API_KEY)

# 2. 备用仓库：即便 AI 繁忙，也能确保 24 个货架 100% 亮灯
BACKUP_ANALYSIS = {
    "女性穿搭": {
        "title": "高级审美·视觉平衡",
        "brief": "利用材质冲突与色彩克制构建高级感。",
        "analysis": "1. 视觉重心：利用黄金分割点配置配饰，引导视线流动。<br>2. 比例逻辑：长短结合的层叠穿搭，拉长视觉线条。<br>3. 材质表达：软硬材质的碰撞（如丝绸配皮革），产生丰富的审美质感。",
        "suggestion": "建议在短视频封面中尝试大面积留白，增加呼吸感。"
    },
    "页面排版": {
        "title": "理性秩序·平面美学",
        "brief": "严谨的网格系统带来的视觉愉悦。",
        "analysis": "1. 空间秩序：严格遵循网格系统，确保信息层级秒抓眼球。<br>2. 负空间艺术：大面积留白缓解视觉疲劳，聚焦核心信息。<br>3. 字体层次：通过字重与字号的剧烈对比，制造视觉张力。",
        "suggestion": "制作PPT或海报时，尝试将重心偏置，利用留白处排版文字。"
    },
    "家居装饰": {
        "title": "空间叙事·静谧居所",
        "brief": "天然材质与极简空间的深度对话。",
        "analysis": "1. 光影氛围：利用自然采光与漫反射光源，营造空间的宁静感。<br>2. 材质细节：微水泥与原木的碰撞，强调自然的原始质感。<br>3. 重心布局：家具低重心化设计，释放纵向空间压力。",
        "suggestion": "拍摄室内设计时，尝试低角度取景，增加空间纵深感。"
    }
}

def fetch_ai_data(category, photo_id):
    # 尝试所有可能的模型版本名，确保进货稳定
    for model_name in ['gemini-1.5-flash-latest', 'gemini-pro']:
        try:
            model = genai.GenerativeModel(model_name)
            prompt = f"作为视觉专家深度客观拆解{category}领域图片ID为{photo_id}的作品。输出纯JSON包含id,category,imageUrl,title,brief,detailedAnalysis,suggestion。imageUrl统一用https://i0.wp.com/images.unsplash.com/photo-{photo_id}?w=1000&q=80"
            response = model.generate_content(prompt)
            match = re.search(r'\{.*\}', response.text, re.DOTALL)
            if match: return json.loads(match.group())
        except: continue
    return None

def update():
    # --- 核心改进：精准扩充为每个类目 8 个顶级 ID ---
    ids_map = {
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
    
    results = []
    print("🚀 审美寻猎全速启动（8x3 模式）...")
    
    for cat, pids in ids_map.items():
        for i, pid in enumerate(pids):
            data = fetch_ai_data(cat, pid)
            if not data: # AI 掉线则启动专业保底，确保每个格子都有货
                backup = BACKUP_ANALYSIS[cat]
                data = {
                    "id": f"pro_{pid}",
                    "category": cat,
                    "imageUrl": f"https://i0.wp.com/images.unsplash.com/photo-{pid}?w=1000&q=80",
                    "title": f"{backup['title']} No.{i+1}",
                    "brief": backup["brief"],
                    "detailedAnalysis": backup["analysis"],
                    "suggestion": backup["suggestion"]
                }
            results.append(data)
            print(f"✅ 已装载: [{cat}] {data['title']}")
            time.sleep(1)
            
    with open('aesthetic_data.json', 'w', encoding='utf-8') as f:
        json.dump(results, f, ensure_ascii=False, indent=4)
    print(f"🎉 24 条深度内容已全部上架！")

if __name__ == "__main__":
    update()
