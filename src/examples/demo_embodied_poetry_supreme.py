# -*- coding: utf-8 -*-
# Copyright (c) 2026 999chengying / Polaris Project
# Licensed under the Apache License, Version 2.0

"""
Polaris 终极融合：六合空间感知与具身诗境引擎 (七律·元认知升维版)
展示：空间多模态刺激 -> 中宫压力计算 -> 情绪频段生成 -> 元认知顿悟升维
"""

VOCAB_4 = {
    "HOT":    ["金戈铁马", "长风万里", "烈火燎原", "气吞山河", "拔剑四顾", "雷霆万钧", "飞星传恨", "狂歌痛饮"],
    "COLD":   ["孤城落日", "寒渊冷雪", "残月晓风", "泣血悲风", "断鸿声里", "枯骨黄沙", "夜雨秋灯", "霜满天际"],
    "CALM":   ["清风明月", "幽谷清泉", "闲云野鹤", "古木苍山", "独钓寒江", "听松煮茶", "空山新雨", "落花微雨"],
    "BLOCK":  ["四面楚歌", "孤城绝壁", "困兽死局", "断剑残垣", "血染长空", "末路穷途", "万骨枯冢", "黑云压城"],
    "FLUID":  ["游龙惊凤", "缥缈孤鸿", "一叶扁舟", "浮萍无痕", "云影天光", "随风起舞", "流水落花", "江海余生"]
}

VOCAB_3 = {
    "HOT":    ["破苍穹", "向天笑", "照九州", "舞长风", "燃星火", "震九霄", "斩楼兰", "踏贺兰"],
    "COLD":   ["骨生寒", "望天涯", "叹枯骨", "霜满天", "血染尘", "恨无穷", "泪已干", "夜无眠"],
    "CALM":   ["空留影", "独钓雪", "坐忘机", "水长流", "听松风", "隐山林", "伴月明", "意悠然"],
    "BLOCK":  ["锁千愁", "拔剑顾", "恨无极", "退无路", "音尘绝", "意难平", "血染衣", "尽悲鸣"],
    "FLUID":  ["任平生", "随风舞", "过无痕", "渺无声", "天地宽", "一叶舟", "江海寄", "散如烟"]
}

# 按情绪分类的元认知（META）词库，用于最后一句的觉醒升维
META_VOCAB = {
    "HOT": {
        "4": ["回首红尘", "大梦初醒", "放下屠刀", "立地成佛"],
        "3": ["皆如幻", "震九霄", "笑苍天", "入涅槃"]
    },
    "CALM": {
        "4": ["万物归虚", "清风明月", "万法归一", "菩提本无"],
        "3": ["了无痕", "照禅心", "水长流", "本无尘"]
    },
    "BLOCK": {
        "4": ["一念空明", "诸相非相", "万骨枯冢", "血染长空"],
        "3": ["照大千", "尽释然", "皆如幻", "证真如"]
    },
    "COLD": {
        "4": ["镜花水月", "尘归尘土", "孤鸿影灭", "大梦千秋"],
        "3": ["一场空", "尽随风", "意如如", "叹苍茫"]
    },
    "FLUID": {
        "4": ["云在青天", "水在瓶中", "随波逐流", "天地同游"],
        "3": ["任平生", "尽逍遥", "意如风", "散如烟"]
    }
}

class SpatialSensoryCube:
    def __init__(self):
        self.state = 5

    def receive_spatial_stimulus(self, direction, intensity):
        if direction in ["前", "后"]: 
            self.state = (self.state + intensity * 2) % 10 or 10
        elif direction in ["左", "右"]: 
            self.state = (self.state + intensity * 3) % 10 or 10
        elif direction in ["上", "下"]: 
            self.state = (self.state + intensity * 4) % 10 or 10
        return self.state

class EmbodiedPoet:
    def __init__(self):
        self.senses = SpatialSensoryCube()
        self.history = set()
        self.meta_core = 5
        self.total_pressure = 0

    def scan_environment(self, events):
        self.total_pressure = 0
        for direction, intensity, desc in events:
            self.senses.receive_spatial_stimulus(direction, intensity)
            self.total_pressure += intensity
            
        if self.total_pressure >= 10: 
            self.meta_core = 1
        elif self.total_pressure >= 5: 
            self.meta_core = 9
        else: 
            self.meta_core = 5
        return self.meta_core

    def pick_word(self, vocab, score, offset):
        idx = (score + offset) % len(vocab)
        orig = idx
        while vocab[idx] in self.history:
            idx = (idx + 1) % len(vocab) 
            if idx == orig: break
        word = vocab[idx]
        self.history.add(word)
        return word

    def generate_seven_char_poem(self):
        if self.meta_core == 1: mood = "BLOCK"
        elif self.meta_core == 9: mood = "HOT"
        else: mood = "CALM"

        score = (self.total_pressure * 3 + self.meta_core * 5) % 10
        lines = []
        
        for i in range(8):
            if i == 7:
                # 【第八句强制升维】：调用当前情绪专属的元认知词库，实现大圆满顿悟
                w4 = self.pick_word(META_VOCAB[mood]["4"], score, i * 2)
                w3 = self.pick_word(META_VOCAB[mood]["3"], score, i * 3)
            else:
                # 前七句：情绪铺陈
                w4 = self.pick_word(VOCAB_4[mood], score, i * 2)
                w3 = self.pick_word(VOCAB_3[mood], score, i * 3)
            
            punctuation = "。" if (i + 1) % 2 == 0 else "，"
            lines.append(w4 + w3 + punctuation)
            
        return lines, mood

if __name__ == "__main__":
    print("=" * 60)
    print("☯️ Polaris 具身诗境引擎：七律·分类升维版")
    print("=" * 60)
    
    scenarios = [
        ("【春日游园】", [("前", 1, "花瓣"), ("左", 1, "微风")]),
        ("【前方遇袭】", [("前", 7, "猛虎咆哮"), ("左", 1, "草丛微动")]),
        ("【四面楚歌】", [("前", 5, "敌军"), ("左", 4, "冷箭"), ("上", 4, "轰炸"), ("下", 3, "地雷")])
    ]

    for title, events in scenarios:
        poet = EmbodiedPoet()
        print(f"\n🌐 {title}")
        
        for d, i, desc in events:
            print(f"  ⚠️ 方位[{d}] 刺激: {desc} (强度 {i})")
        
        meta = poet.scan_environment(events)
        lines, mood = poet.generate_seven_char_poem()
        
        print(f"  🧠 中宫元认知: {meta} | 🎭 情绪频段: {mood}")
        print(f"  📜 [七律具身诗境]:")
        for i in range(0, 8, 2):
            print(f"      {lines[i]} {lines[i+1]}")
