# -*- coding: utf-8 -*-
# Copyright (c) 2026 999chengying / Polaris Project
# Licensed under the Apache License, Version 2.0

"""
Polaris Sparse Transformer Block
基于纯整数拓扑的稀疏混合专家 Transformer 层。
"""

from typing import List, Tuple, Dict

class ExpertFFN:
    """纯整数专家 FFN"""
    def __init__(self, node_coord: Tuple[int, int, int]):
        self.node = node_coord
        self.bias = sum(node_coord) % 10
        
    def forward(self, token: List[int]) -> List[int]:
        return [(val * 3 + self.bias) % 10 for val in token]


class SparseTransformerBlock:
    """
    纯整数稀疏 Transformer 层。
    流程：WTA Attention -> 拓扑 MoE 路由 -> Expert FFN
    """
    def __init__(self, seq_len: int, d_model: int):
        self.seq_len = seq_len
        self.d_model = d_model
        
        # 11 个拓扑专家节点
        self.expert_coords = [
            (3, 3, 3), (3, 1, 3), (3, 5, 3), (1, 3, 3), (5, 3, 3), 
            (3, 3, 1), (3, 3, 5), (3, 1, 1), (3, 5, 5), (3, 1, 5), (3, 5, 1)
        ]
        self.experts = {node: ExpertFFN(node) for node in self.expert_coords}

    def _hash_project(self, features: List[int]) -> Tuple[int, int, int]:
        """将连续小模特征压降为 3D 坐标"""
        third = len(features) // 3
        if third == 0:
            return (3, 3, 3) # 兜底中宫
            
        segs = [features[:third], features[third:2*third], features[2*third:]]
        coord = []
        for seg in segs:
            # 简化的纯整数方差与符号
            mean_val = sum(seg) / len(seg)
            val = int(abs(mean_val)) % 10
            if val < 3: coord.append(1)
            elif val > 6: coord.append(5)
            else: coord.append(3)
        return tuple(coord)

    def _route_to_expert(self, coord: Tuple[int, int, int]) -> Tuple[int, int, int]:
        """拓扑无参路由：找最近的专家"""
        best_expert, min_dist = None, float('inf')
        for e in self.expert_coords:
            dist = sum(abs(coord[i] - e[i]) for i in range(3))
            if dist < min_dist:
                min_dist, best_expert = dist, e
        return best_expert

    def forward(self, Q: List[List[int]], K: List[List[int]], V: List[List[int]]) -> List[List[int]]:
        # 1. 纯整数 WTA Attention
        scores = [[sum(Q[i][d] * K[j][d] for d in range(self.d_model)) % 10 
                   for j in range(self.seq_len)] for i in range(self.seq_len)]
        
        mask = [[1 if scores[i][j] == max(scores[i]) else 0 
                 for j in range(self.seq_len)] for i in range(self.seq_len)]
        
        attn_out = [[0] * self.d_model for _ in range(self.seq_len)]
        for i in range(self.seq_len):
            for d in range(self.d_model):
                val = sum((V[j][d] + j) for j in range(self.seq_len) if mask[i][j] == 1)
                attn_out[i][d] = val % 10
            
        # 2. 拓扑稀疏 MoE 路由与专家 FFN
        final_out = []
        for i, token in enumerate(attn_out):
            coord = self._hash_project(token)
            expert_node = self._route_to_expert(coord)
            expert_output = self.experts[expert_node].forward(token)
            final_out.append(expert_output)
            
        return final_out
