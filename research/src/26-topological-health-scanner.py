# -*- coding: utf-8 -*-
# Copyright (c) 2026 999chengying / Polaris Project
# Licensed under the Apache License, Version 2.0

"""
Polaris 大模型拓扑体检仪 (Topological Health Scanner)
基于 Auto-Healing Bagua Attention 的底层状态，生成医疗级的模型健康诊断报告。
"""

from typing import List, Tuple

class AutoHealingHead:
    """带有自愈免疫机制的单卦注意力头"""
    def __init__(self, upper_name: str, lower_name: str, u_bias: int, l_bias: int):
        self.name = f"{upper_name}/{lower_name}"
        self.u_bias = u_bias
        self.l_bias = l_bias

    def _compute_raw_attention(self, q: List[int], k: List[int], is_reverse: bool = False, swap: bool = False) -> int:
        """计算带偏置的原始注意力分数"""
        q_t = k if swap else q
        k_t = q if swap else k
        
        raw_score = sum(qi * ki for qi, ki in zip(q_t, k_t))
        
        u = (10 - self.u_bias) % 10 if is_reverse else self.u_bias
        l = (10 - self.l_bias) % 10 if is_reverse else self.l_bias
        
        return (raw_score + u + l) % 10

    def forward_with_immunity(self, q: List[int], k: List[int], v: List[int]) -> Tuple[List[int], int, str]:
        """带三级免疫系统的单头前向传播"""
        # 1. 原卦
        score = self._compute_raw_attention(q, k)
        if score > 5:
            return [(vi + self.l_bias) % 10 for vi in v], score, "原卦命中"
            
        # 2. 错卦 (阴阳反转)
        cuo_score = self._compute_raw_attention(q, k, is_reverse=True)
        if cuo_score > 5:
            return [(vi + (10 - self.l_bias)) % 10 for vi in v], cuo_score, "错卦激活"
            
        # 3. 综卦 (上下颠倒)
        zong_score = self._compute_raw_attention(q, k, swap=True)
        if zong_score > 5:
            return [(vi + self.u_bias) % 10 for vi in v], zong_score, "综卦激活"
            
        # 4. 互卦 (坍缩至中宫)
        return [5] * len(v), 5, "互卦坍缩"


class TopologicalScanner:
    """大模型拓扑体检扫描仪"""
    def __init__(self):
        self.heads = [
            AutoHealingHead("乾", "坤", 9, 1),
            AutoHealingHead("坤", "乾", 1, 9),
            AutoHealingHead("震", "离", 8, 3),
            AutoHealingHead("坎", "艮", 7, 6),
            AutoHealingHead("巽", "兑", 2, 4),
            AutoHealingHead("艮", "坎", 6, 7)
        ]

    def scan_and_report(self, Q: List[int], K: List[int], V: List[int]) -> None:
        """执行扫描并出具报告"""
        print("=" * 60)
        print("🏥 纯整数大模型拓扑体检报告 V1.1")
        print("=" * 60)
        print(f"输入 Token 特征:\n  Q: {Q}\n  K: {K}\n  V: {V}\n")
        print("-" * 60)
        
        healthy_count = 0
        warning_count = 0
        critical_count = 0
        
        for head in self.heads:
            out, score, status = head.forward_with_immunity(Q, K, V)
            
            if status == "原卦命中":
                healthy_count += 1
                icon = "🟢"
                diagnosis = "注意力集中，特征提取正常。"
            elif status == "错卦激活":
                warning_count += 1
                icon = "🟡"
                diagnosis = "原特征无效，触发【阴阳反转】。模型视角颠倒，但成功自救。"
            elif status == "综卦激活":
                warning_count += 1
                icon = "🟡"
                diagnosis = "陷入局部死角，触发【上下颠倒】。切换主客体视角成功。"
            else: # 互卦坍缩
                critical_count += 1
                icon = "🔴"
                diagnosis = "极度死锁！特征全丢，触发【太极护盘】，强制回归中宫5。"
                
            print(f"  [Head: {head.name}] {icon} 状态: {status} | 得分: {score}")
            print(f"    -> 诊断: {diagnosis}")
            
        print("-" * 60)
        total_heads = len(self.heads)
        health_score = (healthy_count / total_heads) * 100
        
        print(f"📊 [整体健康度]: 正常 {healthy_count}/{total_heads} | 预警 {warning_count} | 危重 {critical_count}")
        print(f"📈 [系统健康指数]: {health_score:.1f}%")
        
        if critical_count >= total_heads / 2:
            print("🚨 [主治医师结论]: 【红色警报】模型遭遇严重语义过载！")
            print("    超过一半的特征头全部死锁！强烈建议立即截断输入，或者重新进行注意力微调！")
        elif critical_count > 0 or warning_count > total_heads / 2:
            print("💡 [主治医师结论]: 【橙色预警】模型出现局部注意力漂移。")
            print("    自愈系统已疯狂兜底。虽然可以输出，但可能伴随轻度幻觉，需人工复核。")
        elif warning_count > 0:
            print("🟢 [主治医师结论]: 【黄色观察】模型处于正常波动区间，自愈机制发挥了作用。")
        else:
            print("✨ [主治医师结论]: 【绿色健康】极其健康！逻辑清晰，元气满满。")
            
        print("=" * 60)


if __name__ == "__main__":
    scanner = TopologicalScanner()
    
    print("\n>>> 模拟场景 1：复杂/混沌语义 (大量死锁)")
    scanner.scan_and_report([1, 1, 1], [1, 1, 1], [2, 4, 6])
    
    print("\n>>> 模拟场景 2：清晰/正常语义")
    scanner.scan_and_report([8, 9, 2], [3, 7, 1], [4, 5, 6])
