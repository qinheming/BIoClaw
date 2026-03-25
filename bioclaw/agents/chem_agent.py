from rdkit import Chem
from rdkit.Chem import Descriptors
import json

class ChemAgent:
    """专注计算化学的小型智能体，完全在本地执行验证。"""
    
    def __init__(self):
        self.agent_name = "BioClaw-Chem-MicroAgent"

    def evaluate_molecule(self, smiles: str) -> str:
        """评估 SMILES 字符串的里宾斯基成药性"""
        mol = Chem.MolFromSmiles(smiles)
        if mol is None:
            return json.dumps({"error": "无效的 SMILES 字符串"})

        mw = Descriptors.MolWt(mol)
        logp = Descriptors.MolLogP(mol)
        hbd = Descriptors.NumHDonors(mol)
        hba = Descriptors.NumHAcceptors(mol)

        ro5_passed = (mw <= 500) and (logp <= 5) and (hbd <= 5) and (hba <= 10)

        report = {
            "agent": self.agent_name,
            "smiles": smiles,
            "passed_rule_of_five": ro5_passed,
            "details": {
                "Weight": round(mw, 2), "LogP": round(logp, 2),
                "H_Donors": hbd, "H_Acceptors": hba
            }
        }
        return json.dumps(report, indent=2)