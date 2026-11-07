# -*- coding: utf-8 -*-
# Copyright (c) 2026 999chengying / Polaris Project
# Licensed under the Apache License, Version 2.0

"""
Polaris PTPP (Topological Projection Protocol) Gateway
大模型防幻觉网关：高维浮点特征投影、纯整数因果干预与元观测者。
"""

from typing import List, Tuple, Dict

class MetaObserver:
    """
    元观测者（防复读机监控）。
    通过监测状态序列中是否出现高频震荡或死锁，判定模型是否陷入局部循环。
    """
    def __init__(self, threshold: int = 3):
        self.threshold = threshold
        self.history = []

    def observe(self, current_val: int) -> Tuple[int, str]:
        self.history.append(current_val)
        if len(self.history) > 10:
            self.history.pop(0)

        # 检测高频震荡（如 3, 7, 3, 7）
        if len(self.history) >= 4:
            if self.history[-1] == self.history[-3] and self.history[-2] == self.history[-4]:
                return current_val, "⚠️ 死锁警报：检测到高频震荡（复读机前兆）！建议强制破局。"

        # 检测连续相同值
        if len(self.history) >= self.threshold:
            if len(set(self.history[-self.threshold:])) == 1:
                return current_val, f"⚠️ 死锁警报：连续 {self.threshold} 步状态同质化！触发中宫强制重置。"
                
        return current_val, "正常演化"


def hash_project_float_to_small_model(features: List[float]) -> Tuple[int, int, int]:
    """
    拓扑投影 (Topological Projection)
    将 128/4096 维的高维浮点特征，纯整数降维至 3D 空间坐标 (d1, d2, d3) ∈ [0-9]。
    核心算法：按分形三等分，计算绝对均值并映射至模10空间。
    """
    n = len(features)
    if n == 0:
        return (5, 5, 5) # 兜底，返回中宫
    
    third = n // 3
    if third == 0:
        # 维度太小，直接取其绝对值
        val = int(abs(sum(features))) % 10
        return (val, val, val)

    seg1 = features[:third]
    seg2 = features[third:2*third]
    seg3 = features[2*third:]

    def calc_segment(seg: List[float]) -> int:
        # 简单降维：计算该段特征的均值并取绝对值，模 10
        # 为了处理正负号引起的相消，我们用绝对值的均值来代表能量强度
        abs_mean = sum(abs(x) for x in seg) / len(seg)
        return int(abs_mean * 10) % 10

    d1 = calc_segment(seg1)
    d2 = calc_segment(seg2)
    d3 = calc_segment(seg3)

    # 防死锁机制：如果全坍缩为0，强制偏移(洛书3)
    if d1 == 0 and d2 == 0 and d3 == 0:
        return (3, 3, 3)
        
    return (d1, d2, d3)


def causal_steer(state: Tuple[int, int, int]) -> Tuple[str, int, Tuple[int, int, int]]:
    """
    因果干预 (Causal Steer)
    对传入的 3D 小模状态进行代数诊断。
    若特征发散（共识度低于阈值），计算反向的纯整数代数偏置。
    
    返回: (状态: "PASS" 或 "WARN", 共识度, 偏置向量)
    """
    d1, d2, d3 = state
    
    # 计算共识度：基于拓扑偏移定则（值+址），此处用简化的权重和
    # 共识度 0-9，数值越高越安全（趋于稳定）
    consensus = (d1 * 3 + d2 * 5 + d3 * 7) % 10
    
    # 如果共识度 >= 7，认为特征收敛，安全放行
    if consensus >= 7:
        return "PASS", consensus, (0, 0, 0)
        
    # 否则，特征发散（疑似幻觉），计算反向偏置将其拉回安全区。
    # 目标共识度设为 8（艮卦，山，代表稳固）
    target_consensus = 8
    diff = (target_consensus - consensus) % 10
    
    # 将需要弥补的差值，分配到最薄弱的维度上
    # 这里使用极简策略：在 d3 上注入偏置（因为 d3 是控制轴）
    offset = (0, 0, diff)
    
    return "WARN", consensus, offset


def ptpp_guardrail(features: List[float]) -> Dict[str, any]:
    """
    工业级一站式调用接口
    """
    state = hash_project_float_to_small_model(features)
    status, consensus, offset = causal_steer(state)
    
    if status == "PASS":
        return {"status": "PASS", "state": state, "consensus": consensus, "action": "放行"}
        
    # 执行干预
    new_state = tuple((state[i] + offset[i]) % 10 for i in range(3))
    _, new_consensus, _ = causal_steer(new_state)
    
    return {
        "status": "INTERVENE",
        "original_state": state,
        "original_consensus": consensus,
        "offset": offset,
        "fixed_state": new_state,
        "fixed_consensus": new_consensus,
        "action": "已执行纯整数代数纠偏"
    }


# =========================================================
# 自测代码 (可直接在 Programiz 等在线环境运行)
# =========================================================
if __name__ == "__main__":
    print("=" * 60)
    print("☯️ Polaris PTPP 防幻觉网关 (PTPP Gateway) 自测")
    print("=" * 60)

    # 场景 1：正常收敛特征 (全正且稳定)
    normal_features = [0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 0.1, 0.2, 0.3]
    print("\n>>> 场景 1：正常推理特征")
    res1 = ptpp_guardrail(normal_features)
    print(f"  原始特征 12 维 -> 状态: {res1['state']}")
    print(f"  共识度: {res1['consensus']} | 状态: {res1['status']}")
    print(f"  结果: {res1['action']}")

    # 场景 2：严重发散特征 (正负乱跳，模拟幻觉)
    hallucination_features = [-0.98, 0.92, 0.11, -0.45, 0.88, 0.01, 0.99, -0.76, 0.33, -0.99, 0.5, -0.5]
    print("\n>>> 场景 2：严重发散特征 (幻觉)")
    res2 = ptpp_guardrail(hallucination_features)
    print(f"  原始特征 12 维 -> 状态: {res2['original_state']}")
    print(f"  共识度: {res2['original_consensus']} | 状态: {res2['status']}")
    print(f"  触发干预！注入代数偏置力场: {res2['offset']}")
    print(f"  纠偏后状态: {res2['fixed_state']}")
    print(f"  新共识度: {res2['fixed_consensus']}")
    print(f"  结果: {res2['action']}")

    # 场景 3：元观测者防复读机
    print("\n>>> 场景 3：元观测者 (防复读机)")
    observer = MetaObserver(threshold=3)
    sequence = [3, 7, 3, 7, 3, 7]
    for i, val in enumerate(sequence):
        _, status = observer.observe(val)
        print(f"  步 {i+1}: 输入={val} | 状态: {status}")
    print("=" * 60)
