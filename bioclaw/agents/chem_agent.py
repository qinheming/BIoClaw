import json
import requests
from rdkit import Chem
from rdkit.Chem import Descriptors, Lipinski, Draw

class ChemAgent:
    def __init__(self):
        self.agent_name = "BioClaw-Chem-MicroAgent"

    def evaluate_molecule(self, smiles_str: str) -> dict:
        try:
            mol = Chem.MolFromSmiles(smiles_str)
            if mol is None:
                return {"text": f"❌ 无法解析的化学结构: {smiles_str}", "image": None}

            weight = Descriptors.MolWt(mol)
            logp = Descriptors.MolLogP(mol)
            hba = Lipinski.NumHAcceptors(mol)
            hbd = Lipinski.NumHDonors(mol)
            passed = (weight <= 500) and (logp <= 5) and (hba <= 10) and (hbd <= 5)

            # 🌐 插件 B：秘密连接全球最大的公开化学数据库 (PubChem) 查底细
            pubchem_name = "未知神药 (可能为您刚合成的新结构)"
            try:
                url = f"https://pubchem.ncbi.nlm.nih.gov/rest/pug/compound/smiles/{smiles_str}/property/Title/JSON"
                res = requests.get(url, timeout=3)
                if res.status_code == 200:
                    pubchem_name = res.json()['PropertyTable']['Properties'][0]['Title']
            except Exception:
                pass

            # 👁️ 插件 A：启动 2D 绘图引擎，在本地生成分子图像
            img_path = "molecule_vis.png"
            Draw.MolToFile(mol, img_path, size=(500, 500))

            details = {
                "PubChem_Official_Name": pubchem_name,
                "Weight": round(weight, 2),
                "LogP": round(logp, 2),
                "H_Donors": hbd,
                "H_Acceptors": hba
            }
            
            text_res = json.dumps({
                "agent": self.agent_name,
                "smiles": smiles_str,
                "passed_rule_of_five": passed,
                "details": details
            }, indent=2, ensure_ascii=False)

            return {"text": text_res, "image": img_path}
        except Exception as e:
            return {"text": f"计算错误: {str(e)}", "image": None}
