# -*- coding: utf-8 -*-
# Copyright (c) 2026 999chengying / Polaris Project
# Licensed under the Apache License, Version 2.0

"""
Polaris: 记忆三折叠模型 (时间 + 刺激度取卦)
根据时间衰减与刺激度，实现大脑海马体式的记忆分级。
"""

import time

def mod10(x):
    return x % 10 or 10

class MemoryCell:
    def __init__(self, text, timestamp, stimulus_score):
        self.text = text
        self.timestamp = timestamp
        self.stimulus_score = stimulus_score # 1-9
        self.state = 1 # 1:亮(活跃) 2:压缩 0:归档
        self.logic_line = ""
        self.anchors = ""

    def calc_days_old(self):
        now = time.time()
        return int((now - self.timestamp) / (86400)) # 转换为天

    def evaluate_and_fold(self):
        days = self.calc_days_old()
        print("\n--- 正在评估记忆：'{}' ---".format(self.text))
        print("  [参数] 距今时间: {} 天 | 刺激度卦象: {}".format(days, self.stimulus_score))

        # 核心折叠算法
        if days <= 1 or self.stimulus_score >= 8:
            self.state = 1
            print("  [状态 1-活跃]：近期事件或极度强刺激。原文本完整保留，随时参与对话。")
            self.logic_line = "完整上下文"
            self.anchors = self.text

        elif days <= 7 or self.stimulus_score >= 5:
            self.state = 2
            print("  [状态 2-压缩]：时间中度流逝或有一定刺激。剥离废话，仅保留逻辑线与锚点。")
            # 模拟提取
            self.logic_line = "压缩逻辑 2->4->6"
            words = self.text.split("，")
            self.anchors = words[0] + "...等核心片段"

        else:
            self.state = 0
            print("  [状态 0-深层归档]：久远且无刺激的流水账。深度压缩，仅保留极小哈希印记。")
            self.logic_line = "Hash_9981"
            self.anchors = "已归档（需特殊线索唤醒）"

if __name__ == "__main__":
    now = time.time()
    
    print("=" * 60)
    print("Polaris 记忆三折叠引擎启动")
    print("=" * 60)

    # 1. 昨天刚发生的，日常流水账
    m1 = MemoryCell("昨天中午的外卖真难吃，菜都是凉的。", timestamp=now - (1 * 86400), stimulus_score=2)
    
    # 2. 三天前发生的，极其震撼的求婚
    m2 = MemoryCell("那天在摩天轮顶端，她突然拿出了戒指求婚。", timestamp=now - (3 * 86400), stimulus_score=9)
    
    # 3. 半个月前发生的，普通的咖啡馆见面
    m3 = MemoryCell("半个月前在咖啡馆见面，那天她穿了件红裙子，外面下着小雨。", timestamp=now - (15 * 86400), stimulus_score=6)
    
    # 4. 几个月前，极其无聊的例会
    m4 = MemoryCell("三个月前的一天，老板在会议室又画了两个小时的饼。", timestamp=now - (90 * 86400), stimulus_score=1)

    # 执行折叠评估
    for m in [m1, m2, m3, m4]:
        m.evaluate_and_fold()

    print("\n" + "=" * 60)
    print("折叠完毕，当前记忆库体积已大幅缩小，但保留了核心精华！")
