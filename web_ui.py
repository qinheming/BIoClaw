import os
import base64
import gradio as gr
from bioclaw.core.engine import BloClawCoordinator

print("🚀 正在唤醒 BloClaw OS [真·沉浸纯粹去键无框版]...")
engine = BloClawCoordinator()
LOGO_PATH = os.path.join(os.path.dirname(__file__), "assets", "bloclaw-logo.jpg")
with open(LOGO_PATH, "rb") as logo_file:
    LOGO_DATA_URI = "data:image/jpeg;base64," + base64.b64encode(logo_file.read()).decode("ascii")

saas_css = """
/* 整个页面纯净布局，最高限宽拉大，给左屏和光幕预留广袤空间 */
:root, body, .gradio-container { background-color: #ffffff !important; max-width: 1400px !important; margin: 0 auto !important; font-family: -apple-system, system-ui, sans-serif !important; height: 100vh !important; display: flex; flex-direction: column; overflow: hidden; padding: 0 !important;}
footer { display: none !important; }

/* 顶置导航 */
#top_nav { border-bottom: 1px solid #f3f4f6 !important; padding: 10px 25px !important; align-items: center !important; flex-shrink: 0 !important; }

#main_stage { flex-grow: 1 !important; overflow-y: auto !important; display: flex; flex-direction: column; padding: 2vh 2%; }

/* 居中首屏Logo与神坛 */
#welcome_mat { margin: auto !important; display: flex; flex-direction: column; align-items: center; justify-content: center; width: 100%;}
#welcome_logo { width: 100% !important; display: flex !important; justify-content: center !important; margin: 0 auto 10px !important; }
#welcome_logo img { width: 150px !important; height: 150px !important; aspect-ratio: 1 !important; object-fit: contain !important; display: block !important; }

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
/* App1 visual language */
:root { --app-canvas:#f5f7fb; --app-surface:#fff; --app-line:#d8e0ea; --app-line-strong:#bdc9d8; --app-text:#142033; --app-muted:#64748b; --app-accent:#087f8c; --app-navy:#132238; }
body, .gradio-container { background:var(--app-canvas) !important; color:var(--app-text) !important; }
.gradio-container { max-width:1440px !important; }
#top_nav { background:var(--app-surface) !important; border-bottom:1px solid var(--app-line) !important; padding:16px 24px !important; }
#top_nav button, #canvas_toolbar button { border:1px solid var(--app-line-strong) !important; border-radius:8px !important; background:var(--app-surface) !important; color:var(--app-navy) !important; box-shadow:none !important; }
#top_nav button:hover, #canvas_toolbar button:hover { border-color:var(--app-accent) !important; background:#eefbfb !important; }
#top_nav button.primary, .gradio-accordion button.primary { background:var(--app-accent) !important; border-color:var(--app-accent) !important; color:#fff !important; }
#main_stage { padding:18px 24px !important; }
#welcome_mat { max-width:1120px !important; gap:12px !important; }
#welcome_logo { margin:0 auto 8px !important; }
#welcome_logo img { width:150px !important; height:150px !important; }
#welcome_mat h1 { color:var(--app-navy) !important; font-size:clamp(2rem, 4vw, 2.8rem) !important; }
#welcome_mat .prose p { color:var(--app-accent) !important; }
#cards_row { max-width:1120px !important; gap:10px !important; }
#cards_row button { min-height:86px !important; border:1px solid var(--app-line) !important; border-radius:8px !important; background:var(--app-surface) !important; color:var(--app-text) !important; box-shadow:none !important; font-size:13px !important; font-weight:700 !important; text-align:left !important; transition:border-color .15s ease, background .15s ease !important; }
#cards_row button:hover { border-color:#b9dcde !important; background:#eefbfb !important; transform:none !important; box-shadow:none !important; }
#chat_panel { background:var(--app-surface) !important; border:1px solid var(--app-line) !important; border-radius:8px !important; }
#chat_panel .message.user { background:#f1fbfb !important; border:1px solid #b4d9dd !important; border-radius:8px !important; color:var(--app-text) !important; box-shadow:none !important; }
#canvas_panel { border:1px solid #b9dcde !important; border-radius:8px !important; background:#f8fafc !important; box-shadow:0 18px 42px rgba(19,34,56,.12) !important; }
#canvas_toolbar { border-bottom:1px solid var(--app-line) !important; }
.gradio-accordion { border:1px solid var(--app-line) !important; border-radius:8px !important; background:var(--app-surface) !important; margin:0 24px 4px !important; }
.gradio-accordion input:focus, .gradio-accordion textarea:focus { border-color:var(--app-accent) !important; box-shadow:0 0 0 3px rgba(8,127,140,.14) !important; }
#bottom_deck { padding:12px 24px 22px !important; background:var(--app-canvas) !important; }
.inner-capsule { max-width:1120px !important; border:1px solid var(--app-line-strong) !important; border-radius:8px !important; background:var(--app-surface) !important; box-shadow:0 10px 24px rgba(19,34,56,.08) !important; padding:10px !important; }
.inner-capsule:focus-within { border-color:var(--app-accent) !important; box-shadow:0 0 0 3px rgba(8,127,140,.14) !important; }
@media (max-width:760px) {
    #top_nav, #main_stage { padding-left:14px !important; padding-right:14px !important; }
    #top_nav { flex-wrap:wrap !important; gap:8px !important; }
    #cards_row { flex-wrap:wrap !important; }
    #cards_row button { min-width:100% !important; }
    .gradio-accordion { margin-left:14px !important; margin-right:14px !important; }
    #bottom_deck { padding-left:14px !important; padding-right:14px !important; }
}

/* app1 compact workbench proportions */
#main_stage { overflow-y:auto !important; }
#welcome_mat { margin:0 auto !important; padding:22px 0 10px !important; gap:8px !important; }
#welcome_logo { margin:0 auto 2px !important; }
#welcome_logo img { width:96px !important; height:96px !important; }
#welcome_mat h1 { font-size:32px !important; line-height:1.15 !important; }
#welcome_mat .prose p { font-size:15px !important; padding-bottom:10px !important; }
#cards_row { align-items:stretch !important; }
#cards_row button { min-height:76px !important; height:76px !important; padding:12px 16px !important; line-height:1.45 !important; white-space:normal !important; overflow-wrap:anywhere !important; }
#bottom_deck { padding:10px 24px 18px !important; }
#bottom_deck .inner-capsule { min-height:0 !important; height:auto !important; padding:8px 12px !important; }
#composer { min-height:80px !important; height:80px !important; }
#composer > div { align-items:center !important; }
#composer textarea { min-height:48px !important; height:48px !important; max-height:96px !important; width:100% !important; padding:12px !important; text-align:left !important; line-height:1.45 !important; }
#file_input button { min-width:48px !important; width:48px !important; height:48px !important; border:1px solid var(--app-line-strong) !important; border-radius:8px !important; background:#fff !important; color:var(--app-navy) !important; font-size:20px !important; }
#send_btn { min-width:48px !important; height:48px !important; border-radius:8px !important; background:var(--app-accent) !important; color:#fff !important; font-size:22px !important; }
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
        gr.update(value="", interactive=True, placeholder="💡 输入研究任务…"),
        gr.update(value=None),
    )

def prepare_task(text, files, history):
    text = text or ""
    files = files or []
    
    if not text.strip() and not files:
        empty_payload = {"pure_text": "", "pure_files": []}
        return gr.update(), gr.update(), history, gr.update(), gr.update(), gr.update(), empty_payload
        
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
        gr.update(value="", interactive=False, placeholder="⏳ 正在处理…"),
        gr.update(value=None),
        history,
        gr.update(visible=False),  # welcome_block (隐藏大 Logo)
        gr.update(visible=True),   # workspace_block (展现聊天瀑布)
        gr.update(visible=True),   # stop_btn (浮现红区悬浮按键！)
        payload                    
    )

def execute_task(history, payload):
    if not payload: 
        yield history, gr.skip(), gr.skip(), gr.update(interactive=True), gr.update(), gr.update(visible=False); return
    
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
        gr.update(interactive=True, placeholder="💡 输入研究任务…"),
        gr.update(value=None),
        gr.update(visible=False) # 红色急停钮隐匿！
    )

def force_stop():
    return (
        gr.update(interactive=True, placeholder="🛑 已中断，输入新任务…"),
        gr.update(value=None),
        gr.update(visible=False)
    )

def toggle_right_panel(is_open):
    new_state = not is_open
    return gr.update(visible=new_state), new_state

def close_right_panel():
    return gr.update(visible=False), False

def put_text(text):
    return gr.update(value={"text": text, "files": []})


LLM_PRESETS = {
    "OpenAI / 兼容接口": "https://api.openai.com/v1",
    "豆包": "https://ark.cn-beijing.volces.com/api/v3",
    "OpenRouter": "https://openrouter.ai/api/v1",
    "Ollama (本地)": "http://127.0.0.1:11434/v1",
    "自定义": "",
}


def select_provider(provider):
    return gr.update(value=LLM_PRESETS.get(provider, ""))


def apply_llm_config(provider, base_url, model_name, api_key):
    try:
        config = engine.configure_llm(provider, base_url, model_name, api_key)
        key_state = "已设置 API Key" if config["has_api_key"] else "未设置 API Key"
        return f"已应用 {config['provider']} · {config['model_name']} · {key_state}", gr.update()
    except Exception as exc:
        return f"配置未保存：{exc}", gr.update()

with gr.Blocks(title="BloClaw OS") as demo:
    task_payload = gr.State()
    is_panel_open = gr.State(False) 

    # ================= 🌌 顶置全局导航栏 =================
    with gr.Row(elem_id="top_nav"):
        gr.Markdown("<span style='font-size:18px; font-weight:bold; color:#0f172a;'>BloClaw.</span> <span style='font-size:13px;color:#64748b;'>The Ultimate Autonomous AI Scientist.</span>")
        with gr.Row():
            toggle_panel_btn = gr.Button("◫ 切控视界幕布", variant="secondary", size="sm")
            new_chat_btn = gr.Button("➕ 构建新纪元", variant="primary", size="sm")

    with gr.Accordion("⚙ 模型 API 设置", open=False):
        with gr.Row():
            llm_provider = gr.Dropdown(
                choices=list(LLM_PRESETS), value=engine.provider, label="服务商", scale=2
            )
            llm_base_url = gr.Textbox(value=engine.base_url, label="API Base", scale=4)
            llm_model = gr.Textbox(value=engine.model_name, label="模型名称", scale=3)
            llm_api_key = gr.Textbox(label="API Key（留空保持当前）", type="password", scale=3)
        with gr.Row():
            save_llm_btn = gr.Button("保存并应用", variant="primary", size="sm")
            llm_status = gr.Markdown("当前使用启动配置。")

    # ================= 🌌 主干舞台 =================
    with gr.Column(elem_id="main_stage"):
        
        # 居中神坛
        with gr.Column(elem_id="welcome_mat") as welcome_block:
            gr.HTML(
                f'<div id="welcome_logo" style="width:100%;display:flex;justify-content:center;align-items:center;">'
                f'<img src="{LOGO_DATA_URI}" alt="BloClaw Logo" width="150" height="150" '
                'style="width:150px;height:150px;object-fit:contain;display:block;"></div>'
            )
            gr.Markdown("<h1 style='font-size:2.8rem; color:#0f172a; margin:0; text-align:center;'>BloClaw</h1>")
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
                chatbot_kwargs = {"show_label": False, "container": False, "elem_id": "chat_panel"}
                try:
                    chatbot = gr.Chatbot(**chatbot_kwargs, type="messages")
                except TypeError:
                    chatbot = gr.Chatbot(**chatbot_kwargs)
                
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

        with gr.Group(elem_id="composer", elem_classes="inner-capsule"):
            with gr.Row(equal_height=True, elem_classes="items-center w-full h-full"):
                file_input = gr.UploadButton("📎", file_count="multiple", file_types=[".pdf", ".txt", ".csv", ".md", ".xlsx", ".xls"], type="filepath", size="sm", scale=1, min_width=48, elem_id="file_input")
                user_input = gr.Textbox(
                    scale=8, show_label=False, container=False, lines=1, max_lines=3,
                    placeholder="💡 输入研究任务…",
                )
                send_btn = gr.Button("↑", variant="primary", elem_id="send_btn", scale=1, min_width=48)


    # ================= 🚀 数据流与雷达绑定 =================
    new_chat_btn.click(fn=reset_session, inputs=None, outputs=[chatbot, task_payload, welcome_block, workspace_block, right_panel, canvas_screen, user_input, file_input])
    toggle_panel_btn.click(fn=toggle_right_panel, inputs=[is_panel_open], outputs=[right_panel, is_panel_open])
    close_canvas_btn.click(fn=close_right_panel, inputs=None, outputs=[right_panel, is_panel_open])
    llm_provider.change(fn=select_provider, inputs=[llm_provider], outputs=[llm_base_url])
    save_llm_btn.click(
        fn=apply_llm_config,
        inputs=[llm_provider, llm_base_url, llm_model, llm_api_key],
        outputs=[llm_status, llm_api_key],
    )

    for btn, cmd in [(card1, cmd1), (card2, cmd2), (card3, cmd3)]:
        btn.click(fn=put_text, inputs=[cmd], outputs=[user_input]).then(
            fn=prepare_task, inputs=[user_input, file_input, chatbot], outputs=[user_input, file_input, chatbot, welcome_block, workspace_block, stop_btn, task_payload], queue=False
        ).then(
            fn=execute_task, inputs=[chatbot, task_payload], outputs=[chatbot, right_panel, canvas_screen, user_input, file_input, stop_btn]
        )

    # 唯一的管线输出渠道，直接由大文本框组件敲回车引发！
    sub_1 = user_input.submit(
        fn=prepare_task, inputs=[user_input, file_input, chatbot], outputs=[user_input, file_input, chatbot, welcome_block, workspace_block, stop_btn, task_payload], queue=False
    ).then(
        fn=execute_task, inputs=[chatbot, task_payload], outputs=[chatbot, right_panel, canvas_screen, user_input, file_input, stop_btn]
    )

    send_btn.click(
        fn=prepare_task, inputs=[user_input, file_input, chatbot], outputs=[user_input, file_input, chatbot, welcome_block, workspace_block, stop_btn, task_payload], queue=False
    ).then(
        fn=execute_task, inputs=[chatbot, task_payload], outputs=[chatbot, right_panel, canvas_screen, user_input, file_input, stop_btn]
    )
    
    stop_btn.click(fn=force_stop, inputs=None, outputs=[user_input, file_input, stop_btn], cancels=[sub_1])

if __name__ == "__main__":
    demo.launch(server_name="127.0.0.1", server_port=7860, inbrowser=True, css=saas_css)
