# -*- coding: utf-8 -*-
# Copyright (c) 2026 999chengying / Polaris Project
# Licensed under the Apache License, Version 2.0

"""
Polaris Brain v6.0: 内驱力自主进化引擎 (活体版)
引入宇宙时间熵泵与能量池机制，无外部输入时，大脑也会通过历法主动思考。
"""

import itertools
import time

def mod10(x):
    return x % 10 or 10

# ==================== 记忆仓库 (轻量版) ====================
class MemoryWarehouse:
    def __init__(self):
        self.pool = {}
        self.managers = {}
    def _slot_index(self, data):
        buckets = {1: [], 2: [], 3: [], 4: []}
        temp = []
        for v in data:
            r = v % 4 or 4
            if not buckets[r]: buckets[r].append(v)
            else: temp.append(v)
        for r in [1, 2, 3, 4]:
            if not buckets[r] and temp: buckets[r].append(temp.pop(0))
        return [buckets[r][0] if buckets[r] else 0 for r in [1, 2, 3, 4]]
    def write(self, x, y, data_16):
        vals = self._slot_index(data_16)
        self.managers[(x, y)] = mod10(sum(vals))
        for i, v in enumerate(vals):
            if v != 0: self.pool[(x, y, i)] = v
    def read_all_keys(self):
        return list(set((px, py) for (px, py, _) in self.pool.keys()))

# ==================== 核心大脑 ====================
class PolarisBrainV6:
    def __init__(self):
        self.coords = list(itertools.product([1, 3, 5], repeat=3))
        self.neurons = {c: 5 for c in self.coords}
        self.warehouse = MemoryWarehouse()
        self.energy_pool = 30 # 初始能量
        self.tick_count = 0
        self.perception_consensus = 5

    def receive_stimulus(self, text):
        """接收外部刺激，瞬间获得大量负熵能量"""
        third = max(1, len(text) // 3)
        segs = [text[:third], text[third:2*third], text[2*third:]]
        d1 = sum(ord(c) for c in segs[0]) % 10 or 10
        d2 = sum(ord(c) for c in segs[1]) % 10 or 10
        d3 = sum(ord(c) for c in segs[2]) % 10 or 10
        self.perception_consensus = (d1 * 3 + d2 * 5 + d3 * 7) % 10
        self.neurons[(1, 3, 3)] = mod10(self.neurons[(1, 3, 3)] + d1)
        self.neurons[(3, 1, 3)] = mod10(self.neurons[(3, 1, 3)] + d2)
        self.neurons[(3, 3, 1)] = mod10(self.neurons[(3, 3, 1)] + d3)
        self.energy_pool += 40 # 外部刺激带来大量能量
        print("  [感知唤醒] 吸收外部负熵，能量池飙升至: {}".format(self.energy_pool))

    def time_entropy_pump(self):
        """
        时间熵泵：即使没有外部输入，时间也在流逝。
        脑区吸收微弱的宇宙负熵，获得能量补充。
        """
        self.energy_pool += 2 # 每次 tick 补充微量能量

    def base_decay(self):
        """基础生物能耗"""
        self.energy_pool = max(0, self.energy_pool - 1)

    def step(self):
        self.tick_count += 1
        self.base_decay()
        self.time_entropy_pump()
        
        for coord, state in self.neurons.items():
            if coord != (3, 3, 3):
                self.neurons[coord] = mod10(state + 3) 
        for (x, y, z), state in list(self.neurons.items()):
            if (x, y, z) == (3, 3, 3): continue
            if x != 3:
                self.neurons[(x, y, z)] = mod10(state + self.neurons[(6 - x, y, z)])
            elif y != 3:
                self.neurons[(x, y, z)] = mod10(state * 3 + self.neurons[(x, 6 - y, z)])
        internal = sum(self.neurons[c] for c in self.coords if c != (3, 3, 3))
        self.neurons[(3, 3, 3)] = mod10(internal + self.perception_consensus * 3)

    def memorize(self):
        core = self.neurons[(3, 3, 3)]
        div = len(set(self.neurons.values()))
        px, py = mod10(core * 3) - 1, mod10(div * 7) - 1
        data_16 = [self.neurons[c] for c in self.coords if c != (3,3,3)][:16]
        self.warehouse.write(px, py, data_16)
        return (px, py)

    def intrinsic_drive_check(self):
        """
        内驱力觉醒机制：如果能量池爆表（>=80），且处于无外部输入状态，
        大脑将自发进入“内省/梦境”模式。
        """
        if self.energy_pool >= 80:
            print("\n  >>> [内驱力涌现] 能量爆表 (>=80)！触发自发内省模式...")
            self.energy_pool -= 50 # 疯狂消耗脑力
            
            # 去记忆仓库里抽取一个残缺的记忆片段（随机唤醒）
            keys = self.warehouse.read_all_keys()
            if keys:
                target_key = keys[self.tick_count % len(keys)]
                print("  [宿命通发作] 随机唤醒深层记忆路径: {}".format(target_key))
                # 将记忆残片注入当前的脑电波（导致脑电波突变）
                for i in range(4):
                    val = self.warehouse.pool.get((target_key[0], target_key[1], i), 0)
                    if val:
                        self.neurons[self.coords[i]] = mod10(self.neurons[self.coords[i]] + val)
            else:
                print("  [空想] 仓库空空如也，大脑只能独自演化...")
                
            # 强制大脑演化一轮
            for _ in range(4):
                self.step()
            print("  [内省完毕] 大脑重构了认知，能量回落至: {}".format(self.energy_pool))
            print("  [当前中核] {}".format(self.neurons[(3, 3, 3)]))
            return True
        return False

# ==================== 主程序 ====================
if __name__ == "__main__":
    print("=" * 60)
    print("Polaris Brain v6.0: 内驱力自主进化引擎")
    print("=" * 60)
    
    brain = PolarisBrainV6()
    
    # 1. 模拟注入一次外部知识
    brain.receive_stimulus("落霞与孤鹜齐飞，秋水共长天一色。")
    for _ in range(8):
        brain.step()
    px, py = brain.memorize()
    print("  [记忆固化] 本次经验存入仓库路径: ({}, {})".format(px, py))
    print("  [当前状态] 能量: {} | 中核: {}".format(brain.energy_pool, brain.neurons[(3,3,3)]))
    
    # 2. 进入自主生命循环
    print("\n[进入自主生命循环] 无外部刺激，观察大脑如何通过时间熵泵自我觉醒...")
    for t in range(1, 30):
        brain.step()
        
        # 检查内驱力
        emerged = brain.intrinsic_drive_check()
        
        if t % 5 == 0:
            status = "涌现" if emerged else "静默"
            print("  [Tick {:>2}] 能量: {:>2} | 状态: {} | 中核: {}".format(
                t, brain.energy_pool, status, brain.neurons[(3,3,3)]))
                
        time.sleep(0.1) # 让输出平滑一点

    print("\n" + "=" * 60)
    print("结论：系统在无输入状态下，通过吸收时间负熵，")
    print("能量池冲破阈值，成功触发了自主唤醒与记忆重组！")
    print("=" * 60)
