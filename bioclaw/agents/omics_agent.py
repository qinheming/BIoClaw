import json
from Bio.Seq import Seq

class OmicsAgent:
    """
    BioClaw 多组学微智能体。
    专职处理 DNA/RNA 序列、蛋白质翻译、基因突变分析等生物信息学核心任务。
    """
    def __init__(self):
        self.agent_name = "BioClaw-Omics-MicroAgent"

    def analyze_sequence(self, sequence_str: str) -> str:
        """
        接收一段 DNA 序列，进行中心法则运算：
        1. 计算 GC 含量 (判断基因片段稳定性的重要指标)
        2. 将 DNA 翻译成蛋白质 (寻找氨基酸突变)
        """
        try:
            # 净化输入的序列并转成 Biopython 的标准 Seq 对象
            clean_seq = sequence_str.replace(" ", "").upper()
            dna_seq = Seq(clean_seq)
            
            # 生信计算 1：计算 GC 含量 (G和C碱基的比例)
            g_count = dna_seq.count('G')
            c_count = dna_seq.count('C')
            gc_content = (g_count + c_count) / len(dna_seq) * 100 if len(dna_seq) > 0 else 0
            
            # 生信计算 2：DNA 翻译为氨基酸 (中心法则)
            # 遇到终止密码子会显示为 '*'
            protein_seq = dna_seq.translate()
            
            result = {
                "agent": self.agent_name,
                "sequence_length": len(dna_seq),
                "gc_content_percent": round(gc_content, 2),
                "protein_translation": str(protein_seq),
                "status": "success"
            }
            return json.dumps(result, indent=2, ensure_ascii=False)
            
        except Exception as e:
            return json.dumps({"agent": self.agent_name, "error": f"序列解析失败: {str(e)}", "status": "failed"})
