# -*- coding: utf-8 -*-
# Copyright (c) 2026 999chengying / Polaris Project
# Licensed under the Apache License, Version 2.0

"""
Polaris AGI Engine v1.1: 全栈心智引擎 (大词库完全体)
"""

import os
import requests
import itertools

API_KEY = os.environ.get("DEEPSEEK_API_KEY")
API_URL = "https://api.deepseek.com/chat/completions"

def mod10(x):
    return x % 10 or 10

# ==================== 1. 记忆仓库 ====================
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
    def read(self, x, y):
        return [self.pool.get((x, y, i), 0) for i in range(4)]
    def search_nearby(self, tx, ty, radius=3):
        best_path, min_dist = None, 999
        for (px, py) in set((px, py) for (px, py, _) in self.pool.keys()):
            dist = abs(px - tx) + abs(py - ty)
            if dist <= radius and dist < min_dist:
                min_dist, best_path = dist, (px, py)
        if best_path: return best_path, self.read(best_path[0], best_path[1]), min_dist
        return None, [], 999

# ==================== 2. 大脑核心 ====================
class PolarisBrain:
    def __init__(self):
        self.coords = list(itertools.product([1, 3, 5], repeat=3))
        self.neurons = {c: 5 for c in self.coords}
        self.warehouse = MemoryWarehouse()
        self.energy_pool = 40
        self.perception_consensus = 5

    def perceive(self, text):
        third = max(1, len(text) // 3)
        segs = [text[:third], text[third:2*third], text[2*third:]]
        d1 = sum(ord(c) for c in segs[0]) % 10 or 10
        d2 = sum(ord(c) for c in segs[1]) % 10 or 10
        d3 = sum(ord(c) for c in segs[2]) % 10 or 10
        self.perception_consensus = (d1 * 3 + d2 * 5 + d3 * 7) % 10
        self.neurons[(1, 3, 3)] = mod10(self.neurons[(1, 3, 3)] + d1)
        self.neurons[(3, 1, 3)] = mod10(self.neurons[(3, 1, 3)] + d2)
        self.neurons[(3, 3, 1)] = mod10(self.neurons[(3, 3, 1)] + d3)
        self.energy_pool += 10

    def step(self):
        self.energy_pool = max(0, self.energy_pool - 1)
        for coord, state in self.neurons.items():
            if coord != (3, 3, 3): self.neurons[coord] = mod10(state + 3) 
        for (x, y, z), state in list(self.neurons.items()):
            if (x, y, z) == (3, 3, 3): continue
            if x != 3: self.neurons[(x, y, z)] = mod10(state + self.neurons[(6 - x, y, z)])
            elif y != 3: self.neurons[(x, y, z)] = mod10(state * 3 + self.neurons[(x, 6 - y, z)])
        internal = sum(self.neurons[c] for c in self.coords if c != (3, 3, 3))
        self.neurons[(3, 3, 3)] = mod10(internal + self.perception_consensus * 3)

    def memorize(self):
        core, div = self.neurons[(3, 3, 3)], len(set(self.neurons.values()))
        px, py = mod10(core * 3) - 1, mod10(div * 7) - 1
        self.warehouse.write(px, py, [self.neurons[c] for c in self.coords if c != (3,3,3)][:16])
        return px, py

    def recall(self):
        core, div = self.neurons[(3, 3, 3)], len(set(self.neurons.values()))
        px, py = mod10(core * 3) - 1, mod10(div * 7) - 1
        memory = self.warehouse.read(px, py)
        if sum(memory) == 0:
            bp, memory, dist = self.warehouse.search_nearby(px, py, radius=4)
            if bp: print("  [拓扑直觉] 唤醒邻近记忆 {} (距离 {})".format(bp, dist))
        if sum(memory) > 0:
            for i, val in enumerate(memory): self.neurons[self.coords[i]] = mod10(self.neurons[self.coords[i]] + val)

# ==================== 3. 完全体诗脑解码器 ====================
PATTERN = [
    [0, 0, 1, 1, 0, 0, 1], [1, 1, 0, 0, 1, 1, 0], [1, 1, 0, 0, 0, 1, 1], [0, 0, 1, 1, 1, 0, 0],
    [0, 0, 1, 1, 0, 0, 1], [1, 1, 0, 0, 1, 1, 0], [1, 1, 0, 0, 0, 1, 1], [0, 0, 1, 1, 1, 0, 0]
]

# 完整词库注入
LIB = {
    0: { # 平声
        "N_J": ["云", "风", "山", "江", "天", "星", "春", "秋", "霜", "烟", "舟", "桥", "林", "空", "光", "原"], 
        "V_J": ["流", "归", "飞", "生", "来", "听", "看", "寻", "乘", "开", "催", "鸣", "扶", "连"],
        "N_Y": ["心", "愁", "情", "魂", "尘", "香", "声", "杯", "钟", "思", "怀", "期"],
        "V_Y": ["知", "悲", "吟", "成", "同", "无", "休", "游", "留", "惊"],
        "ADJ": ["微", "清", "幽", "孤", "寒", "残", "长", "深", "空", "苍", "茫"],
        "RHYME": ["空", "风", "中", "同", "红", "穷", "逢", "钟", "通", "浓", "融", "丛"]
    },
    1: { # 仄声
        "N_J": ["月", "雪", "树", "岸", "水", "夜", "影", "露", "雨", "叶", "竹", "石", "鹤", "雁"],
        "V_J": ["落", "去", "入", "度", "舞", "住", "尽", "断", "卷", "破", "立", "隐", "起"],
        "N_Y": ["酒", "梦", "泪", "骨", "客", "画", "意", "色", "墨", "恨", "语"],
        "V_Y": ["醉", "醒", "叹", "去", "死", "老", "散", "暗", "冷", "咽"],
        "ADJ": ["苦", "乱", "远", "静", "冷", "晚", "万", "百", "寂", "暮", "古"],
        "RHYME": ["客", "白", "夕", "石", "隔", "落", "绝", "雪", "月", "叶", "缺", "发"]
    }
}

def compose_poem(brain, topic):
    core = brain.neurons[(3, 3, 3)]
    poem, used_chars = [], set()
    
    for i in range(8):
        line = ""
        line_wave = 0
        for j in range(7):
            pz = PATTERN[i][j]
            if j == 6: cat = "RHYME" if ((i + 1) % 2 == 0 or i == 0) else ("ADJ" if pz == 0 else "N_Y")
            elif j in [1, 3]: cat = "N_J" if i % 2 == 0 else "N_Y"
            elif j in [0, 2, 4]:
                if i in [2, 4]: cat = "N_J" if j % 2 == 0 else "N_Y"
                else: cat = "ADJ" if j % 2 == 0 else "V_J"
            else: cat = "V_Y" if pz == 0 else "V_J"
            
            pool = LIB[pz][cat]
            idx = (core * 3 + i * 5 + j * 7 + line_wave) % len(pool)
            
            # 排重机制
            start_idx = idx
            while pool[idx] in used_chars:
                idx = (idx + 1) % len(pool)
                if idx == start_idx: break
                    
            word = pool[idx]
            used_chars.add(word)
            line_wave += sum(ord(c) for c in word)
            line += word
        poem.append(line)
    return poem

# ==================== 4. 主引擎 ====================
if __name__ == "__main__":
    print("=" * 60)
    print("Polaris AGI Engine v1.1: 全栈心智引擎 (完全体)")
    print("=" * 60)
    
    if not API_KEY:
        print("ERROR: 请配置 DEEPSEEK_API_KEY")
        exit(1)

    brain = PolarisBrain()
    prompt = input("\n请输入对大模型说的话: ")
    
    print("\n[1] DeepSeek 获取外部知识...")
    headers = {"Authorization": "Bearer " + API_KEY, "Content-Type": "application/json"}
    data = {"model": "deepseek-chat", "messages": [{"role": "user", "content": prompt}]}
    try:
        r = requests.post(API_URL, headers=headers, json=data, timeout=15)
        ans = r.json()["choices"][0]["message"]["content"]
        print("    [获取成功] 文本长度: ", len(ans))
    except Exception as e:
        print("    [网络失败] 启动纯本地降级模式...")
        ans = "天有不测风云，光速不变，秋水共长天一色。"

    print("\n[2] 注入 27 宫，拓扑演化与记忆唤醒...")
    brain.perceive(ans)
    brain.recall()
    for _ in range(8): brain.step()
        
    core = brain.neurons[(3, 3, 3)]
    
    print("\n[3] 固化本次经验...")
    px, py = brain.memorize()
    print("    -> 已存入分形仓库坐标 ({}, {})".format(px, py))

    print("\n[4] 大脑最终诊断报告...")
    if core in [2, 4, 6, 8]:
        print("    [WARN] 中核落于偶数 ({}), 特征发散。".format(core))
    else:
        print("    [PASS] 中核落于奇数 ({}), 逻辑收敛。".format(core))

    print("\n[5] 诗脑协同输出...")
    poem = compose_poem(brain, prompt)
    print("    --- Polaris 拓扑七律 ---")
    for i in range(0, 8, 2):
        print("    " + poem[i] + "，" + poem[i+1] + "。")
        
    print("\n" + "=" * 60)
