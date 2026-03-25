import os
from openai import OpenAI
from dotenv import load_dotenv
from bioclaw.agents.chem_agent import ChemAgent
from bioclaw.agents.omics_agent import OmicsAgent

load_dotenv()

class BioClawCoordinator:
    def __init__(self):
        self.api_key = os.getenv("DOUBAO_API_KEY")
        self.endpoint = os.getenv("DOUBAO_ENDPOINT")
        self.chem_agent = ChemAgent()
        self.omics_agent = OmicsAgent()
        self.client = OpenAI(api_key=self.api_key, base_url="https://ark.cn-beijing.volces.com/api/v3") if self.api_key else None

    def route_task(self, user_prompt: str, target_data: str = None) -> dict:
        if not self.client:
            if target_data:
                return self.chem_agent.evaluate_molecule(target_data)
            return {"text": "❌ 本地执行需要 target_data", "image": None}

        system_prompt = """
        分析用户的科学请求，严格输出以下三个英文单词之一：
        1. CHEMISTRY (分子量、脂水分配系数、里宾斯基规则、分子结构)
        2. OMICS (基因组、靶点、序列比对、蛋白质、DNA相关)
        3. UNKNOWN (都不属于)
        只输出一个英文单词。
        """
        try:
            response = self.client.chat.completions.create(
                model=self.endpoint,
                messages=[{"role": "system", "content": system_prompt}, {"role": "user", "content": user_prompt}],
                temperature=0.1
            )
            intent = response.choices[0].message.content.strip().upper()

            if "CHEMISTRY" in intent:
                return self.chem_agent.evaluate_molecule(target_data) if target_data else {"text": "❌ 需提供分子(SMILES)", "image": None}
            elif "OMICS" in intent:
                if not target_data:
                    return {"text": "❌ 需提供 DNA 序列", "image": None}
                return {"text": self.omics_agent.analyze_sequence(target_data), "image": None}
            else:
                return {"text": "🤖 [系统回复] 请求超出范围。", "image": None}
        except Exception as e:
            return {"text": f"❌ 大模型路由失败: {str(e)}", "image": None}
