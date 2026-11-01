# -*- coding: utf-8 -*-
# Copyright (c) 2026 999chengying / Polaris Project

"""
Polaris 纯整数 Transformer 完整层演示。
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.polaris.nn.topological_block import TopologicalTransformerBlock

def run_block_demo():
    print("=" * 60)
    print("☯️ Polaris V39: 纯整数 Transformer 层完整闭环")
    print("=" * 60)
    
    Q = [[2, 7], [5, 5], [8, 3]]
    K = [[8, 3], [3, 8], [1, 6]]
    V = [[4, 9], [2, 1], [7, 6]]
    
    block = TopologicalTransformerBlock(seq_len=3, d_model=2)
    output = block.forward(Q, K, V)
    
    print("[输出] 完整 Block 的最终特征:")
    for i, out in enumerate(output):
        print(f"  Token {i} 输出: {out}")
        
    print("\n✅ 零浮点、零指数、零Softmax，纯整数层已跑通！")

if __name__ == "__main__":
    run_block_demo()
