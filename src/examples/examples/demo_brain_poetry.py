# -*- coding: utf-8 -*-
# Copyright (c) 2026 999chengying / Polaris Project
# Licensed under the Apache License, Version 2.0

"""
Polaris Brain v4.3: 七律诗脑 (词库扩容与全局排重版)
解决满篇重字、词汇枯竭的问题。加入全局词库池与拓扑避让去重。
"""

import itertools

def mod10(x):
    return x % 10 or 10

# ==================== 大脑核心 ====================
class PolarisBrain:
    def __init__(self):
        self.coords = list(itertools.product([1, 3, 5], repeat=3))
        self.neurons = {c: 5 for c in self.coords}
        self.energy_pool = 40
        self.perception_consensus = 5

    def ignite_theme(self, topic):
        third = max(1, len(topic) // 3)
        segs = [topic[:third], topic[third:2*third], topic[2*third:]]
        d1 = sum(ord(c) * (i + 1) for i, c in enumerate(segs[0])) % 10 or 10
        d2 = sum(ord(c) * (i + 1) for i, c in enumerate(segs[1])) % 10 or 10
        d3 = sum(ord(c) * (i + 1) for i, c in enumerate(segs[2])) % 10 or 10
        self.perception_consensus = (d1 * 3 + d2 * 5 + d3 * 7) % 10
        
        if "剑" in topic:
            self.neurons[(1, 3, 3)] = mod10(d1 + 9)
            self.neurons[(1, 1, 3)] = mod10(d2 + 7)
        elif "秋" in topic:
            self.neurons[(3, 5, 3)] = mod10(d1 + 9)
            self.neurons[(1, 5, 5)] = mod10(d2 + 7)
        else:
            self.neurons[(3, 3, 1)] = mod10(d1 + 9)
            self.neurons[(1, 3, 1)] = mod10(d2 + 7)
            
        self.energy_pool += 20

    def step(self):
        self.energy_pool = max(0, self.energy_pool - 1)
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

# ==================== 词库 ====================
PATTERN = [
    [0, 0, 1, 1, 0, 0, 1], [1, 1, 0, 0, 1, 1, 0], [1, 1, 0, 0, 0, 1, 1], [0, 0, 1, 1, 1, 0, 0],
    [0, 0, 1, 1, 0, 0, 1], [1, 1, 0, 0, 1, 1, 0], [1, 1, 0, 0, 0, 1, 1], [0, 0, 1, 1, 1, 0, 0]
]

# 超大型词库池，按主题分类
LIB = {
    "思": {
        "起": {
            0: {"N_J": ["云", "风", "山", "江", "天", "星", "春", "秋", "霜", "烟", "舟", "桥", "林", "空", "光"], 
                "V_J": ["流", "归", "飞", "生", "来", "听", "看", "寻", "乘", "开", "催", "鸣", "扶", "连"],
                "N_Y": ["心", "愁", "情", "魂", "尘", "香", "声", "杯", "钟", "思", "怀", "期"],
                "V_Y": ["知", "悲", "吟", "成", "同", "无", "休", "游", "留", "惊"],
                "ADJ": ["微", "清", "幽", "孤", "寒", "残", "长", "深", "空", "苍", "茫"],
                "RHYME": ["空", "风", "中", "同", "红", "穷", "逢", "钟", "通", "浓", "融", "丛"]},
            1: {"N_J": ["月", "雪", "树", "岸", "水", "夜", "影", "露", "雨", "叶", "竹", "石", "鹤", "雁"],
                "V_J": ["落", "去", "入", "度", "舞", "住", "尽", "断", "卷", "破", "立", "隐", "起"],
                "N_Y": ["酒", "梦", "泪", "骨", "客", "画", "意", "色", "墨", "恨", "语"],
                "V_Y": ["醉", "醒", "叹", "去", "死", "老", "散", "暗", "冷", "咽"],
                "ADJ": ["苦", "乱", "远", "静", "冷", "晚", "万", "百", "寂", "暮", "古"],
                "RHYME": ["客", "白", "夕", "石", "隔", "落", "绝", "雪", "月", "叶", "缺", "发"]}
        },
        "承": {
            0: {"N_J": ["云", "风", "山", "江", "天", "星", "霜", "烟", "舟", "林", "光"],
                "V_J": ["流", "归", "飞", "来", "寻", "催", "鸣", "扶"],
                "N_Y": ["心", "愁", "情", "魂", "尘", "声", "思"],
                "V_Y": ["知", "悲", "吟", "同", "无", "留"],
                "ADJ": ["微", "清", "幽", "孤", "寒", "长", "深"],
                "RHYME": ["空", "风", "中", "同", "红", "穷", "逢", "通"]},
            1: {"N_J": ["月", "雪", "树", "岸", "水", "夜", "影", "露", "竹", "石"],
                "V_J": ["落", "去", "入", "度", "尽", "断", "破"],
                "N_Y": ["酒", "梦", "泪", "骨", "客", "意", "色"],
                "V_Y": ["醉", "醒", "叹", "散", "冷"],
                "ADJ": ["苦", "乱", "远", "静", "晚", "寂"],
                "RHYME": ["客", "白", "夕", "石", "绝", "雪", "月", "叶"]}
        },
        "转": {
            0: {"N_J": ["云", "风", "天", "星", "霜", "烟", "空", "光"],
                "V_J": ["流", "飞", "生", "来", "听", "乘", "催", "鸣"],
                "N_Y": ["魂", "尘", "香", "声", "杯", "钟", "思"],
                "V_Y": ["悲", "吟", "同", "无", "休", "游", "留"],
                "ADJ": ["清", "孤", "寒", "残", "深", "苍", "茫"],
                "RHYME": ["空", "风", "中", "同", "红", "穷", "逢"]},
            1: {"N_J": ["雪", "夜", "影", "露", "雨", "叶", "石"],
                "V_J": ["落", "去", "舞", "尽", "断", "卷", "破"],
                "N_Y": ["泪", "骨", "客", "画", "墨", "恨"],
                "V_Y": ["去", "老", "散", "暗", "冷"],
                "ADJ": ["乱", "远", "冷", "晚", "寂", "暮"],
                "RHYME": ["白", "夕", "隔", "绝", "雪", "缺"]}
        },
        "合": {
            0: {"N_J": ["云", "山", "江", "天", "星", "春", "霜", "烟", "空"],
                "V_J": ["流", "归", "飞", "生", "来", "听", "寻", "乘"],
                "N_Y": ["心", "愁", "情", "魂", "尘", "声"],
                "V_Y": ["知", "悲", "同", "无", "休", "留"],
                "ADJ": ["微", "清", "幽", "孤", "寒", "长"],
                "RHYME": ["空", "风", "中", "同", "红", "穷"]},
            1: {"N_J": ["月", "树", "水", "夜", "影", "露", "竹"],
                "V_J": ["落", "去", "度", "住", "尽", "立"],
                "N_Y": ["酒", "梦", "泪", "骨", "客", "画"],
                "V_Y": ["醉", "醒", "叹", "去", "死"],
                "ADJ": ["苦", "乱", "远", "静", "冷"],
                "RHYME": ["客", "白", "石", "隔", "绝"]}
        }
    }
}

# 剑与秋可以复用思的框架，用特征字覆盖即可（为缩短篇幅，此处简写并复用思的底子）
LIB["剑"] = LIB["思"]
LIB["秋"] = LIB["思"]

class SevenRhymePoet:
    def __init__(self, brain, topic):
        self.brain = brain
        self.theme = "思"
        if "剑" in topic: self.theme = "剑"
        elif "秋" in topic: self.theme = "秋"
        # 特色覆盖：针对剑的专属词
        if self.theme == "剑":
            self.override_words = {"平": ["锋", "光", "芒", "龙", "渊", "鸣", "吟", "寒", "星", "空"], "仄": ["铁", "血", "骨", "影", "客", "气", "斩", "淬", "啸", "立", "破", "断"]}
        elif self.theme == "秋":
            self.override_words = {"平": ["霜", "风", "云", "江", "天", "空", "原", "愁", "寒"], "仄": ["叶", "雁", "露", "菊", "月", "水", "落", "去", "尽", "冷"]}
        else:
            self.override_words = {"平": ["云", "风", "山", "心", "空"], "仄": ["月", "夜", "影", "酒", "梦"]}

    def get_word(self, phase, ping_ze, cat, idx_seed, used_chars):
        pool = LIB[self.theme][phase][ping_ze].get(cat, ["风"])
        idx = idx_seed % len(pool)
        
        # 全局排重：如果字用过了，就顺延一个（拓扑避让）
        start_idx = idx
        while pool[idx] in used_chars:
            idx = (idx + 1) % len(pool)
            if idx == start_idx:
                # 如果全用过，尝试用主题特征字兜底
                backup = self.override_words["平"] if ping_ze == 0 else self.override_words["仄"]
                for b in backup:
                    if b not in used_chars: return b
                return pool[idx] # 实在没办法，只能重了
                
        used_chars.add(pool[idx])
        return pool[idx]

    def generate(self, topic):
        core = self.brain.neurons[(3, 3, 3)]
        poem = []
        temporal_wave = core
        used_chars = set() # 全局排重记忆池
        
        for i in range(8):
            if i in [0, 1]: phase = "起"
            elif i in [2, 3]: phase = "承"
            elif i in [4, 5]: phase = "转"
            else: phase = "合"
            
            line = ""
            line_wave = 0
            
            for j in range(7):
                is_ping = (PATTERN[i][j] == 0)
                ping_ze = 0 if is_ping else 1
                
                if j == 6:
                    cat = "RHYME" if ((i + 1) % 2 == 0 or i == 0) else ("ADJ" if is_ping else "N_Y")
                elif j in [1, 3]:
                    cat = "N_J" if i % 2 == 0 else "N_Y"
                elif j in [0, 2, 4]:
                    if i in [2, 4]: cat = "N_J" if j % 2 == 0 else "N_Y"
                    else: cat = "ADJ" if j % 2 == 0 else "V_J"
                else:
                    cat = "V_Y" if is_ping else "V_J"
                    
                if i in [2, 3, 4, 5] and j in [2, 4]:
                    cat = "V_J" if is_ping else "V_Y"
                
                phase_weight = {"起": 1, "承": 3, "转": 7, "合": 2}[phase]
                idx_seed = (core * 3 + phase_weight * 5 + temporal_wave * 7 + i * 3 + j * 5)
                
                # 带排重机制取词
                word = self.get_word(phase, ping_ze, cat, idx_seed, used_chars)
                
                line_wave += sum(ord(c) for c in word)
                line += word
                
            temporal_wave = mod10(temporal_wave + line_wave)
            poem.append(line)
            
        return poem, core

# ==================== 主程序 ====================
if __name__ == "__main__":
    print("=" * 60)
    print("Polaris Brain v4.3: 七律诗脑 (词库扩容与排重版)")
    print("=" * 60)
    
    brain = PolarisBrain()
    topic = input("\n请输入一个作诗的主题词 (推荐: 剑, 秋, 思): ")
    
    brain.ignite_theme(topic) 
    for _ in range(8):
        brain.step()
        
    poet = SevenRhymePoet(brain, topic)
    poem, core = poet.generate(topic)
    
    print("\n--- 脑电波拓扑数据 ---")
    print("中核状态: {} | 脑区多样性: {}".format(core, len(set(brain.neurons.values()))))
    print("----------------------\n")
    
    print("[" + topic + " 七律]")
    for i, line in enumerate(poem):
        prefix = "  "
        if i == 0: prefix = "首联: "
        elif i == 1: prefix = "      "
        elif i == 2: prefix = "颔联: "
        elif i == 3: prefix = "      "
        elif i == 4: prefix = "颈联: "
        elif i == 5: prefix = "      "
        elif i == 6: prefix = "尾联: "
        elif i == 7: prefix = "      "
        print(prefix + line)
        
    print("\n" + "=" * 60)
