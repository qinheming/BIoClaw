import os
import gradio as gr
from bioclaw.core.engine import BloClawCoordinator

print("🚀 正在唤醒 BloClaw OS [真·沉浸纯粹去键无框版]...")
engine = BloClawCoordinator()

saas_css = """
<style>
/* 整个页面纯净布局，最高限宽拉大，给左屏和光幕预留广袤空间 */
:root, body, .gradio-container { background-color: #ffffff !important; max-width: 1400px !important; margin: 0 auto !important; font-family: -apple-system, system-ui, sans-serif !important; height: 100vh !important; display: flex; flex-direction: column; overflow: hidden; padding: 0 !important;}
footer { display: none !important; }

/* 顶置导航 */
#top_nav { border-bottom: 1px solid #f3f4f6 !important; padding: 10px 25px !important; align-items: center !important; flex-shrink: 0 !important; }

#main_stage { flex-grow: 1 !important; overflow-y: auto !important; display: flex; flex-direction: column; padding: 2vh 2%; }

/* 居中首屏Logo与神坛 */
#welcome_mat { margin: auto !important; display: flex; flex-direction: column; align-items: center; justify-content: center; width: 100%;}

/* 强力不折行CSS卡片区 */
#cards_row { flex-wrap: nowrap !important; display: flex !important; width: 100%; max-width: 1100px; margin: 0 auto; gap: 15px;}
.task-card {
    background: #ffffff !important; border: 1px solid #e0f2fe !important; border-radius: 12px !important; padding: 12px 15px !important; 
    cursor: pointer !important; transition: all 0.2s ease !important; flex: 1 !important; text-align: left !important; box-shadow: 0 2px 10px rgba(0,0,0,0.02) !important;
}
.task-card:hover { border-color: #0ea5e9 !important; box-shadow: 0 8px 20px rgba(14,165,233,0.1) !important; transform: translateY(-3px) !important; }

/* 聊天气泡去边框化 */
#chat_panel { background: transparent !important; border: none !important; margin-right: 15px !important; height: 100% !important; overflow-y: auto !important; }
.message.user { border: none !important; background: #f1f5f9 !important; color: #0f172a !important; border-radius: 18px !important; padding: 12px 18px !important; margin-left: auto !important; max-width: 85% !important; box-shadow: 0 2px 4px rgba(0,0,0,0.02) !important;}
.message.bot { border: none !important; background: transparent !important; color: #1e293b !important; padding: 12px 0 12px 15px !important; margin-bottom: 20px !important; max-width: 100% !important; }

/* 右侧全景物理室光幕 */
#canvas_panel { background: #ffffff !important; border: 1px solid #cbd5e1 !important; border-radius: 12px; height: 75vh !important; overflow: hidden; box-shadow: 0 4px 20px rgba(0,0,0,0.04) !important; display: flex; flex-direction: column; transition: all 0.4s cubic-bezier(0.16, 1, 0.3, 1); }
#canvas_toolbar { border-bottom: 1px solid #f1f5f9; padding: 8px 12px; align-items: center; background: #ffffff; }

/* 🌟 底沉无界限胶囊输入舱，完全抛弃额外按钮组 */
#bottom_deck {
    flex-shrink: 0 !important; background: transparent !important; border: none !important;
    padding: 0 10% 4vh 10% !important; display: flex; align-items: center; justify-content: center; position: relative;
}
.inner-capsule {
    width: 100%; max-width: 900px;
    background: #ffffff !important; border: 1px solid #cbd5e1 !important; border-radius: 26px !important;
    box-shadow: 0 4px 25px rgba(0,0,0,0.05) !important; padding: 4px 8px !important; display: flex; align-items: center;
}
.inner-capsule:focus-within { box-shadow: 0 8px 30px rgba(14,165,233,0.1) !important; border-color: #93c5fd !important; }
.inner-capsule .gradio-multimodal-textbox { border: none !important; box-shadow: none !important; background: transparent !important; font-size: 15px !important; outline: none !important; width: 100%; margin: 0 !important; padding: 0 !important;}

/* 高级悬浮打断急停锁钮 */
#stop_btn_container { position: absolute; top: -45px; z-index: 100; left: 50%; transform: translateX(-50%); }
</style>
"""

STANDBY_HTML = """
<div style="height: 100%; display: flex; flex-direction: column; justify-content: center; align-items: center; color: #94a3b8; font-family: system-ui;">
    <svg width="40" height="40" fill="none" stroke="currentColor" stroke-width="1.5" viewBox="0 0 24 24" style="margin-bottom: 15px; opacity: 0.4;"><path stroke-linecap="round" stroke-linejoin="round" d="M14 10l-2 1m0 0l-2-1m2 1v2.5M20 7l-2 1m2-1l-2-1m2 1v2.5M14 4l-2-1-2 1M4 7l2-1M4 7l2 1M4 7v2.5M12 21l-2-1m2 1l2-1m-2 1v-2.5M6 18l-2-1v-2.5M18 18l2-1v-2.5"></path></svg>
    <h3 style="margin: 0; font-weight: 500; letter-spacing: 1px;">BloClaw 光幕待命</h3>
    <p style="font-size: 13px; margin-top: 8px; opacity: 0.6;">等待物理引擎推流图表...</p>
</div>
"""

# ================= 🚀 数据链路与 UI 管控  =================

def reset_session():
    return (
        [], None,
        gr.update(visible=True), gr.update(visible=False), gr.update(visible=False),
        STANDBY_HTML, 
        gr.update(value={"text": "", "files": []}, interactive=True, placeholder="💡 核心数据已卸载。开始新项目...")
    )

def prepare_task(user_data, history):
    text = user_data.get("text", "")
    files = user_data.get("files", [])
    
    if not text.strip() and not files: 
        return gr.update(), history, gr.update(), gr.update(), gr.update(), payload
        
    if history is None: history = []
    
    display_msg = text if text.strip() else "处理当前加载的私有绝密文档数据集。"
    if files:
        f_names = [os.path.basename(f if isinstance(f, str) else getattr(f, 'filepath', getattr(f, 'name', str(f)))) for f in files]
        display_msg += f"\n\n*(📎 AI 已从隐秘网口挂载附加介质: {', '.join(f_names)})*"
    
    history.append({"role": "user", "content": display_msg})
    # 并发控制占位锁
    history.append({"role": "assistant", "content": "*(⏳ 数据解析流重连，系统满载推演中...)*"})
    
    payload = {"pure_text": text, "pure_files": files}
    
    return (
        gr.update(value={"text": "", "files": []}, interactive=False, placeholder="⏳ 交互已被底座冻结锁死，待引擎归零..."), 
        history, 
        gr.update(visible=False),  # welcome_block (隐藏大 Logo)
        gr.update(visible=True),   # workspace_block (展现聊天瀑布)
        gr.update(visible=True),   # stop_btn (浮现红区悬浮按键！)
        payload                    
    )

def execute_task(history, payload):
    if not payload: 
        yield history, gr.skip(), gr.skip(), gr.update(interactive=True, placeholder="💡 下达新的指令参数..."), gr.update(visible=False); return
    
    safe_text = payload["pure_text"] if payload["pure_text"] else "提取文档结构并归纳"
    
    # 传过去历史中已经清掉假占位气泡的那六条有效聊天，提供短效记忆追踪能力！
    past_memory = history[:-1] if len(history) > 1 else None
    res = engine.process_chat(safe_text, uploaded_files=payload["pure_files"], memory_context=past_memory)
    
    history[-1]["content"] = res["text"]
    
    new_html = res.get("screen_html")
    should_open = bool(new_html)
    
    yield (
        history, 
        gr.update(visible=True) if should_open else gr.update(visible=False), 
        gr.update(value=new_html) if should_open else gr.skip(),
        gr.update(interactive=True, placeholder="💡 给 BloClaw 持续发送新指令..."),
        gr.update(visible=False) # 红色急停钮隐匿！
    )

def force_stop():
    return (
        gr.update(interactive=True, placeholder="🛑 已中断主脑。给 BloClaw 准备新指令..."),
        gr.update(visible=False)
    )

def toggle_right_panel(is_open):
    new_state = not is_open
    return gr.update(visible=new_state), new_state

def close_right_panel():
    return gr.update(visible=False), False

def put_text(text):
    return gr.update(value={"text": text, "files": []})

with gr.Blocks(title="BloClaw OS") as demo:
    gr.HTML(saas_css, visible=False)
    task_payload = gr.State()
    is_panel_open = gr.State(False) 

    # ================= 🌌 顶置全局导航栏 =================
    with gr.Row(elem_id="top_nav"):
        gr.Markdown("🧬 <span style='font-size:18px; font-weight:bold; color:#0f172a;'>BloClaw Hub.</span> <span style='font-size:13px;color:#64748b;'>The Ultimate Autonomous AI Scientist.</span>")
        with gr.Row():
            toggle_panel_btn = gr.Button("◫ 切控视界幕布", variant="secondary", size="sm")
            new_chat_btn = gr.Button("➕ 构建新纪元", variant="primary", size="sm")

    # ================= 🌌 主干舞台 =================
    with gr.Column(elem_id="main_stage"):
        
        # 居中神坛
        with gr.Column(elem_id="welcome_mat") as welcome_block:
            gr.Markdown("<div style='font-size:3.5rem; margin-bottom:10px; text-align:center;'>🌌</div>")
            gr.Markdown("<h1 style='font-size:2.8rem; color:#0f172a; margin:0; text-align:center;'>BloClaw Hub</h1>")
            # 🌟 使用了您指定的最具有极客深度的 Slogan！！
            gr.Markdown("<p style='color:#14b8a6; font-size:1.1rem; text-align:center; padding-bottom:30px; font-weight: 500;'>The Ultimate Autonomous AI4S Copilot.</p>")
            
            with gr.Row(elem_id="cards_row"):
                card1 = gr.Button("💊 药物 2D 与靶标对接\n\n一键计算氟西汀并完成受体推演。", elem_classes="bg-white border shadow-sm rounded-xl p-4 text-left font-bold")
                card2 = gr.Button("🌌 虚空测算 3D 生命螺旋\n\n云端折叠预测未知序列的蛋白质空间力场。", elem_classes="bg-white border shadow-sm rounded-xl p-4 text-left font-bold")
                card3 = gr.Button("📊 Agent 沙盘数据绘图\n\n编写代码驱动数据逻辑斯蒂网络极限公式。", elem_classes="bg-white border shadow-sm rounded-xl p-4 text-left font-bold")

            cmd1 = gr.Textbox(value="帮我画出抗抑郁药氟西汀的二维分子图，SMILES：CNCCC(c1ccccc1)Oc2ccc(cc2)C(F)(F)F", visible=False)
            cmd2 = gr.Textbox(value="计算这串未知生命序列的三维折叠与力场：MVLSPADKTNVKAAWGKVGAHAGEYGAEALERMF", visible=False)
            cmd3 = gr.Textbox(value="使用 numpy 为我设计一整套生物种群繁衍和演进数据的『逻辑斯蒂回归热力图 (Logistic Growth)』，并用 plotly 或 seaborn 等在沙盒生成高质图线供我研究（不能有废话！必含图源结果！）。", visible=False)

        # 隐藏的双轨列阵，聊天时原地现身！
        with gr.Row(visible=False) as workspace_block:
            with gr.Column(scale=6):
                chatbot = gr.Chatbot(show_label=False, container=False, elem_id="chat_panel")
                
            with gr.Column(scale=5, visible=False, elem_id="canvas_panel") as right_panel:
                with gr.Row(elem_id="canvas_toolbar"):
                    gr.Markdown("### 🔬 物理与代码视窗", elem_classes="text-sm font-bold text-gray-500 mt-1 ml-1")
                    close_canvas_btn = gr.Button("✖ 掩盖视窗", size="sm", variant="secondary")
                
                with gr.Column(elem_classes="flex-1 overflow-hidden p-2 flex flex-col justify-center"):
                    canvas_screen = gr.HTML(value=STANDBY_HTML, elem_classes="h-full w-full", visible=True)

    # ================= 🌌 沉底多模胶囊 =================
    with gr.Column(elem_id="bottom_deck"):
        with gr.Row(elem_id="stop_btn_container"):
            stop_btn = gr.Button("■ 强制剥离底层渲染 (Stop)", variant="stop", visible=False, size="sm")

        with gr.Group(elem_classes="inner-capsule"):
            with gr.Row(equal_height=True, elem_classes="items-center w-full h-full"):
                # 🌟 绝绝子：剥壳纯去边框的用户无缝输入舱，彻底除掉原生恶心多余右按钮！！
                user_input = gr.MultimodalTextbox(
                    scale=9, show_label=False, 
                    placeholder="💡 解析文件数据、上传 PDF 等；直接键入指令进行 2D构象 / 3D全息分析 (Enter发送)",
                    container=False, lines=1
                )


    # ================= 🚀 数据流与雷达绑定 =================
    new_chat_btn.click(fn=reset_session, inputs=None, outputs=[chatbot, task_payload, welcome_block, workspace_block, right_panel, canvas_screen, user_input])
    toggle_panel_btn.click(fn=toggle_right_panel, inputs=[is_panel_open], outputs=[right_panel, is_panel_open])
    close_canvas_btn.click(fn=close_right_panel, inputs=None, outputs=[right_panel, is_panel_open])

    for btn, cmd in [(card1, cmd1), (card2, cmd2), (card3, cmd3)]:
        btn.click(fn=put_text, inputs=[cmd], outputs=[user_input]).then(
            fn=prepare_task, inputs=[user_input, chatbot], outputs=[user_input, chatbot, welcome_block, workspace_block, stop_btn, task_payload], queue=False
        ).then(
            fn=execute_task, inputs=[chatbot, task_payload], outputs=[chatbot, right_panel, canvas_screen, user_input, stop_btn]
        )

    # 唯一的管线输出渠道，直接由大文本框组件敲回车引发！
    sub_1 = user_input.submit(
        fn=prepare_task, inputs=[user_input, chatbot], outputs=[user_input, chatbot, welcome_block, workspace_block, stop_btn, task_payload], queue=False
    ).then(
        fn=execute_task, inputs=[chatbot, task_payload], outputs=[chatbot, right_panel, canvas_screen, user_input, stop_btn]
    )
    
    stop_btn.click(fn=force_stop, inputs=None, outputs=[user_input, stop_btn], cancels=[sub_1])

if __name__ == "__main__":
    demo.launch(server_name="127.0.0.1", server_port=7860, inbrowser=True)
