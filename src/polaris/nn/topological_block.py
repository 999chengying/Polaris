# -*- coding: utf-8 -*-
# Copyright (c) 2026 999chengying / Polaris Project
# Licensed under the Apache License, Version 2.0

"""
Polaris Topological Block
完整的纯整数 Transformer 层（零浮点、零指数、零 Softmax）。
"""

from typing import List, Tuple

class TopologicalPositionalEncoding:
    """纯整数位置编码（基于模10乘法群的 1, 3, 9, 7 循环）"""
    
    @staticmethod
    def encode(pos: int) -> int:
        """根据位置索引生成纯整数编码"""
        cycle = [1, 3, 9, 7]
        return cycle[pos % 4]


class IntegerFFN:
    """纯整数前馈网络（Topological Feed-Forward Network）"""
    
    def __init__(self, d_model: int, d_ff: int):
        self.d_model = d_model
        self.d_ff = d_ff
        # 使用纯整数初始化权重矩阵 (这里用公式生成，实际训练可用查表)
        self.W1 = [[ (i + j + 3) % 10 for j in range(d_model)] for i in range(d_ff)]
        self.W2 = [[ (i * j + 7) % 10 for j in range(d_ff)] for i in range(d_model)]

    def forward(self, x: List[int]) -> List[int]:
        """前向传播：线性映射 + 拓扑激活 + 线性映射"""
        # 1. 第一次线性映射
        H = [0] * self.d_ff
        for i in range(self.d_ff):
            H[i] = sum(x[j] * self.W1[i][j] for j in range(self.d_model)) % 10
            
        # 2. 纯整数拓扑激活 (代替 ReLU/GELU)
        # 逻辑：大于 5 的激发（乘3），否则置零 (稀疏化)
        H_act = [ (h * 3) % 10 if h > 5 else 0 for h in H ]
        
        # 3. 第二次线性映射
        O = [0] * self.d_model
        for i in range(self.d_model):
            O[i] = sum(H_act[j] * self.W2[i][j] for j in range(self.d_ff)) % 10
            
        return O


class TopologicalTransformerBlock:
    """完整的纯整数 Transformer 块"""
    
    def __init__(self, seq_len: int, d_model: int):
        self.seq_len = seq_len
        self.d_model = d_model
        self.ffn = IntegerFFN(d_model, d_model * 2)
        self.pos_encoder = TopologicalPositionalEncoding()

    def forward(self, Q: List[List[int]], K: List[List[int]], V: List[List[int]]) -> List[List[int]]:
        # 1. 注入纯整数位置编码
        for i in range(self.seq_len):
            pos_code = self.pos_encoder.encode(i)
            for d in range(self.d_model):
                Q[i][d] = (Q[i][d] + pos_code) % 10

        # 2. 纯整数注意力 (WTA)
        scores = [[0] * self.seq_len for _ in range(self.seq_len)]
        for i in range(self.seq_len):
            for j in range(self.seq_len):
                scores[i][j] = sum(Q[i][d] * K[j][d] for d in range(self.d_model)) % 10
                
        mask = [[0] * self.seq_len for _ in range(self.seq_len)]
        for i in range(self.seq_len):
            max_score = max(scores[i])
            for j in range(self.seq_len):
                if scores[i][j] == max_score:
                    mask[i][j] = 1
                    
        attn_out = [[0] * self.d_model for _ in range(self.seq_len)]
        for i in range(self.seq_len):
            for d in range(self.d_model):
                val = sum(V[j][d] + j for j in range(self.seq_len) if mask[i][j] == 1)
                attn_out[i][d] = val % 10
                
        # 3. 纯整数前馈网络 (FFN)
        final_out = []
        for i in range(self.seq_len):
            final_out.append(self.ffn.forward(attn_out[i]))
            
        return final_out
