# -*- coding: utf-8 -*-
# Copyright (c) 2026 999chengying / Polaris Project
# Licensed under the Apache License, Version 2.0

"""
Polaris Topological Attention
纯整数拓扑注意力机制（零浮点、零指数、零除法）。
"""

from typing import List

class TopologicalAttention:
    """
    纯整数拓扑注意力层。
    利用 WTA (赢者通吃) 与位置偏置打破对称，完全摒弃 Softmax。
    """
    def __init__(self, seq_len: int, d_model: int):
        self.seq_len = seq_len
        self.d_model = d_model

    def forward(self, Q: List[List[int]], K: List[List[int]], V: List[List[int]]) -> List[List[int]]:
        """
        前向传播。
        
        Args:
            Q, K, V: 纯整数状态矩阵，维度为 (seq_len x d_model)。
            
        Returns:
            O: 聚合后的特征矩阵 (seq_len x d_model)。
        """
        # 1. 计算纯整数匹配分数 (Mod 10)
        scores = [[0] * self.seq_len for _ in range(self.seq_len)]
        for i in range(self.seq_len):
            for j in range(self.seq_len):
                dot_product = sum(Q[i][d] * K[j][d] for d in range(self.d_model))
                scores[i][j] = dot_product % 10
                
        # 2. 赢者通吃掩码 (Winner-Takes-All) 取代 Softmax
        mask = [[0] * self.seq_len for _ in range(self.seq_len)]
        for i in range(self.seq_len):
            max_score = max(scores[i])
            for j in range(self.seq_len):
                if scores[i][j] == max_score:
                    mask[i][j] = 1
                    
        # 3. 纯整数特征聚合 (带拓扑位置偏置防死锁)
        O = [[0] * self.d_model for _ in range(self.seq_len)]
        for i in range(self.seq_len):
            for d in range(self.d_model):
                val = 0
                for j in range(self.seq_len):
                    if mask[i][j] == 1:
                        # 核心：加位置偏置 j，防止对称相消
                        val += V[j][d] + j
                O[i][d] = val % 10 
                
        return O
