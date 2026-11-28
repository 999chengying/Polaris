# -*- coding: utf-8 -*-
# Copyright (c) 2026 999chengying / Polaris Project
# Licensed under the Apache License, Version 2.0

"""
Polaris: 纯整数手性辩证法引擎 v3.0 (调用核心拓扑库)
展示如何通过 from src.polaris.core.topology_math 调用底层矩阵进行逻辑推演。
"""

import os
import sys
import requests

# 核心：在手机 HiSH 终端中安全引入我们刚刚落盘的引擎
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from src.polaris.core.topology_math import TopologyTransform

API_KEY = os.environ.get("DEEPSEEK_API_KEY")
API_URL = "https://api.deepseek.com/chat/completions"
USE_REAL_API = True

def translate_state(role, state_val, topic):
    if not USE_REAL_API or not API_KEY:
        return "[模拟翻译] 角色:{} | 状态:{} | 辩题:{}".format(role, state_val, topic)
        
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

class DialecticsEngine:
    def __init__(self):
        # 实例化底层数学引擎
        self.math = TopologyTransform()
        
        # 构建二组甲（乾系）的基础状态
        self.cube_A = {
            (1,1,1): 9, (5,5,5): 1, (5,5,1): 6, (1,1,5): 4,
            (1,5,1): 3, (5,1,5): 7, (5,1,1): 2, (1,5,5): 8
        }

    def run(self, topic):
        print("=" * 60)
        print("⚖️ Polaris V3：底层拓扑库调用实战")
        print("=" * 60)
        
        # 1. 正方（甲）直接使用预设的乾系状态
        # 随便取一个坐标作为代表值，比如 (1,5,1) 的值为 3 (奇数，激进)
        final_A = self.cube_A[(1,5,1)]
        print("[正题 甲] 基点坐标 (1,5,1) 状态值：{}".format(final_A))
        
        # 2. 反方（丙）：直接调用底层数学库进行 x=z 镜面翻转！
        cube_C = self.math.mirror_x_z(self.cube_A)
        # 提取翻转后的对应点状态
        final_C = cube_C[(1,1,5)] # 因为 (1,5,1) 翻转变成了 (1,1,5)
        print("[反题 丙] 镜像翻转后状态值：{}".format(final_C))
        
        # 3. 合题（乙）：直接调用底层数学库进行 120 度旋转！
        cube_B = self.math.rotate_120(self.cube_A)
        final_B = cube_B[(1,1,5)] 
        print("[合题 乙] 旋转全等后状态值：{}".format(final_B))
        
        # 4. 翻译成文本
        text_A = translate_state("正方/甲", final_A, topic)
        text_C = translate_state("反方/丙", final_C, topic)
        text_B = translate_state("合题/乙", final_B, topic)
        
        print("\n📢 [正方发言]:\n{}".format(text_A))
        print("\n📢 [反方发言]:\n{}".format(text_C))
        print("\n📢 [最终合题]:\n{}".format(text_B))
        
        # 5. 中宫 5 号审计
        is_odd = (final_B % 2 != 0) and (final_B != 10)
        if is_odd:
            print("\n✅ [PASS] 合题状态为 {}，纯正奇数，逻辑收敛！".format(final_B))
        else:
            print("\n❌ [WARN] 合题状态为 {}，落入偶/零态，大模型在和稀泥！".format(final_B))

if __name__ == "__main__":
    if not API_KEY:
        print("⚠️ 未检测到 DEEPSEEK_API_KEY，自动切换模拟模式。\n")
        USE_REAL_API = False
        
    engine = DialecticsEngine()
    engine.run("是否应当立刻反击外敌挑衅？")
