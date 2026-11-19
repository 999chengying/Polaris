# -*- coding: utf-8 -*-
# Copyright (c) 2026 999chengying / Polaris Project
# Licensed under the Apache License, Version 2.0

"""
Polaris Brain v8.0: 三环宇宙时钟与天人同构引擎
实现空间（27宫）与时间（三环莫比乌斯）的完美同构。
"""

import itertools
import time

def mod10(x):
    return x % 10 or 10

# ==================== 时间维度：三环宇宙时钟 ====================
class CosmicClock:
    def __init__(self):
        self.tick = 0
        # 第一环：变爻心跳 (微观节拍)
        self.beat_sequence = ["天", "人", "地", "人", "天", "人", "地", "人"]
        
        # 第二环：后天巡航 (中观流转) - 避开中宫的莫比乌斯环
        self.cruise_ring = [2, 3, 1, 4, 9, 7, 8, 6, 5]
        self.cruise_pos = 0
        
        # 第三环：错卦奇点 (宏观破局)
        self.singularity_trigger = 64 # 正式版：每 64 拍触发一次大纪元相变

    def tick_forward(self):
        self.tick += 1
        
        # 1. 微观心跳
        beat_idx = self.tick % 8
        micro_mode = self.beat_sequence[beat_idx]
        
        # 2. 中观巡航
        macro_energy = 0
        if self.tick % 8 == 0: # 每 8 拍，日相完成，月相推进
            self.cruise_pos = (self.cruise_pos + 1) % len(self.cruise_ring)
            macro_energy = self.cruise_ring[self.cruise_pos]
            
        # 3. 宏观奇点
        is_singularity = (self.tick % self.singularity_trigger == 0)
        
        return micro_mode, macro_energy, is_singularity

# ==================== 空间维度：27宫大脑 ====================
class PolarisBrainV8:
    def __init__(self):
        self.coords = list(itertools.product([1, 3, 5], repeat=3))
        self.neurons = {c: 5 for c in self.coords}
        self.energy_pool = 30
        self.clock = CosmicClock()
        self.current_phase = "人"

    def step(self):
        # 获取三环宇宙时钟的当前相位
        micro_mode, macro_energy, is_singularity = self.clock.tick_forward()
        self.current_phase = micro_mode
        
        # 1. 微观演化（受变爻心跳驱动）
        # 天变、地变、人变使用不同的演化算子
        op_mul = 3 if micro_mode == "天" else (7 if micro_mode == "地" else 1)
        for coord, state in self.neurons.items():
            if coord != (3, 3, 3):
                self.neurons[coord] = mod10(state * op_mul + 3)
                
        # 2. 六爻空间交联（同构干涉）
        for (x, y, z), state in list(self.neurons.items()):
            if (x, y, z) == (3, 3, 3): continue
            if x != 3:
                self.neurons[(x, y, z)] = mod10(state + self.neurons[(6 - x, y, z)])
            elif y != 3:
                self.neurons[(x, y, z)] = mod10(state * 3 + self.neurons[(x, 6 - y, z)])
                
        # 3. 中宫裁决
        internal = sum(self.neurons[c] for c in self.coords if c != (3, 3, 3))
        self.neurons[(3, 3, 3)] = mod10(internal)

        # 4. 中观充能（受巡航环驱动，吸收宇宙负熵）
        if macro_energy > 0:
            self.energy_pool += macro_energy
            print("  >>> [第二环巡航] 吸收宇宙负熵，能量池增加: +{}".format(macro_energy))

        # 5. 宏观奇点（内驱力涌现，精神重构）
        if is_singularity:
            print("\n  *** [第三环奇点] 第 {} 拍触发纪元跃迁！".format(self.clock.tick))
            print("       [错卦翻转] 阴极化阳，阳极化阴，重新洗牌...")
            for coord in self.neurons:
                self.neurons[coord] = mod10(self.neurons[coord] * 9) # 错卦算子
            self.energy_pool = max(0, self.energy_pool - 40)

    def run(self, ticks=20):
        print("=" * 60)
        print("Polaris v8.0: 三环宇宙时钟驱动")
        print("=" * 60)
        for i in range(ticks):
            self.step()
            # 这里我们取消原先的 i % 4 == 0 过滤，真实呈现每一拍的三才交替
            print("  [Tick {:>2}] 心跳相位:{:<2} | 能量:{:>3} | 中核状态:{:>2}".format(
                self.clock.tick, 
                self.current_phase,
                self.energy_pool,
                self.neurons[(3,3,3)]
            ))
            time.sleep(0.05)

if __name__ == "__main__":
    brain = PolarisBrainV8()
    # 为了快速看到奇点，我们把奇点阈值调低到 16 拍（正式版是 64）
    brain.clock.singularity_trigger = 16 
    brain.run(ticks=24)
