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
        self.tools_path = os.path.abspath("v_genesis/tools")

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
        
        # 战前爆破：清理前朝余孽图纸
        if os.path.exists("sandbox_plot.html"): os.remove("sandbox_plot.html")
        if os.path.exists("sandbox_plot.png"): os.remove("sandbox_plot.png")
        
        success = True; error_msg = ""
        # 封装变量环境！
        sand_env = {"requests": requests, "os": os, "re": re}
        try:
            with redirect_stdout(output_buffer):
                # 🌟 强行环境挂载！
                injection_header = """
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import plotly.express as px
import plotly.graph_objects as go
import warnings
warnings.filterwarnings('ignore')
plt.rcParams['figure.figsize'] = (10, 6)
plt.rcParams['figure.dpi'] = 150
# 强行使 AI 的 show() 瘫痪，防止进程僵死
plt.show = lambda *args, **kwargs: None
if hasattr(go.Figure, 'show'): go.Figure.show = lambda self, *args, **kwargs: None
"""
                
                # 🌟 绝境物理劫持代码：不管模型怎么写，我们在它写完的代码后面强行查房！
                injection_footer = """
_we_saved_something = False
# 查房 1：翻找它生成的任何 Plotly 图形变量，强行导出交互式 HTML！
for _var_name, _var_val in list(locals().items()):
    if 'plotly.graph_objs' in str(type(_var_val)):
        _var_val.write_html('sandbox_plot.html', full_html=False, include_plotlyjs='cdn')
        _we_saved_something = True
        break
# 查房 2：如果它死活没用 Plotly 而是用了老掉牙的 matplotlib，给它存成死图 PNG
if not _we_saved_something and plt.get_fignums():
    plt.savefig('sandbox_plot.png', bbox_inches='tight')
"""
                
                # 正则剥皮：砍掉大模型多余的保存代码，全由我们的 Footer 查房接管
                safe_code = re.sub(r"fig\.show\(\)|plt\.show\(\)", "", python_code)
                safe_code = re.sub(r"fig\.write_html\(.*?\)", "", safe_code)
                safe_code = re.sub(r"plt\.savefig\(.*?\)", "", safe_code)
                
                exec(injection_header + safe_code + "\n\n" + injection_footer, sand_env)
        except Exception as e:
            success = False; error_msg = traceback.format_exc()
            
        plot_html = None
        plot_img = None
        
        # 战后搜山：如果查房成功生成了由 Plotly 构造的网页组件
        if os.path.exists("sandbox_plot.html"):
            with open("sandbox_plot.html", "r", encoding="utf-8") as f:
                plot_html = f.read()
        elif os.path.exists("sandbox_plot.png"):
            plot_img = os.path.abspath("sandbox_plot.png")

        return {"success": success, "stdout": output_buffer.getvalue().strip(), "error": error_msg, "plot_html": plot_html, "plot_path": plot_img}

    def generate_rdkit_2d_html(self, raw_target):
        # 2D 依然使用原生的高清 Image 组件，所以给绝对路径
        try:
            from rdkit import Chem; from rdkit.Chem import Draw
            pure_smiles = max(re.findall(r'[A-Za-z0-9@+\-\[\]\.\(\)\=\#\/\\]{4,}', raw_target), key=len)
            if pure_smiles.endswith("OH"): pure_smiles = pure_smiles[:-1] 
            mol = Chem.MolFromSmiles(pure_smiles)
            if not mol: return None
            path = os.path.abspath("temp_mol.png")
            Draw.MolToFile(mol, path, size=(800, 600))
            return path
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
            file_context += "\n\n【隐秘沙盒已挂载以数据档案】\n"
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
                        with open(path, 'r', encoding='utf-8') as tf: file_context += f"📄[提取数据文本]:\n{tf.read()[:3000]}\n"
                except: pass
        
        final_prompt = str(user_message) + file_context

        # 🌟 铁令如山：你只管写，其他的我接管！！
        sys_prompt = f"""你是全球顶级 AI 科研主脑 BloClaw。具备长时记忆关联。
【最高行动法则】
1. TEXT: 直接文本交互。
2. PYTHON_SANDBOX: ✨代码并在沙盒画图。🔥强烈要求：只要用户让你生成高级图表，你务必使用 `import plotly.express as px` !! 图表赋给变量 `fig` 即可！系统会在暗中直接劫持并投屏到界面右侧！绝不需要你写写入文件的繁杂步骤！
3. 2D_MOLECULE: 写纯 SMILES 生成拓扑。
4. 3D_PROTEIN: 展示已知自然分子(填4位PDB)。
5. FOLD_PROTEIN: 云端折叠未知生命序列。
6. MOLECULAR_DOCKING: 模拟重叠对接。填: [PDB纯编号]|||[SMILES纯序列]。
7. CREATE_TOOL: 创建永久挂载的脚本工具名。

必须完全且仅以此规矩输出四组XML：
<thought>短思考</thought>
<action>填入上面动作全大写</action>
<target>动作的投喂纯代码文字。</target>
<reply>极其专业的解答。不必解释沙盒技术细节。</reply>"""

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
            if not thought: thought = "算力解构中"

            final_md = f"*(**🧠 分析主干**: {thought})*\n\n{reply_md}"
            
            # 👇 这两兄弟将分别投向 HTML 渲染玻璃 和 纯图片放大画框！
            screen_html = None  
            screen_image = None

            if action == "PYTHON_SANDBOX" and core_data:
                res = self.execute_sandbox(core_data)
                if res['success']:
                    if res['stdout']: final_md += f"\n\n**🤖 沙盒终端报告**:\n```text\n{res['stdout']}\n```"
                    
                    # 🌟 绝杀对接：拿到了 plotly 高级代码！立刻穿透 iframe 进入全屏隔离右舱！
                    if res['plot_html']:
                        html_src = res['plot_html']
                        # 利用强隔离的 srcdoc 和 allow-scripts 把互动效果拉满！
                        screen_html = f"<div style='width:100%; height:100vh; overflow:hidden; background-color:#ffffff; border-radius:12px;'><iframe srcdoc='{html.escape(html_src)}' style='width:100%; height:100%; border:none;' sandbox='allow-scripts allow-same-origin allow-popups'></iframe></div>"
                        final_md += f"\n\n🟢 **宇宙机算渲染完毕。底层 Plotly 拦截成功，可交互的高维图表已推送至右面板。**"
                    # 最差情况：模型死活用了老图库，那也给它导出一张高清大片并允许下载放大！
                    elif res['plot_path']: 
                        screen_image = res['plot_path']
                        final_md += f"\n\n🟢 **底层工作台运转完毕，无损原始静态底片已印制在右视窗供提取。**"
                else: 
                     final_md += f"\n*(❌ 沙盒崩溃反馈)*\n```python-traceback\n{res['error']}\n```"

            elif action == "2D_MOLECULE" and core_data: 
                screen_image = self.generate_rdkit_2d_html(core_data)
            elif action == "3D_PROTEIN" and core_data: screen_html = self.generate_3d_iframe(core_data)
            
            elif action == "FOLD_PROTEIN" and core_data:
                seq = re.sub(r'[^A-Z]', '', core_data.upper())
                api_resp = requests.post('https://api.esmatlas.com/foldSequence/v1/pdb/', data=seq, timeout=40)
                if api_resp.status_code == 200:
                    screen_html = self.generate_3d_iframe(None, is_custom=True, pdb_str=api_resp.text)
                    final_md += "\n\n🟢 **宇宙力场测算结束，实体投影已上传至视窗。**"

            elif action == "MOLECULAR_DOCKING" and "|||" in core_data:
                parts = core_data.split("|||")
                screen_html = self.generate_docking_iframe(parts[0].strip(), parts[1].strip())
                final_md += f"\n\n🟢 **抗体与受体复合界面的 3D 重型对接轨道构像已布设完成。**"
                
            elif action == "CREATE_TOOL":
                parts = core_data.split("\n", 1)
                if len(parts) >= 2:
                    tool_name = parts[0].strip().replace('.py', '')
                    os.makedirs(self.tools_path, exist_ok=True)
                    with open(os.path.join(self.tools_path, f"{tool_name}.py"), "w") as f: f.write(parts[1])
                    final_md += f"\n\n💾 【数字生命突变】：系统磁盘新增执行脚本 `{tool_name}.py` 。该模组已合并至 BloClaw 主体代码！"

            return {"text": final_md, "screen_html": screen_html, "screen_image": screen_image}
            
        except Exception as e: return {"text": str(e), "screen_html": None, "screen_image": None}
