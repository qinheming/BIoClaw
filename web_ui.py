import os
import gradio as gr
from bioclaw.core.engine import BloClawCoordinator
import time

print("🚀 正在唤醒 BloClaw Canvas [极简生产力工作站版]...")
engine = BloClawCoordinator()

# 🍏 苹果/Notion级极简高定 CSS：极度干净、专注、专业
saas_css = """
<style>
/* 整个页面纯净的淡灰背景，突出白色卡片 */
:root, body, .gradio-container { background-color: #f9fafb !important; max-width: 96% !important; margin: 0 auto !important; padding-top: 20px !important; font-family: -apple-system, system-ui, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif !important; }

/* 顶置指挥坞：仿 Mac Spotlight 搜索栏的悬浮输入框 */
#command_deck {
    background: #ffffff !important; border: 1px solid #e5e7eb !important; border-radius: 16px !important;
    box-shadow: 0 4px 20px rgba(0,0,0,0.05) !important; padding: 8px 12px !important; margin-bottom: 24px !important;
}
#command_deck textarea { background: transparent !important; color: #111827 !important; border: none !important; font-size: 16px !important; box-shadow: none !important; }
#command_deck textarea:focus { outline: none !important; box-shadow: none !important; }

/* 聊天气泡极简去边框化 */
#chat_panel { background: transparent !important; border: none !important; margin-right: 15px !important; }

/* 右侧全息画板容器：极简纯白实验室卡片 */
#canvas_panel {
    background: #ffffff !important; border: 1px solid #e5e7eb !important; border-radius: 16px; 
    height: 75vh; overflow: hidden; box-shadow: 0 4px 20px rgba(0,0,0,0.03) !important;
}

footer { display: none !important; }
</style>
"""

# 极简画板待机屏
STANDBY_HTML = """
<div style="height: 100%; display: flex; flex-direction: column; justify-content: center; align-items: center; color: #9ca3af; font-family: system-ui;">
    <svg width="48" height="48" fill="none" stroke="currentColor" stroke-width="1.5" viewBox="0 0 24 24" style="margin-bottom: 15px; opacity: 0.5;"><path stroke-linecap="round" stroke-linejoin="round" d="M14 10l-2 1m0 0l-2-1m2 1v2.5M20 7l-2 1m2-1l-2-1m2 1v2.5M14 4l-2-1-2 1M4 7l2-1M4 7l2 1M4 7v2.5M12 21l-2-1m2 1l2-1m-2 1v-2.5M6 18l-2-1v-2.5M18 18l2-1v-2.5"></path></svg>
    <h3 style="margin: 0; font-weight: 500; letter-spacing: 1px;">Canvas 物理画布视窗</h3>
    <p style="font-size: 13px; margin-top: 8px; opacity: 0.7;">等待渲染 2D拓扑 / 3D全息 信号</p>
</div>
"""

def submit_message(user_message, history):
    if not user_message.strip(): return "", history
    if history is None: history = []
    
    # 🌟 破除阴阳版本错误：强制使用最稳妥的字典交互流，迎合底层 Pydantic！
    history.append({"role": "user", "content": user_message})
    history.append({"role": "assistant", "content": "*(🧬 Agent 构建计算网络中...)*"})
    return "", history 

def engine_response(history):
    if not history: yield history, gr.skip(), gr.skip(); return
    
    user_input = history[-2]["content"]
    res = engine.process_chat(user_input)
    
    history[-1]["content"] = res["text"]
    new_html = res.get("screen_html")
    should_open = bool(new_html)
    
    yield (
        history, 
        gr.update(visible=True) if should_open else gr.skip(), # 如果有图，自动展开右屏
        gr.update(value=new_html) if should_open else gr.skip()
    )

def toggle_panel(current_state):
    """一键自主收起/展开画布权限"""
    new_state = not current_state
    return gr.update(visible=new_state), new_state

with gr.Blocks(title="BloClaw Workspace") as demo:
    gr.HTML(saas_css, visible=False)
    panel_state = gr.State(False)

    # 顶栏标志
    gr.Markdown("### 🧬 BloClaw Canvas <span style='font-size:14px;color:#6b7280;font-weight:normal;margin-left:8px;'>AI4S Agentic Workspace</span>")

    # ================= 🚀 TOP 置顶全效指令舱 =================
    with gr.Group(elem_id="command_deck"):
        with gr.Row(equal_height=True):
            user_input = gr.Textbox(scale=8, show_label=False, placeholder="在此输入自然语言指令、公式或序列...", container=False, lines=2)
            
            with gr.Column(scale=1, min_width=200):
                with gr.Row():
                    submit_btn = gr.Button("解析运行 ↵", variant="primary")
                    toggle_btn = gr.Button("切展画布 ◫", variant="secondary")

    gr.Examples(
        examples=[
            "帮我画出抗抑郁药氟西汀的二维分子图，SMILES：CNCCC(c1ccccc1)Oc2ccc(cc2)C(F)(F)F", 
            "接驳云端算力，计算这串未知序列的三维折叠：MVLSPADKTNVKAAWGKVGAHAGEYGAEALERMF"
        ],
        inputs=[user_input]
    )

    gr.Markdown("<hr style='border-color: #e5e7eb; margin: 15px 0;'>")

    # ================= 🚀 下半部：对话与画板区 =================
    with gr.Row():
        # 左侧对话流
        with gr.Column(scale=6):
            # 🌟 没有任何危险参数的最纯净声明，只负责显示
            chatbot = gr.Chatbot(height="70vh", show_label=False, elem_id="chat_panel")

        # 右侧画布 (默认藏起，极其干净)
        with gr.Column(scale=5, visible=False, elem_id="canvas_panel") as right_panel:
            canvas_screen = gr.HTML(value=STANDBY_HTML, elem_classes="h-full w-full")
            
    # ================= 事件中枢 =================
    # 右上角自主控制开关
    toggle_btn.click(fn=toggle_panel, inputs=[panel_state], outputs=[right_panel, panel_state])

    # 代码提交双管线
    submit_btn.click(fn=submit_message, inputs=[user_input, chatbot], outputs=[user_input, chatbot], queue=False).then(
        fn=engine_response, inputs=[chatbot], outputs=[chatbot, right_panel, canvas_screen]
    )
    user_input.submit(fn=submit_message, inputs=[user_input, chatbot], outputs=[user_input, chatbot], queue=False).then(
        fn=engine_response, inputs=[chatbot], outputs=[chatbot, right_panel, canvas_screen]
    )

if __name__ == "__main__":
    demo.launch(server_name="127.0.0.1", server_port=7860, inbrowser=True)
