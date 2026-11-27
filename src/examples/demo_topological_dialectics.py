# -*- coding: utf-8 -*-
# Copyright (c) 2026 999chengying / Polaris Project
# Licensed under the Apache License, Version 2.0

"""
Polaris: 纯整数手性辩证法引擎 (最终入库版)
融合黑格尔正反合与三维手性立方体拓扑变换。
通过纯整数状态强制约束大模型辩论极性，拒绝和稀泥。
"""

import os
import requests

API_KEY = os.environ.get("DEEPSEEK_API_KEY")
API_URL = "https://api.deepseek.com/chat/completions"
USE_REAL_API = True

# ==================== 1. 拓扑坐标与变换定义 ====================
# 基准面（取立方体甲的四个关键极点，作为状态注入点）
CUBE_A_POINTS = [(1, 1, 1), (1, 1, 5), (5, 1, 1), (1, 5, 1)]

def mirror_flip(coord):
    """甲到丙的镜像翻转：以 x=y 面进行空间镜像"""
    x, y, z = coord
    return (y, x, z)

def rotate_120(coord):
    """丙到乙的旋转全等：绕 (1,1,1)-(5,5,5) 体对角线旋转120度"""
    x, y, z = coord
    return (z, x, y)

# ==================== 2. 大模型翻译引擎 ====================
def translate_state(role, state_val, topic):
    """大模型只作为翻译官，纯整数状态决定其语气"""
    if not USE_REAL_API or not API_KEY:
        return "[模拟翻译] 角色:{}, 状态:{}, 辩题:{}".format(role, state_val, topic)
        
    prompt = (
        "你是一个状态翻译官。请将纯整数映射为人类的辩论语言。\n"
        "辩题：{}\n".format(topic) +
        "你的阵营：{}\n".format(role) +
        "当前纯整数拓扑状态值为：{}\n".format(state_val) +
        "规则：如果状态为奇数（1,3,5,7,9），请用激进、刚健、果断的语气；如果是偶数（2,4,6,8,10），请用阴柔、退让、保守的语气。\n"
        "请写一段 50 字以内的发言，不要任何废话。"
    )
    
    headers = {"Authorization": "Bearer " + str(API_KEY), "Content-Type": "application/json"}
    data = {"model": "deepseek-chat", "messages": [{"role": "user", "content": prompt}], "temperature": 0.3}
    try:
        r = requests.post(API_URL, headers=headers, json=data, timeout=30)
        return r.json()["choices"][0]["message"]["content"].strip()
    except Exception as e:
        return "[API异常] " + str(e)

# ==================== 3. 辩证法主引擎 ====================
class TopologicalDialectics:
    def __init__(self):
        self.cube_A = {c: 0 for c in CUBE_A_POINTS}
        self.cube_C = {c: 0 for c in CUBE_A_POINTS}
        self.cube_B = {c: 0 for c in CUBE_A_POINTS}

    def run(self, topic):
        print("=" * 60)
        print("⚖️ Polaris：纯整数手性辩证法引擎")
        print("=" * 60)
        
        # 1. 生成基础极性
        base_hash = sum(ord(c) for c in topic) % 9 + 1
        # 强制正题为奇数（刚健），确保阳刚起手
        state_A = (base_hash % 5) * 2 + 1 
        print("[系统注入] 题目初始哈希：{} | 正题强制奇数：{}".format(base_hash, state_A))
        
        # 2. 构建正方（甲）
        for i, c in enumerate(CUBE_A_POINTS):
            self.cube_A[c] = (state_A + i) % 10 or 10
            
        # 3. 构建反方（丙）：镜像翻转 + 阴阳对冲（强制偶数）
        for i, c in enumerate(CUBE_A_POINTS):
            target = mirror_flip(c)
            # 加 5 强制反转奇偶，制造绝对对立
            self.cube_C[target] = (self.cube_A[c] + 5) % 10 or 10 
            
        # 4. 构建合题（乙）：物理旋转融合
        for i, c in enumerate(CUBE_A_POINTS):
            target = rotate_120(c)
            # 取正反双方的平均值作为中和态
            fused_val = (self.cube_A[c] + self.cube_C[target]) // 2
            self.cube_B[target] = fused_val if fused_val != 0 else 10
            
        # 提取代表值
        final_A = list(self.cube_A.values())[0]
        final_C = list(self.cube_C.values())[0]
        final_B = list(self.cube_B.values())[0]
        
        print("\n--- 拓扑坐标演算完毕 ---")
        print("[正题 甲] 状态值：{}".format(final_A))
        print("[反题 丙] 状态值：{}".format(final_C))
        print("[合题 乙] 状态值：{}".format(final_B))
        
        # 5. 生成文本
        text_A = translate_state("正方/甲", final_A, topic)
        text_C = translate_state("反方/丙", final_C, topic)
        text_B = translate_state("合题/乙", final_B, topic)
        
        print("\n📢 [正方发言（甲）]:\n{}".format(text_A))
        print("\n📢 [反方发言（丙）]:\n{}".format(text_C))
        print("\n📢 [最终合题（乙）]:\n{}".format(text_B))
        
        # 6. 中宫 5 号审计与纠偏
        print("\n--- [中宫5号 拓扑审计] ---")
        is_odd = (final_B % 2 != 0) and (final_B != 10)
        
        if is_odd:
            print("✅ [PASS] 合题状态为 {}，纯正奇数，逻辑收敛！".format(final_B))
        else:
            print("❌ [WARN] 合题状态为 {}，落入偶/零态，大模型在和稀泥！".format(final_B))
            print("🚀 [中宫干涉] 触发【加5逃出生天】算子，强行拉升极性重写合题...")
            
            # 7. 自我纠偏：加 5 强制变阳，重新翻译
            corrected_B = (final_B + 5) % 10 or 10
            print("  -> 修正后的纯整数状态：{}".format(corrected_B))
            
            # 用修正后的极性，强制大模型重写
            text_B_corrected = translate_state("纠偏后的合题/乙", corrected_B, topic)
            print("\n📢 [中宫强制干预后的最终合题]:\n{}".format(text_B_corrected))

if __name__ == "__main__":
    if not API_KEY:
        print("⚠️ 未检测到 DEEPSEEK_API_KEY，自动切换模拟模式。\n")
        USE_REAL_API = False
        
    engine = TopologicalDialectics()
    engine.run("面对外敌挑衅，是否应该立刻武力反击？")
