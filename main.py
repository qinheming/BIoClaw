from bioclaw.core.engine import BloClawCoordinator

if __name__ == "__main__":
    print("🚀 启动 BloClaw 强人工智能控制台...\n")
    
    engine = BloClawCoordinator()
    
    # --- 测试案例 1：跟化学相关的自然语言 ---
    print("\n===========================")
    print("[人类科学家]: BloClaw，接住这个靶点分子，帮我测算它的里宾斯基成药性！")
    result_1 = engine.route_task(
        user_prompt="帮我看看这个分子的数据，测试它的成药性", 
        target_data="CC(=O)OC1=CC=CC=C1C(=O)O" # 阿司匹林
    )
    print(f"\n[BloClaw 核心响应]:\n{result_1}")

    # --- 测试案例 2：跟基因多组学相关的请求 (测试大脑的分类能力) ---
    print("\n===========================")
    print("[人类科学家]: 帮我分析一下这串疑似 TP53 突变的 DNA 序列。")
    # 这段 DNA 序列: ATG(Methionine/起始) GCC(Alanine) ATT(Isoleucine) GTA(Valine) ... TAA(终止/标志为*)
    result_2 = engine.route_task(
        user_prompt="提取这串基因的特征，帮我转录翻译出它的氨基酸看有没有突变",
        target_data="ATGGCCATTGTAATGGGCCGCTGAAAGGGTGCCCGATAG" 
    )
    print(f"\n[BloClaw 核心响应]:\n{result_2}")
