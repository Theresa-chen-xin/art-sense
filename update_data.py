import json
import datetime
import os
import time
import google.generativeai as genai
import re

# 1. 钥匙配置
GOOGLE_API_KEY = os.environ.get('GOOGLE_API_KEY')
genai.configure(api_key=GOOGLE_API_KEY)

# 2. 多维审美语料库：即便 AI 繁忙，也要确保 8 张图有 8 种专业视角
DIVERSE_BACKUP = {
    "女性穿搭": [
        {"title": "法式极简·视觉平衡", "brief": "利用低饱和度色块构建高级感。", "analysis": "1. 视觉重心：利用黄金分割点配置配饰，引导视线。2. 比例逻辑：利用高腰线优化头身比。", "sug": "建议封面尝试大面积留白。"},
        {"title": "先锋解构·结构张力", "brief": "打破对称性带来的视觉冲击。", "analysis": "1. 几何秩序：非对称剪裁创造出动态的视觉流向。2. 空间感：利用面料褶皱制造光影深浅。", "sug": "适合作为强视觉冲击力的封面素材。"},
        {"title": "老钱风·质感叙事", "brief": "通过天然材质传递稳定的阶层感。", "analysis": "1. 材质表达：哑光羊绒与珍珠的温润质感互补。2. 色彩哲学：极简米色调传递理性。", "sug": "拍摄时注意细节特写，强调材质。"},
        {"title": "高街机能·工业美学", "brief": "实用主义与未来感的视觉碰撞。", "analysis": "1. 线条逻辑：硬朗的轮廓线勾勒出力量感。2. 视觉锚点：利用金属扣件作为视觉抓手。", "sug": "建议搭配冷色调滤镜提升科技感。"},
        {"title": "复古摩登·色彩重构", "brief": "高饱和度色彩的现代对比应用。", "analysis": "1. 互补色平衡：利用红色与绿色的低频对比制造张力。2. 节奏感：圆点元素的重复律动。", "sug": "适合活泼、高频剪辑类视频封面。"},
        {"title": "中性风·模糊边界", "brief": "消除性别属性的直线条设计。", "analysis": "1. 直线构图：垂直线条带来的冷静与克制。2. 视觉减法：舍弃多余装饰，聚焦版型。", "sug": "文字排版建议使用衬线体，中和硬朗。"},
        {"title": "波西米亚·自然秩序", "brief": "繁复纹样中的视觉统一性。", "analysis": "1. 纹理堆叠：通过相似元素的重复建立韵律。2. 光影氛围：利用自然光增强手工感。", "sug": "建议作为生活方式类视频背景。"},
        {"title": "静奢主义·细节克制", "brief": "不经意间的审美流露。", "analysis": "1. 隐藏细节：利用同色系缝线展示工艺。2. 视觉呼吸感：适当的露肤度平衡包裹感。", "sug": "建议封面字体选择极细体。"}
    ],
    "页面排版": [
        {"title": "瑞士网格·理性基石", "brief": "严谨的数学逻辑带来的视觉舒适。", "analysis": "1. 空间秩序：遵循三栏网格，确保信息层级秒抓眼球。2. 负空间：利用留白缓解视觉压力。", "sug": "PPT制作时，图片与文字比例建议3:2。"},
        {"title": "包豪斯·功能至上", "brief": "几何形状与基础色彩的终极组合。", "analysis": "1. 形式追随功能：利用粗体字强调核心动作指令。2. 视觉重心：红黄色块的冲突引导。", "sug": "教学类视频建议采用此排版。"},
        {"title": "酸性设计·未来主义", "brief": "高对比与金属质感的视觉轰炸。", "analysis": "1. 流体造型：无视重力的排版带来的流动感。2. 光栅效果：利用折射光模拟屏幕感。", "sug": "适合时尚、潮流类短视频宣发。"},
        {"title": "新丑风·反传统秩序", "brief": "故意打破平衡的视觉挑战。", "analysis": "1. 故意错位：打破对齐原则，制造不安感。2. 粗糙肌理：模拟报纸印刷的颗粒感。", "sug": "适合个性化极强的Vlog封面。"},
        {"title": "极简主义·减法艺术", "brief": "剔除一切干扰，直抵核心。", "analysis": "1. 视觉聚焦：利用极小元素与巨大留白的对比。2. 呼吸感：文字行间距拉大，降低压迫感。", "sug": "高端商务内容推荐此风格。"},
        {"title": "杂志风·叙事排版", "brief": "模拟纸媒质感的沉浸式体验。", "analysis": "1. 叠放逻辑：文字与图片的重叠制造空间层。2. 视觉节奏：大小标题的错位布局。", "sug": "适合个人IP展示页设计。"},
        {"title": "数据美学·可视化逻辑", "brief": "将枯燥数字转化为视觉享受。", "analysis": "1. 色谱映射：利用颜色深浅传递数据权重。2. 线条流动：利用连接线引导逻辑关系。", "sug": "总结类视频建议采用。"},
        {"title": "东方意境·留白韵味", "brief": "虚实结合的视觉平衡感。", "analysis": "1. 散点透视：视野不受固定边框限制。2. 视觉留白：赋予画面呼吸的灵魂。", "sug": "文化类博主封面首选。"}
    ],
    "家居装饰": [
        {"title": "侘寂风·残缺之美", "brief": "时间在材质上留下的审美印记。", "analysis": "1. 材质肌理：微水泥与老木头的颗粒感对比。2. 氛围感：暗调光影营造的冥想空间。", "sug": "拍摄室内设计时，尝试低角度取景。"},
        {"title": "包豪斯·工业优雅", "brief": "钢管、皮革与几何线条的重组。", "analysis": "1. 线条逻辑：钢管椅的曲线与空间的直角冲突。2. 色彩权重：局部克莱因蓝的点缀。", "sug": "适合作为专业、理性的人设背景。"},
        {"title": "奶油风·治愈包裹", "brief": "高明度色调带来的情绪安抚。", "analysis": "1. 色温平衡：全屋低饱和暖色调。2. 视觉圆角：家具无棱角化处理，增加柔和感。", "sug": "适合家居、育儿类视频封面。"},
        {"title": "中古风·复古回潮", "brief": "半个世纪前的审美精髓。", "analysis": "1. 木质色差：胡桃木色与焦糖色的层次。2. 几何美学：标志性PH灯具的造型美学。", "sug": "建议增加复古噪点滤镜。"},
        {"title": "极简北欧·光影逻辑", "brief": "追逐自然光的极致排版。", "analysis": "1. 采光设计：大面积开窗将室外景观引入。2. 视觉纯净：去除踢脚线的极致线条感。", "sug": "建筑摄影建议使用超广角。"},
        {"title": "工业LOFT·原始力量", "brief": "红砖与黑钢的粗犷对话。", "analysis": "1. 暴露美学：管道与横梁的视觉线条化。2. 空间高度：利用层高制造纵向呼吸感。", "sug": "适合探店、机械类主题背景。"},
        {"title": "法式轻奢·线条韵律", "brief": "优雅石膏线勾勒的贵族质感。", "analysis": "1. 对称美学：法式中轴线的视觉安定感。2. 视觉层次：水晶灯与鱼骨拼地板的对应。", "sug": "建议文字排版采用金色边框装饰。"},
        {"title": "极简主义·空白力量", "brief": "空间即是画作本身。", "analysis": "1. 空间体块：利用墙面转折制造几何阴影。2. 焦点法则：整个空间仅保留一件核心艺术品。", "sug": "展示极简生活态度时的最佳背景。"}
    ]
}

def fetch_ai_data(category, photo_id, index):
    # 按照优先级尝试 AI 接口
    for model_name in ['gemini-1.5-flash-latest', 'gemini-pro']:
        try:
            model = genai.GenerativeModel(model_name)
            # 强化 Prompt，要求必须根据不同 ID 给出差异化建议
            prompt = f"深度分析{category}领域图片(ID:{photo_id})。作为视觉专家，从设计法则、构图重心、光影材质、批判性建议四个维度拆解。输出纯JSON格式，严禁感性废话。包含id,category,imageUrl,title,brief,detailedAnalysis,suggestion。"
            response = model.generate_content(prompt)
            match = re.search(r'\{.*\}', response.text, re.DOTALL)
            if match: return json.loads(match.group())
        except: continue
    return None

def update():
    ids_map = {
        "女性穿搭": ["1485230895905-efd5b757fb45", "1550614000-4b95d4662d59", "1539106723-b7ad4176adad", "1434389678232-04e21dca1ef3", "1529139574466-a303027c1d8b", "1515886657613-9f3515b0c78f", "1469334031218-e382a71b716b", "1532453288672-3a27e9be9efd"],
        "页面排版": ["1503694978374-8a2fa686963a", "1586075010923-2dd4570fb338", "1611162617474-5b21e879e113", "1561070791-2526d30994b5", "1541462608143-67571c6738dd", "1499951360447-b19be8fe80f5", "1512295767273-ac109cb3a5f6", "1626785774573-4b799315345d"],
        "家居装饰": ["1600210492486-724fe5c67fb0", "1618221195710-dd6b41faaea6", "1586023492125-27b2c045efd7", "1505691938895-1758d7feb511", "1554995207-c18c203602cb", "1616486338812-3dadae4b4ace", "1631679706909-1844bbd07221", "1522708323590-d24dbb6b0267"]
    }
    
    results = []
    print("🚀 审美实验室：正在进行 8x3 差异化寻猎...")
    
    for cat, pids in ids_map.items():
        for i, pid in enumerate(pids):
            data = fetch_ai_data(cat, pid, i)
            if not data: # 启动差异化保底逻辑
                backup = DIVERSE_BACKUP[cat][i]
                data = {
                    "id": f"pro_{pid}",
                    "category": cat,
                    "imageUrl": f"https://i0.wp.com/images.unsplash.com/photo-{pid}?w=1000&q=80",
                    "title": backup["title"],
                    "brief": backup["brief"],
                    "detailedAnalysis": backup["analysis"],
                    "suggestion": backup["sug"]
                }
            results.append(data)
            print(f"✅ 装载完毕: [{cat}] {data['title']}")
            time.sleep(1)
            
    with open('aesthetic_data.json', 'w', encoding='utf-8') as f:
        json.dump(results, f, ensure_ascii=False, indent=4)

if __name__ == "__main__":
    update()
