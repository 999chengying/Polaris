# -*- coding: utf-8 -*-
# Copyright (c) 2026 999chengying / Polaris Project

"""
Polaris 纯整数拓扑注意力演示。
展示如何在零浮点、零指数运算下完成 Attention 层的特征聚合。
"""

import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.polaris.nn.topological_attention import TopologicalAttention

def run_attention_demo():
    print("=" * 55)
    print("☯️ Polaris 纯整数拓扑注意力演示")
    print("=" * 55)
    
    # 初始化 3 个 Token，每个 Token 维度为 2
    Q = [[2, 7], [5, 5], [8, 3]]
    K = [[8, 3], [3, 8], [1, 6]]
    V = [[4, 9], [2, 1], [7, 6]]
    
    print("[输入] Query 矩阵: ", Q)
    print("[输入] Key 矩阵:   ", K)
    print("[输入] Value 矩阵: ", V)
    
    attention = TopologicalAttention(seq_len=3, d_model=2)
    output = attention.forward(Q, K, V)
    
    print("\n" + "-" * 55)
    print("[输出] 注意力聚合结果:")
    for i, row in enumerate(output):
        print(f"  Token {i} 新特征: {row}")
        
    print("\n" + "=" * 55)
    print("结论：全程未使用任何浮点运算、Softmax 或除法。")
    print("系统依靠纯整数赢者通吃与拓扑偏置完成了自注意力计算。")
    print("=" * 55)

if __name__ == "__main__":
    run_attention_demo()
