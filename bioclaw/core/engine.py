import os
import re
import io
import html
import base64
import traceback
import requests
import glob
from contextlib import redirect_stdout
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

class BloClawCoordinator:
    def __init__(self):
        self.api_key = os.getenv("DOUBAO_API_KEY")
        self.base_url = "https://ark.cn-beijing.volces.com/api/v3"
        self.model_name = os.getenv("DOUBAO_ENDPOINT", "ep-20250222165018-9xts8")
        if not self.api_key:
            self.api_key = os.getenv("OPENAI_API_KEY", "")
            self.base_url = "https://api.openai.com/v1"
            self.model_name = "gpt-3.5-turbo"
        self.client = OpenAI(api_key=self.api_key, base_url=self.base_url)
        self.tools_path = os.path.abspath("bioclaw/tools")

    def clean_code(self, raw_code):
        if not raw_code: return ""
        code = raw_code.strip()
        if code.startswith("```"):
            code = re.sub(r"^```[a-zA-Z]*\n?", "", code)
            code = re.sub(r"\n?```$", "", code).strip()
        return code

    def extract_tag(self, text, tag):
        pattern = f"<{tag}>(.*?)</{tag}>"
        match = re.search(pattern, text, re.DOTALL | re.IGNORECASE)
        return match.group(1).strip() if match else ""

    def execute_sandbox(self, python_code):
        output_buffer = io.StringIO()
        html_file = os.path.abspath("sandbox_plot.html")
        png_file = os.path.abspath("sandbox_plot.png")
        
        # 战前扫清残骸，防止大模型偷懒直接用了上次生成的图
        if os.path.exists(html_file): os.remove(html_file)
        if os.path.exists(png_file): os.remove(png_file)
        
        success = True; error_msg = ""
        try:
            with redirect_stdout(output_buffer):
                # 🌟 剥除花里胡哨的底层劫持，我们用最干净原生的沙盒跑大模型自己写的完美代码！
                # 唯一就是预加载一下常用包，节省时间。
                preset_env = """
import os, re, requests, base64
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import plotly.express as px
import plotly.graph_objects as go
import seaborn as sns
import warnings
warnings.filterwarnings('ignore')
plt.rcParams['figure.figsize'] = (10, 6)
"""
                safe_code = python_code
                # 剔除阻塞性的展示函数
                safe_code = re.sub(r"fig\.show\(\)|plt\.show\(\)|figure\.show\(\)", "", safe_code)
                
                exec(preset_env + safe_code, globals())
        except Exception as e:
            success = False; error_msg = traceback.format_exc()
            
        plot_html = None
        plot_img = None
        
        # 🌟 简单的寻找即可：既然在大模型规则里逼它写死了保存名，查就是了！
        if os.path.exists(html_file):
            with open(html_file, "r", encoding="utf-8") as f:
                plot_html = f.read()
        elif os.path.exists(png_file):
            plot_img = png_file

        return {"success": success, "stdout": output_buffer.getvalue().strip(), "error": error_msg, "plot_html": plot_html, "plot_path": plot_img}

    def generate_rdkit_2d_html(self, raw_target):
        try:
            from rdkit import Chem; from rdkit.Chem import Draw
            pure_smiles = max(re.findall(r'[A-Za-z0-9@+\-\[\]\.\(\)\=\#\/\\]{4,}', raw_target), key=len)
            if pure_smiles.endswith("OH"): pure_smiles = pure_smiles[:-1] 
            mol = Chem.MolFromSmiles(pure_smiles)
            if not mol: return None
            path = os.path.abspath("temp_mol.png")
            Draw.MolToFile(mol, path, size=(800, 600))
            with open(path, "rb") as f: b64 = base64.b64encode(f.read()).decode('utf-8')
            return f"<div style='height:100vh; display:flex; align-items:center; justify-content:center; background:#fafafa;'><img src='data:image/png;base64,{b64}' style='max-width:98%; max-height:98%; border-radius:12px; box-shadow:0 6px 25px rgba(0,0,0,0.08); border:1px solid #e5e7eb; background:white; padding:10px;'></div>"
        except: return None

    def generate_docking_iframe(self, pdb_id, smiles):
        pdb = re.sub(r'[^a-zA-Z0-9]', '', pdb_id).lower()
        if len(pdb) > 4: pdb = pdb[-4:] 
        pure_smiles = max(re.findall(r'[A-Za-z0-9@+\-\[\]\.\(\)\=\#\/\\]{4,}', smiles), key=len)
        try:
            from rdkit import Chem; from rdkit.Chem import AllChem; import base64
            m = Chem.MolFromSmiles(pure_smiles); m = Chem.AddHs(m); 
            if AllChem.EmbedMolecule(m, randomSeed=1) == -1: AllChem.Compute2DCoords(m)
            sdf_block = Chem.MolToMolBlock(m)
            b64_sdf = base64.b64encode(sdf_block.encode('utf-8')).decode('utf-8')
            script = f"var v = $3Dmol.createViewer('g', {{backgroundColor:'#ffffff'}}); $3Dmol.download('pdb:{pdb}', v, {{}}, function() {{ v.setStyle({{}}, {{cartoon: {{color: 'spectrum', opacity: 0.6}}}}); var sdf_data = atob('{b64_sdf}'); v.addModel(sdf_data, 'sdf'); v.setStyle({{model: -1}}, {{stick: {{colorscheme: 'greenCarbon', radius: 0.3}}, sphere: {{radius: 0.6}}}}); v.zoomTo(); v.render(); }});"
            html_src = f"<html><head><script src='https://3Dmol.csb.pitt.edu/build/3Dmol-min.js'></script></head><body style='margin:0;'><div id='g' style='width:100vw; height:100vh;'></div><script>{script}</script></body></html>"
            return f"<iframe srcdoc='{html.escape(html_src)}' style='width:100%; height:100vh; border:none;'></iframe>"
        except Exception as e: return f"<div style='height:100vh; display:flex; align-items:center; justify-content:center; color:#ef4444; font-family:monospace; background:#fef2f2; padding:20px;'><br>{str(e)}</div>"

    def generate_3d_iframe(self, core_data, is_custom=False, pdb_str=None):
        if not is_custom:
            pdb = re.sub(r'[^a-zA-Z0-9]', '', core_data).lower()
            return f"<iframe src='https://3dmol.csb.pitt.edu/viewer.html?pdb={pdb}&style=cartoon;color:spectrum&spin=true&bcolor=ffffff' style='width:100%; height:100vh; border:none;'></iframe>"
        else:
            escaped_pdb = pdb_str.replace("`", "")
            script = f"var v = $3Dmol.createViewer('g', {{backgroundColor:'#ffffff'}}); v.addModel(`{escaped_pdb}`, 'pdb'); v.setStyle({{}}, {{cartoon:{{color:'spectrum'}}}}); v.zoomTo(); v.render();"
            html_src = f"<html><head><script src='https://3Dmol.csb.pitt.edu/build/3Dmol-min.js'></script></head><body style='margin:0;'><div id='g' style='width:100vw; height:100vh;'></div><script>{script}</script></body></html>"
            return f"<iframe srcdoc='{html.escape(html_src)}' style='width:100%; height:100vh; border:none;'></iframe>"

    def process_chat(self, user_message, uploaded_files=None, memory_context=None):
        file_context = ""
        evolved_tools = [f.replace(".py", "") for f in os.listdir(self.tools_path) if f.endswith(".py")] if os.path.exists(self.tools_path) else []
        if uploaded_files:
            file_context += "\n\n【隐秘沙盒挂载资产】\n"
            for f in uploaded_files:
                path = f if isinstance(f, str) else getattr(f, 'filepath', getattr(f, 'name', str(f)))
                ext = os.path.splitext(path)[1].lower()
                try:
                    if ext == '.pdf':
                        import PyPDF2
                        with open(path, 'rb') as pf: file_context += f"📰[文献提取]:\n{''.join([p.extract_text() for p in PyPDF2.PdfReader(pf).pages[:4]])[:1500]}\n"
                    elif ext in ['.xlsx', '.xls']:
                        import pandas as pd
                        df = pd.read_excel(path); heads = ", ".join(df.columns.tolist())
                        file_context += f"📊[Excel数据探针]: {path}\n表头({heads}), 预览:\n{df.head(6).to_string()}\n"
                    elif ext in ['.txt', '.csv', '.md']:
                        with open(path, 'r', encoding='utf-8') as tf: file_context += f"📄[提取文本数据]:\n{tf.read()[:3000]}\n"
                except: pass
        
        final_prompt = str(user_message) + file_context

        # 🌟 最暴君的死命令指令：由大模型全权负责将网页端渲染写死进物理磁盘！
        sys_prompt = f"""你是科研主脑 BloClaw。具备超长的记忆推理能力。
【动作指配法则】
1. TEXT: 直接文本解答。
2. PYTHON_SANDBOX: ✨启动无敌沙盒绘图或运算。
🚨🚨【生死铁律】: 如果你要画能够让用户鼠标互动的极高画质网页图，请强制使用 `import plotly.express as px`。
并且，在所有绘图代码写完的【最后一行】，你【必须、务必、硬性要求】把你画的图表保存下来供前端获取：
如果用的是 plotly，那么你的最后一句代码不可违背地必须是：`fig.write_html('sandbox_plot.html', include_plotlyjs='cdn', full_html=True)` 
如果用的是 numpy/matplotlib/seaborn 等，那么最后一句一定是：`plt.savefig('sandbox_plot.png', bbox_inches='tight')`。
绝不做任何隐瞒，你写了才能给主人看！

3. 2D_MOLECULE: 写纯 SMILES。
4. 3D_PROTEIN: 展示已知自然生物蛋白(填PDB)。
5. FOLD_PROTEIN: 云端折叠大分子未见序列。
6. MOLECULAR_DOCKING: 模拟对接。填: [PDB纯编号]|||[SMILES纯序列]。
7. CREATE_TOOL: 在本地繁衍系统脚本。第一行名字，后面源码。

必须严格用此四组 XML 输出：
<thought>短思考</thought>
<action>填入大写的上述任意一项参数</action>
<target>如果是沙盒这块一定填入携带保存指令的最纯正 Python 代码！</target>
<reply>详实的学术解析。不用复述你绘制了什么图表。</reply>"""

        llm_messages = [{"role": "system", "content": sys_prompt}]
        if memory_context:
            for msg_dict in memory_context[-6:]:  
                r = msg_dict.get("role", ""); c = str(msg_dict.get("content", ""))
                if not isinstance(c, str): continue
                if r == "assistant":
                    c = re.sub(r"!\[.*?\]\(.*?\)", "", c); c = re.sub(r"\*\(\*\*🧠.*?\)\*\n\n", "", c)
                    llm_messages.append({"role": "assistant", "content": c[:800]})
                elif r == "user":
                    clean_user = re.sub(r"\n\n\*\(\w+ .*\)\*", "", c)
                    llm_messages.append({"role": "user", "content": clean_user})

        llm_messages.append({"role": "user", "content": final_prompt})

        try:
            resp = self.client.chat.completions.create(model=self.model_name, messages=llm_messages, temperature=0.1)
            raw_text = resp.choices[0].message.content
            
            action = self.extract_tag(raw_text, "action").upper()
            core_data = self.clean_code(self.extract_tag(raw_text, "target"))
            thought = self.extract_tag(raw_text, "thought")
            reply_md = self.extract_tag(raw_text, "reply")

            if not reply_md: reply_md = raw_text
            if not action: action = "TEXT"
            if not thought: thought = "推演进行中..."

            final_md = f"*(**🧠 神经逻辑核**: {thought})*\n\n{reply_md}"
            screen_html = None  
            screen_image = None 

            if action == "PYTHON_SANDBOX" and core_data:
                res = self.execute_sandbox(core_data)
                
                # 🌟 无论代码运行成不成功，都给强制暴露沙盒内部全量源码信息
                if res['stdout'] or res['error']:
                    final_md += f"\n\n---\n**🤖 终端回显记录**:\n```text\n{(res['stdout'] + chr(10) + res['error']).strip()}\n```"
                
                if res['success']:
                    if res['plot_html']:
                        html_src = res['plot_html']
                        # 这个带安全放行属性的巨大 IFRAME，才是包裹交互图表的真正容器！
                        screen_html = f"<div style='width:100%; height:100vh; overflow:hidden; background-color:#ffffff; border-radius:12px; box-shadow:0 6px 25px rgba(0,0,0,0.06);'><iframe srcdoc='{html.escape(html_src)}' style='width:100%; height:100%; border:none;' sandbox='allow-scripts allow-same-origin allow-popups'></iframe></div>"
                        final_md += f"\n\n🟢 **沙盒渲染已突破屏障，并入您的右侧视图。**"
                    elif res['plot_path']: 
                        screen_image = res['plot_path']
                        final_md += f"\n\n🟢 **低维光栅底片已在右舱呈列。**"
                else: 
                     final_md += f"\n*(❌ 执行异常，代码不合规)*"

            elif action == "2D_MOLECULE" and core_data: screen_html = self.generate_rdkit_2d_html(core_data)
            elif action == "3D_PROTEIN" and core_data: screen_html = self.generate_3d_iframe(core_data)
            elif action == "FOLD_PROTEIN" and core_data:
                seq = re.sub(r'[^A-Z]', '', core_data.upper())
                api_resp = requests.post('https://api.esmatlas.com/foldSequence/v1/pdb/', data=seq, timeout=40)
                if api_resp.status_code == 200:
                    screen_html = self.generate_3d_iframe(None, is_custom=True, pdb_str=api_resp.text)
                    final_md += "\n\n🟢 **宇宙折叠网接入，形体重建完毕。**"
            elif action == "MOLECULAR_DOCKING" and "|||" in core_data:
                parts = core_data.split("|||")
                screen_html = self.generate_docking_iframe(parts[0].strip(), parts[1].strip())
            elif action == "CREATE_TOOL":
                parts = core_data.split("\n", 1)
                if len(parts) >= 2:
                    tool_name = parts[0].strip().replace('.py', '')
                    os.makedirs(self.tools_path, exist_ok=True)
                    with open(os.path.join(self.tools_path, f"{tool_name}.py"), "w") as f: f.write(parts[1])
                    final_md += f"\n\n💾 【物理层写入】：宿主磁盘新增功能 `{tool_name}.py` 。该模组已合流 BloClaw ！"

            return {"text": final_md, "screen_html": screen_html, "screen_image": screen_image}
            
        except Exception as e: return {"text": str(e), "screen_html": None, "screen_image": None}
