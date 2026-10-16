# BloClaw 修复说明（前端 + 功能）

本次在仓库副本上做最小且连贯的修改，已通过 `py_compile` 语法校验、Gradio 5.50 无头启动校验、沙盒 AST 拦截单测。

## 根本原因（最关键）
- **自定义 CSS 此前根本没生效**：原 `web_ui.py` 把 `css=saas_css` 传给了 `demo.launch(...)`，但在 Gradio 5 里 `css` 是 `gr.Blocks(...)` 的构造参数，`launch()` 不接受该参数。结果整份样式表被丢弃/报错 —— 这是“整个页面比例、输入框都不对”的最根本原因。
  - 修正：`gr.Blocks(title="BloClaw OS", css=saas_css)`，`launch()` 不再传 css。

## 前端（web_ui.py）
- **合并三代互相冲突的 CSS** 为单一连贯样式表（青灰-深蓝 App1 视觉）。此前 `:root/body` 背景、`max-width`(1400 vs 1440)、`#welcome_logo img` 尺寸（被定义 4 次）、`.inner-capsule/#composer` 圆角高度等被反复覆盖。
- **输入框选择器修正**：原样式挂在不存在的 `.gradio-multimodal-textbox` 上（底部其实是 `gr.Textbox`），完全失效。现用 `#composer` / `#composer textarea` / `#file_input button` / `#send_btn`，附件、输入、发送三件在胶囊里垂直居中、不再被固定高度裁切。
- **聊天气泡选择器兼容 Gradio 5**：补 `.user-row .message` / `.bot-row .message`，旧的 `.message.user/.bot` 保留做回退。
- **去掉内联样式冲突**：欢迎区 logo/标题/副标题改由 CSS 统一控制（原先 HTML 内联 `3.1rem`、`150px` 与带 `!important` 的 CSS 互相矛盾）。
- **移除死按钮**：顶栏 `EN`、`历史` 无任何事件绑定（点击无反应），已删除；保留可用的 `配置 / 新任务 / 更多`。
- **预设卡片 bug 修复**：`put_text` 原返回 `{"text":..., "files":[]}`（多模态格式）写进纯文本 `gr.Textbox`，会写坏输入框甚至在 `prepare_task` 里 `.strip()` 报错。改为返回纯字符串。

## 功能（bioclaw/core/engine.py）
- **接线微智能体**：`route_task` 现按数据形态走确定性微智能体 —— DNA/RNA → `OmicsAgent`，可解析的 SMILES → `ChemAgent`（含 Lipinski 规则），无结构化数据再回退 LLM。此前两个 agent 是死代码，与 README “LLM 路由意图、agent 做确定性计算”不符。agent 采用惰性加载，纯 Web/LLM 路径不强依赖 rdkit/biopython。
- **沙盒安全校验（兑现 README 的 “AST 安全沙盒”）**：`execute_sandbox` 在 `exec` 前加 `_validate_sandbox_code` 做 AST 静态检查，拦截 `subprocess/socket/ctypes/...` 导入、`os.system/os.remove/...`、`eval/exec/compile/__import__`、以及 `__subclasses__/__globals__` 等逃逸向量；并改为在**独立命名空间**执行（不再 `exec(..., globals())` 污染引擎全局）。
  - 注意：这是**基础防护，非绝对隔离**。真正高安全需求应上 OS 级沙箱（容器/seccomp/gVisor 等）。
- **路径锚定到包**：`tools_path` 改为基于 `__file__` 的 `bioclaw/tools`，不再依赖启动时的 CWD。

## 其他
- 新增 `bioclaw/core/__init__.py`（此前缺失，靠命名空间包勉强可导入）。

## 仍建议处理（未改，属仓库卫生/配置，非本次范围）
- 仓库里提交了多张生成的 `*.png` 和 `bioclaw_stable_v1.tar.gz`，建议清理并加入 `.gitignore`。
- `.env.example` / engine 默认 `DOUBAO_ENDPOINT` 是写死的私人 endpoint，别人用不了，建议置空并在 README 说明。
- `顶栏“更多”` 在未开始对话前切换的右侧光幕位于隐藏的工作区内，点击暂无可见效果（仅对话中有意义），属可接受行为。

## 验证记录
- `python3 -m py_compile web_ui.py engine.py`：通过。
- Gradio 5.50 无头启动：HTTP 200、页面约 377KB、`top_nav/main_stage/welcome_mat/cards_row/chat_panel/canvas_panel/bottom_deck/composer/file_input/send_btn` 全部在组件图中、CSS 已注入、无旧多模态选择器残留。
- 沙盒 AST 拦截：subprocess / os.system / os.remove / eval / `__subclasses__` / 语法错误均被正确拦截；正常 plotly、matplotlib、os.path 用法放行。
- 未做实机浏览器视觉回归（沙盒无法把本机浏览器画面投给你），CSS 冲突与选择器失配属确定性修复，气泡实际观感建议你本地跑一次确认。
