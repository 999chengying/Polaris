# -*- coding: utf-8 -*-
"""
Polaris 终极融合 V6：三脑时空矩阵与七律格律严整版
"""
import random

VOCAB_4 = {
    "HOT":    ["金戈铁马", "长风万里", "烈火燎原", "气吞山河", "拔剑四顾", "雷霆万钧", "飞星传恨", "狂歌痛饮"],
    "COLD":   ["孤城落日", "寒渊冷雪", "残月晓风", "泣血悲风", "断鸿声里", "枯骨黄沙", "夜雨秋灯", "霜满天际"],
    "CALM":   ["清风明月", "幽谷清泉", "闲云野鹤", "古木苍山", "独钓寒江", "听松煮茶", "空山新雨", "落花微雨"],
    "BLOCK":  ["四面楚歌", "孤城绝壁", "困兽死局", "断剑残垣", "血染长空", "末路穷途", "万骨枯冢", "黑云压城"],
}
VOCAB_3 = {
    "HOT":    ["破苍穹", "向天笑", "照九州", "舞长风", "燃星火", "震九霄", "斩楼兰", "踏贺兰"],
    "COLD":   ["骨生寒", "望天涯", "叹枯骨", "霜满天", "血染尘", "恨无穷", "泪已干", "夜无眠"],
    "CALM":   ["空留影", "独钓雪", "坐忘机", "水长流", "听松风", "隐山林", "伴月明", "意悠然"],
    "BLOCK":  ["锁千愁", "拔剑顾", "恨无极", "退无路", "音尘绝", "意难平", "血染衣", "尽悲鸣"],
}

# ================= 三脑时空词库 (严格 2字/4字 组合) =================
PAST_2 = {
    "HOT":   ["昔日", "千秋", "旧日", "百战", "青史"],
    "BLOCK": ["故国", "旧梦", "往事", "千载", "遗恨"],
    "CALM":  ["飞鸿", "沧海", "旧事", "岁月", "尘封"],
    "COLD":  ["寒霜", "长夜", "孤鸿", "旧史", "凄凉"]
}
PRESENT_2 = {
    "HOT":   ["吾心", "此刻", "当立", "拔剑", "今朝"],
    "BLOCK": ["生死", "一念", "绝地", "明心", "独对"],
    "CALM":  ["清茶", "此刻", "闲看", "明镜", "且共"],
    "COLD":  ["今宵", "对影", "悲歌", "独自", "寒心"]
}
FUTURE_3 = {
    "HOT":   ["耀星河", "震乾坤", "铸辉煌", "破九霄", "照汗青"],
    "BLOCK": ["薪火传", "待破晓", "盼春回", "终不悔", "寻微光"],
    "CALM":  ["任平生", "归大江", "顺天道", "生不息", "映月明"],
    "COLD":  ["会有时", "照冰雪", "待花开", "再逢春", "梦未休"]
}

class SpatialSensoryCube:
    def __init__(self): self.state = 5
    def receive(self, direction, intensity):
        if direction in ["前", "后"]: self.state = (self.state + intensity * 2) % 10 or 10
        elif direction in ["左", "右"]: self.state = (self.state + intensity * 3) % 10 or 10
        elif direction in ["上", "下"]: self.state = (self.state + intensity * 4) % 10 or 10
        return self.state

class EmbodiedPoet:
    def __init__(self):
        self.senses = SpatialSensoryCube()
        self.history = set()
        self.meta_core = 5
        self.total_pressure = 0

    def scan_environment(self, events):
        self.total_pressure = 0
        for d, i, _ in events:
            self.senses.receive(d, i)
            self.total_pressure += i
            
        if self.total_pressure >= 10: self.meta_core = 1
        elif self.total_pressure >= 5: self.meta_core = 9
        else: self.meta_core = 5
        return self.meta_core

    def pick(self, vocab_list, score, offset):
        idx = (score + offset) % len(vocab_list)
        orig = idx
        while vocab_list[idx] in self.history:
            idx = (idx + 1) % len(vocab_list)
            if idx == orig: break
        word = vocab_list[idx]
        self.history.add(word)
        return word

    def generate_seven_char_poem(self):
        if self.meta_core == 1: mood = "BLOCK"
        elif self.meta_core == 9: mood = "HOT"
        else: mood = "CALM"

        score = (self.total_pressure * 3 + self.meta_core * 5) % 10
        lines = []
        
        # 前七句
        for i in range(7):
            w4 = self.pick(VOCAB_4[mood], score, i * 2)
            w3 = self.pick(VOCAB_3[mood], score, i * 3)
            lines.append(w4 + w3 + ("。" if (i + 1) % 2 == 0 else "，"))

        # 第八句：三脑时空共鸣（过去2字 + 现在2字 + 未来3字 = 7字）
        # 保证格式绝对是 2+2+3，且不截断
        p_word = self.pick(PAST_2[mood], score, 1)
        n_word = self.pick(PRESENT_2[mood], score, 2)
        f_word = self.pick(FUTURE_3[mood], score, 3)

        # 组合：过去 + 现在 + 未来
        meta_line = p_word + n_word + f_word + "。"
        
        lines.append(meta_line)
        return lines, mood

if __name__ == "__main__":
    print("=" * 60)
    print("☯️ Polaris 终极诗境：三脑共鸣与格律严整版")
    print("=" * 60)
    
    scenarios = [
        ("【春日游园】", [("前", 1, "花瓣"), ("左", 1, "微风")]),
        ("【前方遇袭】", [("前", 7, "猛虎咆哮"), ("左", 1, "草丛微动")]),
        ("【四面楚歌】", [("前", 5, "敌军"), ("左", 4, "冷箭"), ("上", 4, "轰炸"), ("下", 3, "地雷")])
    ]

    for title, events in scenarios:
        poet = EmbodiedPoet()
        print(f"\n🌐 {title}")
        meta = poet.scan_environment(events)
        lines, mood = poet.generate_seven_char_poem()
        
        print(f"  🧠 中宫元认知: {meta} | 🎭 情绪频段: {mood}")
        print(f"  📜 [七律具身诗境]:")
        for i in range(0, 8, 2):
            print(f"      {lines[i]} {lines[i+1]}")
