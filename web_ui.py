import gradio as gr
import json
from bioclaw.core.engine import BioClawCoordinator

print("⏳ 正在唤醒 BioClaw 全知核心引擎...")
engine = BioClawCoordinator()

def beautify_report(raw_text):
    """🪄 翻译滤镜：把机器看的 JSON 变成人类看的高级报告"""
    try:
        data = json.loads(raw_text)
        agent = data.get("agent", "")
        
        # 如果是化学智能体返回的，披上化学报告的皮
        if "Chem" in agent:
            passed = "✅ 完美通过 (符合里宾斯基法则，成药潜力高)" if data.get("passed_rule_of_five") else "⚠️ 未通过 (可能需优化结构)"
            d = data.get("details", {})
            return f"""### 🧪 BioClaw 理化深度检验报告
**🔬 药物基础档案**
* 🏷️ **全网检索通用名称**: **`{d.get('PubChem_Official_Name', '未知新分子')}`**
* 🧬 **SMILES 结构**: `{data.get('smiles', '')}`

**⚖️ 成药潜力评估 (Rule of Five)**
* 综合判定: **{passed}**
* **分子量 (Weight)**: `{d.get('Weight')} g/mol`  *(标准阈值: ≤ 500)*
* **脂水分配系 (LogP)**: `{d.get('LogP')}` *(标准阈值: ≤ 5，影响细胞膜穿透)*
* **氢键供体数 (H-Donors)**: `{d.get('H_Donors')}` *(标准阈值: ≤ 5)*
* **氢键受体数 (H-Acceptors)**: `{d.get('H_Acceptors')}` *(标准阈值: ≤ 10)*
"""
        # 如果是生物智能体返回的，披上基因报告的皮
        elif "Omics" in agent:
            return f"""### 🧬 BioClaw 基因多组学推演报告
**🔬 基础序列信息**
* 📏 **序列长度 (Length)**: `{data.get('length')} bp`
* 📊 **GC 含量 (GC-Content)**: `{data.get('gc_content')}%` *(影响引物结合与热稳定性)*

**🔄 生命中心法则翻译推演**
* **原始 DNA**: `{data.get('sequence')}`
* **信使 RNA**: `{data.get('mrna')}`
* **蛋白质链**: `{data.get('protein_translation')}` *(注: 带有 `*` 代表捕捉到终止密码子)*
"""
        # 如果都不是，就原样输出
        return f"```json\n{raw_text}\n```"
    except Exception:
        return raw_text

def chat_logic(history, prompt, target):
    if not history:
        history = []
    if not prompt:
        history.append({"role": "user", "content": "⚠️ 空指令"})
        history.append({"role": "assistant", "content": "报告指挥官，请输入自然语言指令！"})
        return history, None, prompt, target

    # 让中枢大脑去处理运算任务，拿到生冷的 JSON 文本
    res = engine.route_task(prompt, target)
    
    # 🌟 调用滤镜！把 JSON 强行洗成极其漂亮的 Markdown 报告！
    bot_text = beautify_report(res['text'])
    img_path = res['image']
    
    user_msg = f"🗣️ **指令**: {prompt}\n🧬 **数据**: `{target if target else '无'}`"
    history.append({"role": "user", "content": user_msg})
    history.append({"role": "assistant", "content": bot_text})
    
    return history, img_path, "", ""

with gr.Blocks() as demo:
    gr.Markdown("# 🧬 BioClaw 中枢仪表盘 (Omniscient 2.0)")
    gr.Markdown("> **云端意图预测** | **生化知识联网爬虫** | **本地多组学运算** | **RDKit 视觉渲染**")
    
    with gr.Row():
        with gr.Column(scale=5):
            chatbot = gr.Chatbot(height=500, label="BioClaw 实验记录台")
            with gr.Row():
                user_input = gr.Textbox(scale=2, show_label=False, placeholder="输入你要让我做的事... (如：帮我查查这个)")
                data_input = gr.Textbox(scale=2, show_label=False, placeholder="输入生化数据 (SMILES / DNA)")
            submit_btn = gr.Button("🚀 提交给 BioClaw 引擎运算", variant="primary")
            
            gr.Examples(
                examples=[
                    ["从云端查一下这个分子的全名，并测试它的成药性", "CC(=O)OC1=CC=CC=C1C(=O)O"],
                    ["这是一种神秘的抗菌药物，看看它能过里宾斯基法则吗", "Cc1ccc(cc1)C(=O)NC2=CC=C(C=C2)S(=O)(=O)N"],
                    ["提取这段序列的特征，转录翻译氨基酸看看有没有突变", "ATGGCCATTGTAATGGGCCGCTGAAAGGGTGCCCGATAG"]
                ],
                inputs=[user_input, data_input],
                label="💡 快速指令控制面板 (点击按钮可直接填入指令)"
            )

        with gr.Column(scale=3):
            vis_image = gr.Image(label="🔬 2D 化学结构显微镜", type="filepath", interactive=False)

    submit_btn.click(
        fn=chat_logic, 
        inputs=[chatbot, user_input, data_input], 
        outputs=[chatbot, vis_image, user_input, data_input]
    )
    user_input.submit(chat_logic, [chatbot, user_input, data_input], [chatbot, vis_image, user_input, data_input])
    data_input.submit(chat_logic, [chatbot, user_input, data_input], [chatbot, vis_image, user_input, data_input])

if __name__ == "__main__":
    # 配置以消除 Gradio 6.0 的某些主题参数警告
    demo.launch(server_name="127.0.0.1", server_port=7860, inbrowser=True)
