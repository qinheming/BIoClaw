import os
import base64
import gradio as gr
from bioclaw.core.engine import BloClawCoordinator

print("🚀 正在唤醒 BloClaw OS ...")
engine = BloClawCoordinator()
LOGO_PATH = os.path.join(os.path.dirname(__file__), "assets", "bloclaw-logo.jpg")
with open(LOGO_PATH, "rb") as logo_file:
    LOGO_DATA_URI = "data:image/jpeg;base64," + base64.b64encode(logo_file.read()).decode("ascii")

# ================= 🎨 单一连贯样式表 =================
# 说明：此前这里堆叠了三代互相覆盖的 CSS（背景/最大宽度/logo 尺寸/输入框被重复定义多次），
# 现在合并为一套 App1 的青灰-深蓝视觉语言，避免数值互相打架。
saas_css = """
:root {
    --app-canvas:#ffffff; --app-surface:#ffffff; --app-line:#d8e0ea;
    --app-line-strong:#bdc9d8; --app-text:#142033; --app-muted:#64748b;
    --app-accent:#087f8c; --app-accent-soft:#eefbfb; --app-navy:#132238;
}

/* —— 整体外壳 —— */
html, body, #root {
    width:100% !important; min-width:0 !important; min-height:100% !important;
    margin:0 !important; background:#fff !important;
}
body { overflow-x:hidden !important; }
.gradio-container {
    width:100% !important; max-width:none !important; margin:0 !important;
    background:#fff !important; color:var(--app-text) !important;
    font-family:-apple-system, system-ui, "Segoe UI", sans-serif !important;
    min-height:100vh !important; display:flex !important; flex-direction:column !important;
    padding:0 !important;
}
.gradio-container > .main { width:100% !important; max-width:none !important; padding:0 !important; }
footer { display:none !important; }

/* —— 顶部导航 —— */
#top_nav {
    background:var(--app-surface) !important; border-bottom:1px solid var(--app-line) !important;
    padding:12px 24px !important; align-items:center !important; flex-shrink:0 !important;
    justify-content:space-between !important; flex-wrap:wrap !important; gap:8px !important;
}
#top_nav button {
    min-width:84px !important; height:38px !important;
    border:1px solid var(--app-line-strong) !important; border-radius:8px !important;
    background:var(--app-surface) !important; color:var(--app-navy) !important;
    box-shadow:none !important; font-weight:600 !important;
}
#top_nav button:hover { border-color:var(--app-accent) !important; background:var(--app-accent-soft) !important; }

/* —— 模型设置折叠面板 —— */
.gradio-accordion {
    border:1px solid var(--app-line) !important; border-radius:8px !important;
    background:var(--app-surface) !important; margin:8px 24px 0 !important;
}
.gradio-accordion input:focus, .gradio-accordion textarea:focus {
    border-color:var(--app-accent) !important; box-shadow:0 0 0 3px rgba(8,127,140,.14) !important;
}
.gradio-accordion button.primary { background:var(--app-accent) !important; border-color:var(--app-accent) !important; color:#fff !important; }

/* —— 主干舞台 —— */
#main_stage {
    flex:1 1 auto !important; overflow-y:auto !important; padding:20px 24px !important;
    display:flex; flex-direction:column; background:#fff !important;
}

/* —— 首屏欢迎 —— */
#welcome_mat {
    margin:auto !important; width:100%; max-width:1200px;
    display:flex; flex-direction:column; align-items:center; gap:10px;
}
#welcome_logo { display:flex !important; justify-content:center !important; margin:0 auto 4px !important; }
#welcome_logo img { width:104px !important; height:104px !important; object-fit:contain !important; display:block !important; }
#welcome_mat h1 {
    margin:0 !important; text-align:center !important; color:var(--app-navy) !important;
    font-size:34px !important; line-height:1.15 !important; font-weight:800 !important;
}
#welcome_mat .prose p {
    margin:0 !important; text-align:center !important; color:var(--app-accent) !important;
    font-size:15px !important; font-weight:600 !important; padding-bottom:12px !important;
}

/* —— 任务卡片：桌面不折行，移动端折行 —— */
#cards_row { display:flex !important; flex-wrap:nowrap !important; width:100%; gap:12px; align-items:stretch; }
#cards_row > div { min-width:0 !important; flex:1 1 0 !important; }
#cards_row button {
    flex:1 1 0 !important; min-width:0 !important; width:100% !important; min-height:88px !important;
    border:1px solid var(--app-line) !important; border-radius:12px !important;
    background:#fff !important; color:var(--app-text) !important;
    box-shadow:none !important; font-size:14px !important; font-weight:700 !important;
    text-align:center !important; line-height:1.4 !important; padding:12px 14px !important;
    white-space:normal !important; overflow-wrap:anywhere !important;
    transition:border-color .15s ease, background .15s ease, transform .15s ease !important;
}
#cards_row button:hover { border-color:#83cfe0 !important; background:var(--app-accent-soft) !important; transform:translateY(-2px) !important; }

/* —— 工作区：聊天 + 右侧光幕 —— */
#chat_panel {
    background:var(--app-surface) !important; border:1px solid var(--app-line) !important;
    border-radius:12px !important; min-height:52vh !important; max-height:70vh !important;
    overflow-y:auto !important; padding:8px !important; margin-right:12px !important;
}
#canvas_panel {
    border:1px solid #b9dcde !important; border-radius:12px !important; background:#fff !important;
    box-shadow:0 18px 42px rgba(19,34,56,.12) !important; height:72vh !important;
    overflow:hidden !important; display:flex !important; flex-direction:column !important;
    flex-wrap:nowrap !important; min-height:0 !important;
}
#canvas_panel > div:last-child {
    width:100% !important; min-width:0 !important; min-height:0 !important;
    flex:1 1 auto !important; overflow:hidden !important;
}
#canvas_panel .html-container, #canvas_panel .html-container > .prose {
    width:100% !important; height:100% !important; min-height:0 !important;
    overflow:hidden !important;
}
#canvas_toolbar {
    border-bottom:1px solid var(--app-line) !important; padding:8px 12px !important;
    align-items:center !important; background:var(--app-surface) !important;
}

/* 聊天气泡（Gradio 5 的 DOM，兼顾新旧类名，缺失时优雅回退） */
#chat_panel .user-row .message, #chat_panel .message.user {
    background:var(--app-accent-soft) !important; border:1px solid #b4d9dd !important;
    border-radius:12px !important; color:var(--app-text) !important;
}
#chat_panel .bot-row .message, #chat_panel .message.bot {
    background:transparent !important; border:none !important; color:#1e293b !important;
}

/* —— 底部输入舱 —— */
#bottom_deck {
    flex-shrink:0 !important; background:#fff !important;
    padding:12px 24px 22px !important; position:relative;
}
#stop_btn_container {
    position:absolute !important; top:-16px !important; left:50% !important;
    transform:translateX(-50%) !important; z-index:50;
}
/* 输入舱外壳（gr.Group#composer，此前错把样式挂在不存在的多模态类上） */
#composer {
    width:100% !important; max-width:1200px !important; margin:0 auto !important;
    background:var(--app-surface) !important; border:1px solid var(--app-line-strong) !important;
    border-radius:16px !important; box-shadow:0 10px 24px rgba(19,34,56,.08) !important;
    padding:8px 10px !important;
}
#composer:focus-within { border-color:var(--app-accent) !important; box-shadow:0 0 0 3px rgba(8,127,140,.14) !important; }
#composer > div { display:flex !important; align-items:center !important; gap:8px !important; width:100% !important; }
#composer textarea {
    border:none !important; background:transparent !important; box-shadow:none !important; outline:none !important;
    font-size:15px !important; line-height:1.5 !important; padding:10px 6px !important;
    min-height:44px !important; max-height:120px !important; resize:none !important; width:100% !important;
}
#file_input button, #send_btn {
    min-width:44px !important; width:44px !important; height:44px !important; flex:0 0 44px !important;
    border-radius:10px !important; font-size:20px !important; padding:0 !important;
}
#file_input, #file_input > div {
    width:44px !important; min-width:44px !important; max-width:44px !important;
    flex:0 0 44px !important; background:#fff !important;
}
#file_input button { border:1px solid var(--app-line-strong) !important; background:#fff !important; color:var(--app-navy) !important; }
#send_btn { border:none !important; background:var(--app-accent) !important; color:#fff !important; }
#send_btn:hover { background:#0a6f7a !important; }

/* —— 响应式 —— */
@media (max-width:760px) {
    #top_nav, #main_stage, #bottom_deck { padding-left:14px !important; padding-right:14px !important; }
    #cards_row { flex-wrap:wrap !important; }
    #cards_row button { flex:1 1 100% !important; min-width:100% !important; }
    #chat_panel { margin-right:0 !important; }
    #canvas_panel { height:50vh !important; }
}
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
    # 底部是 gr.Textbox（纯文本），其 value 必须是字符串；
    # 此前返回 {"text": ..., "files": []} 是多模态组件格式，会让预设卡片写坏输入框甚至报错。
    return gr.update(value=text)


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

def open_llm_settings():
    return gr.update(visible=True, open=True)

with gr.Blocks(title="BloClaw OS", css=saas_css) as demo:
    task_payload = gr.State()
    is_panel_open = gr.State(False)

    # ================= 🌌 顶置全局导航栏 =================
    # 注：原先的 EN / 历史 两个按钮没有任何事件绑定（点击无反应），已移除以免误导；
    # 留下的 配置 / 新任务 / 更多 均有实际功能。
    with gr.Row(elem_id="top_nav"):
        gr.Markdown("<span style='font-size:20px; font-weight:800; color:#142033;'>🧬 BloClaw Matrix</span>")
        with gr.Row():
            config_btn = gr.Button("配置", variant="secondary", size="sm")
            new_chat_btn = gr.Button("新任务", variant="secondary", size="sm")
            toggle_panel_btn = gr.Button("更多", variant="secondary", size="sm")

    with gr.Accordion("模型 API 设置", open=False, visible=False) as llm_settings:
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
                f'<div id="welcome_logo"><img src="{LOGO_DATA_URI}" alt="BloClaw Logo"></div>'
            )
            gr.Markdown("# BloClaw Matrix")
            gr.Markdown("AI4S 超级智能工作站")

            with gr.Row(elem_id="cards_row"):
                card1 = gr.Button("创新药研发", elem_classes="matrix-card")
                card2 = gr.Button("生物信息与组学分析", elem_classes="matrix-card")
                card3 = gr.Button("医学与科研写作", elem_classes="matrix-card")
                card4 = gr.Button("科研情报与证据检索", elem_classes="matrix-card")
                card5 = gr.Button("项目管理与实验闭环", elem_classes="matrix-card")

            cmd1 = gr.Textbox(value="帮我画出抗抑郁药氟西汀的二维分子图，SMILES：CNCCC(c1ccccc1)Oc2ccc(cc2)C(F)(F)F", visible=False)
            cmd2 = gr.Textbox(value="计算这串未知生命序列的三维折叠与力场：MVLSPADKTNVKAAWGKVGAHAGEYGAEALERMF", visible=False)
            cmd3 = gr.Textbox(value="使用 numpy 为我设计一整套生物种群繁衍和演进数据的『逻辑斯蒂回归热力图 (Logistic Growth)』，并用 plotly 或 seaborn 等在沙盒生成高质图线供我研究（不能有废话！必含图源结果！）。", visible=False)
            cmd4 = gr.Textbox(value="检索并整理一个科研主题的最新证据、关键文献和验证路径。", visible=False)
            cmd5 = gr.Textbox(value="为当前项目建立实验计划、里程碑、风险清单和可复核交付记录。", visible=False)

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
    config_btn.click(fn=open_llm_settings, inputs=None, outputs=[llm_settings])
    save_llm_btn.click(
        fn=apply_llm_config,
        inputs=[llm_provider, llm_base_url, llm_model, llm_api_key],
        outputs=[llm_status, llm_api_key],
    )

    for btn, cmd in [(card1, cmd1), (card2, cmd2), (card3, cmd3), (card4, cmd4), (card5, cmd5)]:
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
    demo.launch(server_name="127.0.0.1", server_port=7860, inbrowser=True)
