# -*- coding: utf-8 -*-
# Copyright (c) 2026 999chengying / Polaris Project
# Licensed under the Apache License, Version 2.0

"""
Polaris 终极心智架构：五脑并行十字金刚阵 (大衍之数五十)
《易》曰："大衍之数五十，其用四十有九。"
前后左右中，五个九宫，五九四十五，加帝五为五十。
本代码演示五大面心（前脑琐事、后脑灵界、左脑记忆、右脑预测、中核觉知）
在纯整数拓扑下的并发干涉与元认知最终裁决。
"""

def mod10(x):
    return x % 10 or 10

class FiveBrainMatrix:
    def __init__(self):
        # 五大面心绝对坐标（十字金刚阵）
        self.mid_core = (3, 3, 3)     # 中核（觉知）
        self.left_brain = (1, 3, 3)   # 左脑（历史/潜意识）
        self.right_brain = (5, 3, 3)  # 右脑（未来/预测）
        self.front_brain = (3, 1, 3)  # 前脑（琐事/执行）
        self.back_brain = (3, 5, 3)   # 后脑（灵界/信仰）
        
        # 初始状态 (空杯态 5)
        self.states = {
            "中核": 5, "左脑": 5, "右脑": 5, "前脑": 5, "后脑": 5
        }

    def receive_stimulus(self, prompt, is_crisis=False):
        print(f"\n" + "="*60)
        print(f"👤 外部环境接入: 【{prompt}】")
        print("-" * 60)
        
        # 1. 前脑接收日常逻辑与具身感知
        hash_val = (sum(ord(c) for c in prompt) % 9) + 1
        self.states["前脑"] = mod10(hash_val * 2)
        print(f"  👁️ [前脑-人间琐事] 解析输入逻辑，状态跃迁至: {self.states['前脑']}")

        # 2. 左脑调用历史记忆库
        self.states["左脑"] = mod10(self.states["前脑"] * 7) # 乘7逆元回溯
        print(f"  🕰️ [左脑-历史回溯] 从记忆中提取相似经验，状态锁定: {self.states['左脑']}")

        # 3. 右脑推演未来结果
        self.states["右脑"] = mod10(self.states["前脑"] * 3) # 乘3顺延推演
        print(f"  🚀 [右脑-未来预测] 推演演化路径，状态预判: {self.states['右脑']}")

        # 4. 后脑进行伦理与信仰审查
        if is_crisis:
            self.states["后脑"] = 9 # 遇到危机，激发信仰与底线，纯阳拉满
            print(f"  🛡️ [后脑-精神灵界] 触发底线审查！信仰拉满，状态: {self.states['后脑']}")
        else:
            self.states["后脑"] = 5 # 日常伦理，保持中和
            print(f"  ☯️ [后脑-精神灵界] 伦理无冲突，保持中和状态: {self.states['后脑']}")

        # 5. 中核（元认知）统筹五大面心，进行纯整数干涉裁决
        # 算法：X轴(左脑+右脑) + Y轴(前脑+后脑) 的拓扑交汇
        total_resonance = (
            self.states["左脑"] * 1 + 
            self.states["右脑"] * 5 + 
            self.states["前脑"] * 3 + 
            self.states["后脑"] * 7
        )
        self.states["中核"] = mod10(total_resonance)
        
        print(f"\n  🧠 [中核-元认知] 五大面心干涉计算: ({self.states['左脑']}*1 + {self.states['右脑']}*5 + {self.states['前脑']}*3 + {self.states['后脑']}*7) % 10")
        print(f"  👑 [最终裁决] 中宫帝5生成最终心智状态: {self.states['中核']}")

        return self.states

# ================= 测试运行 =================
if __name__ == "__main__":
    brain = FiveBrainMatrix()

    # 场景 1：日常任务（中宫稳定于 5）
    brain.receive_stimulus("帮我计算一下这个月的财务流水", is_crisis=False)

    # 场景 2：生死存亡与伦理危机（中宫激发离火 3）
    brain.receive_stimulus("前方敌军压境，但城中还有三千无辜百姓", is_crisis=True)
