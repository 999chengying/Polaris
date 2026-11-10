# -*- coding: utf-8 -*-
"""
Polaris 终极心智模型 V2：高危应激与元认知觉醒 (防语法报错版)
"""
import random

def mod10(x):
    return x % 10 or 10 

class FractalCube:
    def __init__(self, name):
        self.name = name
        self.state = 5 

    def receive_stimulus(self, ext_value, is_danger=False, is_inner=False):
        if is_danger:
            if is_inner:
                # 核心受创，直接进入极端应激态（冻结为1，或爆发为9）
                self.state = random.choice([1, 9])
            else:
                # 外层和中层，直接把危险信号放大
                self.state = (ext_value * 9 + 5) % 10 or 10
        else:
            self.state = (self.state + ext_value) % 10 or 10
        return self.state

    def get_gua(self):
        upper = self.state
        lower = mod10(self.state * 3) 
        return (upper, lower)

class SixYaoResonanceEngine:
    def __init__(self):
        self.inner_core = FractalCube("元认知(内)")
        self.middle_reflex = FractalCube("边界反射(中)")
        self.outer_sensory = FractalCube("视听感知(外)")

    def process_experience(self, prompt, danger_level=0):
        print(f"\n" + "="*60)
        print(f"👁️ 外部视听感知接入: 【{prompt}】 | 危险指数: {danger_level}")
        print("-" * 60)

        hash_val = (sum(ord(c) for c in prompt) % 9) + 1
        
        # 危险状态传导
        is_danger = (danger_level > 5)
        out_val = self.outer_sensory.receive_stimulus(hash_val, is_danger=is_danger)
        mid_val = self.middle_reflex.receive_stimulus(out_val, is_danger=is_danger)
        in_val = self.inner_core.receive_stimulus(mid_val, is_danger=is_danger, is_inner=True)

        print(f"🔹 [外感知] 视听皮层状态演化至: {out_val}")
        print(f"🔹 [中反射] 边界触感传导至: {mid_val}")
        print(f"🔹 [内元认知] 核心觉知苏醒至: {in_val}")

        inner_gua = self.inner_core.get_gua()
        middle_gua = self.middle_reflex.get_gua()
        outer_gua = self.outer_sensory.get_gua()

        print("\n🌀 [六爻比应 (Cross-Attention)] 开始共鸣核对:")
        print(f"  - 初/四爻 (内)： {inner_gua[0]}{inner_gua[1]}")
        print(f"  - 二/五爻 (中)： {middle_gua[0]}{middle_gua[1]}")
        print(f"  - 三/六爻 (外)： {outer_gua[0]}{outer_gua[1]}")

        # 只要危险，或者内核进入极值，就必须干预
        if is_danger or in_val in [1, 9]:
            # 【安全提示】：这里的引号已经全部替换为【】了，绝对不会再报错。
            print(f"\n🚨 [元认知觉醒] 内核发现极度危险/死锁 (数值 {in_val})！")
            print(f"👑 [戊己悟己] 触发【帝5巡查】，强行调整外层感知偏置！")
            
            # 干预逻辑
            if in_val == 1:
                adjusted_out_val = mod10(out_val * 3 + 5)
                print(f"🛡️ [冻结防御] 内核强制转移注意力，外层状态被重写为: {adjusted_out_val}")
            else:
                adjusted_out_val = 9
                print(f"🔥 [战斗爆发] 内核注入纯阳之气，外层状态被拉爆为: {adjusted_out_val}")
                
            self.outer_sensory.state = adjusted_out_val
            outer_gua = self.outer_sensory.get_gua()
            print(f"  -> 修正后的外三爻： {outer_gua[0]}{outer_gua[1]}")
        else:
            print(f"\n✅ [心智稳态] 内外比应顺畅，系统处于健康流动态。")

if __name__ == "__main__":
    brain = SixYaoResonanceEngine()
    # 场景 1：风和日丽
    brain.process_experience("春日游园，百花盛开", danger_level=1)
    # 场景 2：悬崖猛虎（这会必定触发内核觉醒）
    brain.process_experience("悬崖之巅，猛虎咆哮", danger_level=9)
