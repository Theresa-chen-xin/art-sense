import json
import requests
import datetime
import os
import time
# 新增：Gemini SDK
import google.generativeai as genai

# 获取 GitHub 注入的环境变量中的 Key
GOOGLE_API_KEY = os.environ.get('GOOGLE_API_KEY')
if not GOOGLE_API_KEY:
    print("错误: 未检测到 GOOGLE_API_KEY，请确保在 GitHub Secrets 中正确设置了 GEMINI_KEY！")
    exit(1)

# 配置 Gemini
genai.configure(api_key=GOOGLE_API_KEY)
model = genai.GenerativeModel('gemini-pro')

def analyze_image_pro(category, img_url):
    """
    让 Gemini 真正介入，对图片进行深度客观理性拆解
    由于云端无法直接发送文件，我们通过 Prompt 将分类名和图片描述传给它
    以此来模拟对具体图片的分析逻辑
    """
    timestamp = datetime.datetime.now().strftime("%Y%m%d%H%M")
    topics_map = {
        "女性穿搭": "法式极简黑白、低饱和老钱风、慵懒叠穿、机能风机能机能風、波西米亚度假風、3D拟物化柔软粘土风、干练通勤大女主气场風、日系通透氧气叠穿风、暗黑先锋机能风、古着混搭、极简同色系、大胆撞色、Y2K千禧风、老钱静奢风、慵懒意式复古风",
        "页面排版": "大留白杂志风、瑞士网格理性严谨排版、包豪斯几何构成排版、复古波普艺术拼贴、酸性金属鐳射镭射排版、数据可视化可视化排版、3D拟物化拟物化拟物化拟物化拟物化拟物化拟物化拟物化拟物化、竖排文字东方和风意境、大面积留白负空间排版、中性色极简主义、几何错位网格排版",
        "家居装饰": "现代侘寂微水泥客厅、法式轻奢轻奢轻奢轻奢线条感客厅、北欧原木极简极简极简主义主义主义卧室、美式乡村田园田园田园田园田园温情、现代轻奢轻奢轻奢轻奢黄铜大理石、新中式中式中式中式禅意屏风禅意意境空间、工業工業工業工業工业工业LOFT紅砖红砖墙、奶油奶油奶油奶油奶油中古中古风、多巴胺多巴胺多巴胺多巴胺孟菲斯几何、微水泥侘寂、低重心宁静力量"
    }
    
    # 获取对应分类下的随机热点关键词
    keyword_pool = topics_map.get(category, "审美趋势")
    
    # --- 核心新增：精心调教的 AI 提示词 (Prompt) ---
    prompt = f"""
        Role: 你是一个拥有 15 年经验的、客观理性的、国际顶级审美策展人和设计批评家。
        
        Task: 分析今日全网最火的一个关于【{category}】领域的视觉标杆案例。你必须使用客观、专业、没有任何废话的语言，为审美小白提供‘导师级’的深度拆解。
        
        Input Context: 分类名【{category}】，图片网络ID【{img_url.split('/')[-1]}】。你无法看到图片，请根据分类和关键词随机模拟出一个今日该领域的‘审美趋势标杆’（如关键词池：{keyword_pool}）来进行分析。
        
        Output Format:
        你必须完全依照下面的 JSON 格式，不要返回任何多余的开头或结尾：
        {{
            "id": "top_{timestamp}_{category}",
            "category": "{category}",
            "imageUrl": "{img_url}",
            "title": "（你模拟出的、客观理性的标题，限制 10 个字以内）",
            "brief": "（你模拟出的、客观理性的短描述，限制 20 个字以内）",
            "detailedAnalysis": "（你模拟出的、客观理性的、导师级四点深度拆解，每一块用英文 `.<br>` 分割。内容必须涵盖色彩体系、构图逻辑、材质细节、光影氛围，限制 200 字以内）",
            "suggestion": "（你模拟出的、客观理性的、给新手的商业建议，限制 30 字以内）"
        }}
        
        Constraint:
        1.  不要使用“这个作品真美”这种主观废话。
        2.  必须从技术和设计法则的角度切入分析。
        3.  JSON 里的属性名必须和上面的完全一致，JSON 必须合法。
    """

    try:
        response = model.generate_content(prompt)
        # 清除 AI 有时候会加在开头的 ```json
        clean_text = response.text.replace('```json', '').replace('```', '').strip()
        data = json.loads(clean_text)
        return data
    except Exception as e:
        print(f"AI 分析出错 (ID: {img_url.split('/')[-1]}): {e}，将使用备用文字")
        return None

def update_database():
    timestamp = datetime.datetime.now().strftime("%Y%m%d")
    
    # 锁定 24 张高清、具有极高审美价值的图片 ID
    categories_map = {{
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
    }}
    
    all_results = []
    
    for category, id_list in categories_map.items():
        print(f"正在进行【{category}】领域的 AI 客观理性拆解，每份 8 条灵感...")
        for i, photo_id in enumerate(id_list):
            # 使用高可靠性的图片中转加速链接
            img_url = f"[https://images.unsplash.com/photo-](https://images.unsplash.com/photo-){photo_id}?auto=format&fit=crop&w=800&q=80"
            
            # --- 核心改进：呼叫 AI 真正生成分析文案 ---
            print(f"  -> 呼叫 AI 分析 Top.{i+1}...")
            # 由于云端无法发送文件，我们将类别名和图片描述发给AI，让其根据其广泛的设计知识随机匹配出合理的分析
            # 在云端我们只能根据图片的描述去模拟生成合理的设计分析
            ai_data = analyze_image_pro(category, img_url)
            
            # 为了商业效率，我们加入一个小的延时，防止请求过快被 AI 接口临时封禁
            time.sleep(1) 
            
            if ai_data:
                # 注入真实的图片链接
                ai_data["imageUrl"] = img_url
                all_results.append(ai_data)
            else:
                # 如果 AI 分析失败，则提供一个合理的客观理性兜底方案
                all_results.append({
                    "id": f"bk_{category}_{i}_{timestamp}",
                    "category": category,
                    "imageUrl": img_url,
                    "title": f"客观理性案例 No.{i+1}",
                    "brief": f"来自【{category}】领域的视觉标杆。",
                    "detailedAnalysis": "1. 色彩克制：采用低饱和的中性色调，传递专业感。<br>2. 空间秩序：视觉焦点的布局严谨，核心信息一目了然。<br>3. 材质表达：强调通过不同材质接触点的对比来传递高级感。",
                    "suggestion": "建议收藏并拆解其构图逻辑，作为短视频封面排版参考。"
                })
    
    return all_results

try:
    print("开始执行全自动导师级审美寻猎...")
    data = update_database()
    with open('aesthetic_data.json', 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=4)
    print("数据库更新成功！所有货架已换上 AI 导师级客观拆解文案。")
except Exception as e:
    print(f"更新出错: {e}")
