#!/usr/bin/env python3
import math
import sys

def calculate_gc_content(sequence):
    """
    计算DNA序列的GC含量百分比
    参数:
        sequence: str，输入的DNA序列（大小写不敏感，可包含空格）
    返回:
        float，GC含量百分比，保留两位小数
    异常:
        ValueError: 序列包含非ATCG字符时抛出
    """
    sequence_clean = sequence.upper().replace(' ', '')
    if not all(nucleotide in 'ATCG' for nucleotide in sequence_clean):
        invalid_chars = set(sequence_clean) - set('ATCG')
        raise ValueError(f"序列中包含无效核苷酸字符: {', '.join(invalid_chars)}")
    total_length = len(sequence_clean)
    if total_length == 0:
        return 0.0
    gc_count = sequence_clean.count('G') + sequence_clean.count('C')
    return round((gc_count / total_length) * 100, 2)

def calculate_tm(sequence, salt_concentration=50, primer_concentration=0.25):
    """
    计算DNA序列的熔解温度(Tm)，包含盐浓度校正
    参数:
        sequence: str，输入的DNA序列
        salt_concentration: int/float，Na+浓度，单位mM，默认50mM
        primer_concentration: int/float，引物浓度，单位μM，默认0.25μM
    返回:
        float，熔解温度，保留两位小数
    异常:
        ValueError: 序列包含非ATCG字符时抛出
    """
    sequence_clean = sequence.upper().replace(' ', '')
    if not all(nucleotide in 'ATCG' for nucleotide in sequence_clean):
        invalid_chars = set(sequence_clean) - set('ATCG')
        raise ValueError(f"序列中包含无效核苷酸字符: {', '.join(invalid_chars)}")
    total_length = len(sequence_clean)
    if total_length == 0:
        return 0.0
    
    gc_count = sequence_clean.count('G') + sequence_clean.count('C')
    at_count = total_length - gc_count
    
    # 基础Tm计算：分短序列和长序列
    if total_length <= 30:
        # 短引物近似公式
        tm = 4 * gc_count + 2 * at_count
    else:
        # 长序列公式（SantaLucia, 1998）
        tm = 64.9 + 41 * (gc_count - 16.4) / total_length
    
    # 盐浓度和引物浓度校正（Montobro-Calvo模型简化）
    tm += 16.6 * math.log10(salt_concentration / 1000) - 0.65 * math.log10(primer_concentration / 1000) - (600 / total_length)
    
    return round(tm, 2)

def main():
    if len(sys.argv) > 1:
        dna_sequence = sys.argv[1]
    else:
        dna_sequence = input("请输入待分析的DNA序列：").strip()
    
    try:
        gc_content = calculate_gc_content(dna_sequence)
        tm_value = calculate_tm(dna_sequence)
        
        print("="*40)
        print("DNA序列分析报告")
        print("="*40)
        print(f"输入序列长度: {len(dna_sequence.replace(' ', ''))} bp")
        print(f"GC含量: {gc_content} %")
        print(f"熔解温度(Tm): {tm_value} °C")
        print(f"校正条件: Na+浓度=50mM，引物浓度=0.25μM")
        print("="*40)
        
    except ValueError as e:
        print(f"错误: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()