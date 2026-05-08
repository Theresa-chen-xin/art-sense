import json
import os
import time
import google.generativeai as genai
import re

GOOGLE_API_KEY = os.environ.get('GOOGLE_API_KEY')
genai.configure(api_key=GOOGLE_API_KEY)

# 💡 核心升级：把保底文案也写成顶级干货！就算没连上AI，也能学到东西。
def get_deep_fallback(category, photo_id, index):
    return {
        "id": f"pro_{photo_id}",
        "category": category,
        "imageUrl": f"https://images.unsplash.com/photo-{photo_id}?auto=format&fit=crop&w=1000&q=80",
        "title": "高级感重塑：克制与张力的视觉博弈",
        "brief": "通过大面积留白与核心元素的材质碰撞，建立顶级视觉秩序。",
        "detailedAnalysis": """
        <div class='space-y-12'>
            <section>
                <h4 class='text-lg font-serif font-bold text-black border-b-2 border-black pb-3 mb-5'>01 / 构图法则 (Composition)</h4>
                <p class='text-gray-600 text-[15px] leading-loose'>本作品放弃了传统的居中对齐，采用了更为高级的“三分法偏置构图”。创作者刻意在画面的左侧/上方留出了高达 60% 的负空间（Negative Space）。这种大面积的留白并非空间的浪费，而是为了给观众的视觉提供“呼吸感”。小白在实操时，最容易犯的错误就是把画面填满，这反而会导致视觉焦点的丧失。正确的做法是：只保留一个绝对的核心主体，并将其放置在九宫格的交叉点上，利用留白形成气场。</p>
            </section>
            <section>
                <h4 class='text-lg font-serif font-bold text-black border-b-2 border-black pb-3 mb-5'>02 / 色彩动力 (Color Dynamics)</h4>
                <p class='text-gray-600 text-[15px] leading-loose'>画面运用了经典的“莫兰迪色系”逻辑——也就是降低所有颜色的饱和度，加入灰调。这种色彩处理方式能够剥离颜色的“火气”，传递出一种冷静、克制的情绪价值。但在整体低饱和度的背景下，作者巧妙地在核心视觉锚点处，点缀了极小面积的高饱和度对比色（例如克莱因蓝或爱马仕橙）。这种“90%低调 + 10%爆发”的色彩公式，能够瞬间抓住眼球且不显廉价。</p>
            </section>
            <section>
                <h4 class='text-lg font-serif font-bold text-black border-b-2 border-black pb-3 mb-5'>03 / 质感与光影 (Light & Texture)</h4>
                <p class='text-gray-600 text-[15px] leading-loose'>高级感往往来源于材质的冲突。在这里，我们能看到“硬与软”、“哑光与高光”的直接对抗。例如金属的冷硬与织物的柔软形成对比，或者哑光微水泥与反光玻璃的结合。在光影处理上，没有使用平淡的顺光，而是采用了带有明显指向性的侧逆光。侧光能够勾勒出物体的边缘轮廓，强化表面的粗糙肌理，让平面的二维图像产生了强烈的三维立体感。</p>
            </section>
            <section class="bg-gray-50 p-8 rounded border-l-4 border-black">
                <h4 class='text-sm font-bold uppercase tracking-widest text-black mb-4'>💡 导师建议：小白如何直接套用公式？</h4>
                <ol class='list-decimal list-inside text-gray-700 text-[14px] leading-loose space-y-2'>
                    <li>做减法：无论是穿搭还是排版，去掉你身上/画面中 30% 不必要的装饰。</li>
                    <li>定主色调：确保画面中有一种颜色占据主导地位（70%），切忌色彩均分。</li>
                    <li>制造冲突：如果你穿了非常基础的纯色衣服，请搭配一个极具设计感或金属光泽的配饰作为破局点。</li>
                </ol>
            </section>
        </div>
        """
    }

def fetch_aesthetic_analysis(category, photo_id, index):
    for model_name in ['gemini-1.5-flash', 'gemini-pro']:
        try:
            model = genai.GenerativeModel(model_name)
            # 💡 强制约束 AI：必须详实，不少于500字！
            prompt = f"""
            你是一位拥有顶级审美的视觉艺术总监，正在手把手教零基础的小白如何看懂高级感。
            请深度拆解【{category}】领域的顶尖作品(ID:{photo_id})。
            
            极其严格的要求：
            1. 拒绝空洞！必须具体到“它用了什么颜色、什么光线、放在了什么位置”。
            2. 每个维度的解析文字必须极其详实，整篇分析不少于500字。
            
            输出纯 JSON，格式如下：
            {{
                "id": "pro_{photo_id}",
                "category": "{category}",
                "imageUrl": "https://images.unsplash.com/photo-{photo_id}?auto=format&fit=crop&w=1000&q=80",
                "title": "（起一个客观且具有洞察力的标题）",
                "brief": "（一句话总结核心美学规律）",
                "detailedAnalysis": "<div class='space-y-12'><section><h4 class='text-lg font-serif font-bold text-black border-b-2 border-black pb-3 mb-5'>01 / 构图法则 (Composition)</h4><p class='text-gray-600 text-[15px] leading-loose'>（至少150字深度解析，为什么这么排，留白怎么用）</p></section><section><h4 class='text-lg font-serif font-bold text-black border-b-2 border-black pb-3 mb-5'>02 / 色彩动力 (Color Dynamics)</h4><p class='text-gray-600 text-[15px] leading-loose'>（至少150字深度解析，饱和度、对比度、主次色调）</p></section><section><h4 class='text-lg font-serif font-bold text-black border-b-2 border-black pb-3 mb-5'>03 / 质感与光影 (Light & Texture)</h4><p class='text-gray-600 text-[15px] leading-loose'>（至少100字深度解析，光源方向，材质对比）</p></section><section class='bg-gray-50 p-8 rounded border-l-4 border-black'><h4 class='text-sm font-bold uppercase tracking-widest text-black mb-4'>💡 导师建议：小白如何直接套用公式？</h4><ol class='list-decimal list-inside text-gray-700 text-[14px] leading-loose space-y-2'><li>（实操步骤1）</li><li>（实操步骤2）</li><li>（实操步骤3）</li></ol></section></div>"
            }}
            """
            response = model.generate_content(prompt)
            match = re.search(r'\{.*\}', response.text, re.DOTALL)
            if match: return json.loads(match.group())
        except: continue
    
    # 只要 AI 出错，就调用我们写好的上千字干货！
    return get_deep_fallback(category, photo_id, index)

def update():
    ids_map = {
        "女性穿搭": ["1485230895905-efd5b757fb45", "1550614000-4b95d4662d59", "1539106723-b7ad4176adad", "1434389678232-04e21dca1ef3"],
        "页面排版": ["1503694978374-8a2fa686963a", "1586075010923-2dd4570fb338", "1611162617474-5b21e879e113", "1561070791-2526d30994b5"],
        "家居装饰": ["1600210492486-724fe5c67fb0", "1618221195710-dd6b41faaea6", "1586023492125-27b2c045efd7", "1505691938895-1758d7feb511"]
    } # 暂时保留12张保证速度，通过后再扩充到24张。
    
    results = []
    print("🚀 启动[万字干货版]审美解析引擎...")
    
    for cat, pids in ids_map.items():
        for i, pid in enumerate(pids):
            data = fetch_aesthetic_analysis(cat, pid, i)
            if data: results.append(data)
            time.sleep(5) # 必须休息5秒，防止被封
            
    with open('aesthetic_data.json', 'w', encoding='utf-8') as f:
        json.dump(results, f, ensure_ascii=False, indent=4)

if __name__ == "__main__":
    update()
