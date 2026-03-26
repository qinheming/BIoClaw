import os
import re
import io
import html
import base64
import urllib.parse
import traceback
import requests
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
        success = True; error_msg = ""
        try:
            with redirect_stdout(output_buffer):
                exec(python_code, {"requests": requests, "os": os, "re": re})
        except Exception as e:
            success = False; error_msg = traceback.format_exc()
        return {"success": success, "stdout": output_buffer.getvalue().strip(), "error": error_msg}

    # 🌟 究极黑客魔法：把 2D 药物图像压成 Base64，镶嵌在赛博朋克深空背景的 HTML 里！
    def generate_rdkit_2d_html(self, raw_target):
        try:
            from rdkit import Chem; from rdkit.Chem import Draw
            pure_smiles = max(re.findall(r'[A-Za-z0-9@+\-\[\]\.\(\)\=\#\/\\]{4,}', raw_target), key=len)
            mol = Chem.MolFromSmiles(pure_smiles)
            if not mol: return None
            
            img_path = os.path.abspath("temp_mol.png")
            Draw.MolToFile(mol, img_path, size=(600, 400))
            
            with open(img_path, "rb") as img_file:
                b64_string = base64.b64encode(img_file.read()).decode('utf-8')
                
            # 直接生成一段深空蓝底、高亮药物的发光 HTML 面板
            return f"""<div style='width:100%; height:100%; display:flex; align-items:center; justify-content:center; background: radial-gradient(circle, #0f172a 0%, #020617 100%);'>
                <img src='data:image/png;base64,{b64_string}' style='max-width:90%; max-height:90%; border-radius:16px; box-shadow: 0 0 40px rgba(14, 165, 233, 0.4); border: 1px solid #0ea5e9; background: rgba(255,255,255,0.9); padding: 10px;'>
            </div>"""
        except: return None

    # 3D 黑暗模式全息舱
    def generate_3d_iframe(self, core_data, is_custom=False, pdb_str=None):
        if not is_custom:
            pdb = re.sub(r'[^a-zA-Z0-9]', '', core_data).lower()
            return f"<iframe src='https://3dmol.csb.pitt.edu/viewer.html?pdb={pdb}&style=cartoon;color:spectrum&spin=true&bcolor=020617' width='100%' height='100%' style='border:none;'></iframe>"
        else:
            escaped_pdb = pdb_str.replace("`", "")
            script = f"var v = $3Dmol.createViewer('g', {{backgroundColor:'#020617'}}); v.addModel(`{escaped_pdb}`, 'pdb'); v.setStyle({{}}, {{cartoon:{{color:'spectrum'}}}}); v.zoomTo(); v.render();"
            html_src = f"<html><head><script src='https://3Dmol.csb.pitt.edu/build/3Dmol-min.js'></script></head><body style='margin:0;'><div id='g' style='width:100vw; height:100vh;'></div><script>{script}</script></body></html>"
            return f"<iframe srcdoc='{html.escape(html_src)}' width='100%' height='100%' style='border:none;'></iframe>"

    def process_chat(self, user_message):
        sys_prompt = """你是顶级AI科学家BloClaw。
可选动作：1. TEXT  2. PYTHON_SANDBOX  3. 2D_MOLECULE (输入SMILES)  4. 3D_PROTEIN(4位PDB码)  5. FOLD_PROTEIN(长氨基酸序列)
必须严格输出以下XML：
<thought>简短思考</thought>
<action>动作，必须全大写</action>
<target>参数，只保留最核心的字母段</target>
<reply>写给主人的回复，Markdown排版</reply>"""

        try:
            resp = self.client.chat.completions.create(model=self.model_name, messages=[{"role": "system", "content": sys_prompt}, {"role": "user", "content": user_message}], temperature=0.1)
            raw_text = resp.choices[0].message.content
            
            action = self.extract_tag(raw_text, "action").upper()
            core_data = self.clean_code(self.extract_tag(raw_text, "target"))
            thought = self.extract_tag(raw_text, "thought")
            reply_md = self.extract_tag(raw_text, "reply")

            if action == "3D_PROTEIN" and len(core_data) > 6: action = "FOLD_PROTEIN"
            final_md = f"*(**🧠 BloClaw 神经元**: {thought})*\n\n{reply_md if reply_md else raw_text}"
            
            # 🌟 统一屏幕变量，右侧只接收 HTML 字符串！彻底消灭残破框！
            screen_html = None  
            sys_log = f"\n\n<details><summary><span style='color:#0ea5e9;'>[+] 展开系统内核日志</span></summary>\n\n```text\n[Action]: {action}\n"

            if action == "PYTHON_SANDBOX" and core_data:
                res = self.execute_sandbox(core_data)
                sys_log += f"返回:\n{res['stdout']}\n{res['error']}"

            elif action == "2D_MOLECULE" and core_data:
                # 核心变身：2D 图像直接转变成在右屏发光的前端 HTML 代码
                screen_html = self.generate_rdkit_2d_html(core_data)
                sys_log += "2D 投影推至右屏。"

            elif action == "3D_PROTEIN" and core_data:
                screen_html = self.generate_3d_iframe(core_data)
                sys_log += "3D 晶体点亮右屏。"

            elif action == "FOLD_PROTEIN" and core_data:
                seq = re.sub(r'[^A-Z]', '', core_data.upper())
                resp = requests.post('https://api.esmatlas.com/foldSequence/v1/pdb/', data=seq, timeout=40)
                if resp.status_code == 200:
                    screen_html = self.generate_3d_iframe(None, is_custom=True, pdb_str=resp.text)
                    final_md += "\n\n🟢 **虚空力场构象渲染完毕，请阅右侧全息视窗。**"
                    sys_log += "ESMFold 虚空折叠成功。"

            sys_log += "```\n</details>"
            return {"text": final_md + sys_log, "screen_html": screen_html}
            
        except Exception as e: return {"text": str(e), "screen_html": None}
