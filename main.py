from bioclaw.agents.chem_agent import ChemAgent
from bioclaw.core.safety_sandbox import BioSafetySandbox

if __name__ == "__main__":
    print("🚀 启动 BioClaw 核心验证系统...\n")

    # 1. 测试本地化学智能体 (以阿司匹林为例)
    print("--- 🧪 正在测试 ChemAgent ---")
    agent = ChemAgent()
    result = agent.evaluate_molecule("CC(=O)OC1=CC=CC=C1C(=O)O")
    print(result)

    # 2. 测试湿实验安全沙箱
    print("\n--- 🛡️ 正在测试 Safety Sandbox ---")
    dangerous_ai_script = """
import os
print("准备控制移液枪")
os.system("rm -rf /") # 模拟 AI 生成的危险代码
"""
    is_safe, msg = BioSafetySandbox.verify_protocol(dangerous_ai_script)
    print(f"脚本安全性: {is_safe} | 拦截结果: {msg}")