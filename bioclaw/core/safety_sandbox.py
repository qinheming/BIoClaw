import ast
from typing import Tuple

class BioSafetySandbox:
    """
    BioClaw 特有的安全层：在将 AI 生成的 Python 脚本发送给底层液体工作站前，
    进行静态安全分析，拦截破坏性指令。
    """
    FORBIDDEN_FUNCTIONS = {'os.system', 'subprocess.run', 'shutil.rmtree', 'open'}

    @classmethod
    def verify_protocol(cls, script_content: str) -> Tuple[bool, str]:
        try:
            tree = ast.parse(script_content)
        except SyntaxError as e:
            return False, f"语法错误: {e}"

        for node in ast.walk(tree):
            if isinstance(node, ast.Call):
                func_name = ""
                if isinstance(node.func, ast.Name):
                    func_name = node.func.id
                elif isinstance(node.func, ast.Attribute):
                    func_name = node.func.attr
                
                if func_name in cls.FORBIDDEN_FUNCTIONS:
                    return False, f"安全拦截: 禁止调用 '{func_name}'"
        
        return True, "验证通过：脚本被判定为实验设备安全。"