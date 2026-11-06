# -*- coding: utf-8 -*-
# Copyright (c) 2026 999chengying / Polaris Project
# Licensed under the Apache License, Version 2.0

"""
Polaris Auto-Healing Bagua Attention
具备三级物理免疫（错、综、互）的纯整数多头注意力层。
"""

from typing import List, Tuple, Dict

class AutoHealingHead:
    """带有自愈免疫机制的单卦注意力头"""
    def __init__(self, upper_name: str, lower_name: str, u_bias: int, l_bias: int):
        self.name = f"{upper_name}/{lower_name}"
        self.u_bias = u_bias
        self.l_bias = l_bias

    def _compute_raw_attention(self, q: List[int], k: List[int], is_reverse: bool = False, swap: bool = False) -> int:
        q_t = k if swap else q
        k_t = q if swap else k
        
        raw_score = sum(qi * ki for qi, ki in zip(q_t, k_t))
        
        u = (10 - self.u_bias) % 10 if is_reverse else self.u_bias
        l = (10 - self.l_bias) % 10 if is_reverse else self.l_bias
        
        return (raw_score + u + l) % 10

    def forward_with_immunity(self, q: List[int], k: List[int], v: List[int]) -> Tuple[List[int], int, str]:
        """三级免疫前向传播"""
        # 1. 原卦
        score = self._compute_raw_attention(q, k, v)
        if score > 5:
            return [(vi + self.l_bias) % 10 for vi in v], score, "原卦命中"
            
        # 2. 错卦 (阴阳反转)
        cuo_score = self._compute_raw_attention(q, k, v, is_reverse=True)
        if cuo_score > 5:
            return [(vi + (10 - self.l_bias)) % 10 for vi in v], cuo_score, "错卦激活"
            
        # 3. 综卦 (上下颠倒)
        zong_score = self._compute_raw_attention(q, k, v, swap=True)
        if zong_score > 5:
            return [(vi + self.u_bias) % 10 for vi in v], zong_score, "综卦激活"
            
        # 4. 互卦 (坍缩至中宫)
        return [5] * len(v), 5, "互卦坍缩"


class AutoHealingBaguaAttention:
    """多头自愈注意力聚合层"""
    def __init__(self):
        # 可以按需扩展至 64 个 Head
        self.heads = [
            AutoHealingHead("乾", "坤", 9, 1),
            AutoHealingHead("坤", "乾", 1, 9),
            AutoHealingHead("震", "离", 8, 3),
            AutoHealingHead("坎", "艮", 7, 6),
        ]

    def forward(self, Q: List[int], K: List[int], V: List[int]) -> List[int]:
        final_output = [0] * len(V)
        for head in self.heads:
            out, _, _ = head.forward_with_immunity(Q, K, V)
            for i in range(len(V)):
                final_output[i] = (final_output[i] + out[i]) % 10
        return final_output
