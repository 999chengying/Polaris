# -*- coding: utf-8 -*-
# Copyright (c) 2026 999chengying / Polaris Project
# Licensed under the Apache License, Version 2.0

"""
PolarisBlock (终极融合版)
集成了：纯整数 WTA 注意力 + 拓扑稀疏 MoE + 六爻防御熔断 + O(1) 极限环记忆池。
"""

from typing import List, Tuple
from src.polaris.core.topological_rotator import TopologicalRotator

class ExpertFFN:
    def __init__(self, node_coord: Tuple[int, int, int]):
        self.bias = sum(node_coord) % 10
    def forward(self, token: List[int]) -> List[int]:
        return [(val * 3 + self.bias) % 10 for val in token]

class TopologicalMemoryCell:
    """极限环 O(1) 记忆池"""
    def __init__(self, d_model: int = 4):
        self.memory_pool = [[0] * d_model for _ in range(4)]
        self.step_count = 0

    def update_and_read(self, token_features: List[int], token_coord: Tuple[int, int]) -> List[int]:
        self.step_count += 1
        u, l = token_coord
        for _ in range(self.step_count % 4):
            u, l = (TopologicalRotator.next_post_to_pre(u), TopologicalRotator.next_post_to_pre(l))
        
        target_slot = (u + l + self.step_count) % 4
        for i in range(len(token_features)):
            decay = (self.step_count + i) % 10
            self.memory_pool[target_slot][i] = (self.memory_pool[target_slot][i] + token_features[i] + decay) % 10
        return self.memory_pool[target_slot]

class PolarisBlock:
    """
    纯整数拓扑心智 Block (终极版)。
    包含：WTA 注意力 (局部) + MoE (稀疏) + 六爻防御 (免疫) + O(1) 记忆 (全局)。
    """
    def __init__(self, seq_len: int, d_model: int):
        self.seq_len = seq_len
        self.d_model = d_model
        self.expert_coords = [(3,3,3), (3,1,3), (3,5,3), (1,3,3), (5,3,3), (3,3,1), (3,3,5), (3,1,1), (3,5,5), (3,1,5), (3,5,1)]
        self.experts = {node: ExpertFFN(node) for node in self.expert_coords}
        self.memory = TopologicalMemoryCell(d_model=d_model)

    def _hash_project(self, features: List[int]) -> Tuple[int, int, int]:
        third = len(features) // 3
        if third == 0: return (3, 3, 3)
        segs = [features[:third], features[third:2*third], features[2*third:]]
        coord = []
        for seg in segs:
            val = int(abs(sum(seg) / len(seg))) % 10
            coord.append(1 if val < 3 else (5 if val > 6 else 3))
        return (coord[0], coord[1], coord[2])

    def _route_to_expert(self, coord: Tuple[int, int, int]) -> Tuple[int, int, int]:
        return min(self.expert_coords, key=lambda e: sum(abs(coord[i] - e[i]) for i in range(3)))

    def forward(self, Q: List[List[int]], K: List[List[int]], V: List[List[int]]) -> List[List[int]]:
        # 1. 纯整数 WTA Attention
        scores = [[sum(Q[i][d] * K[j][d] for d in range(self.d_model)) % 10 for j in range(self.seq_len)] for i in range(self.seq_len)]
        mask = [[1 if scores[i][j] == max(scores[i]) else 0 for j in range(self.seq_len)] for i in range(self.seq_len)]
        
        attn_out = [[0] * self.d_model for _ in range(self.seq_len)]
        for i in range(self.seq_len):
            for d in range(self.d_model):
                val = sum((V[j][d] + j) for j in range(self.seq_len) if mask[i][j] == 1)
                attn_out[i][d] = val % 10

        # 2. 核心融合：MoE + 六爻熔断 + O(1) 记忆
        block_output = []
        for i, token in enumerate(attn_out):
            # A. MoE 稀疏路由
            coord = self._hash_project(token)
            expert_node = self._route_to_expert(coord)
            expert_out = self.experts[expert_node].forward(token)
            
            # B. 六爻边界防御 (防死锁)
            # 检查第 3 维 (边界特征) 是否为偶数死锁
            if self.d_model >= 3 and expert_out[2] % 2 == 0:
                # 触发逆元收权，强制翻转
                expert_out[2] = (expert_out[2] * 3) % 10
                
            # C. O(1) 极限环记忆融合
            memory_coord = (expert_node[0], expert_node[1])
            memory_out = self.memory.update_and_read(expert_out, memory_coord)
            
            # D. 最终混合 (局部特征 + 记忆回响)
            hybrid_out = [(expert_out[d] + memory_out[d]) % 10 for d in range(self.d_model)]
            block_output.append(hybrid_out)
            
        return block_output
