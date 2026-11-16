# -*- coding: utf-8 -*-
# Copyright (c) 2026 999chengying / Polaris Project
# Licensed under the Apache License, Version 2.0

"""
Polaris 第三环：错卦奇点防御总线
死锁判定 + 加5逃出生天（生数↔成数，见 research/28 篇）
"""


class SingularityRing:
    """错卦奇点防御：死锁检测 + 加5破局"""

    def __init__(self, history_size=6):
        self.history = []
        self.history_size = history_size

    def is_deadlock(self, state):
        """连续 3 次相同 或 A→B→A→B 震荡"""
        self.history.append(state)
        if len(self.history) > self.history_size:
            self.history.pop(0)
        if len(self.history) >= 3 and len(set(self.history[-3:])) == 1:
            return True
        if len(self.history) >= 4 \
                and self.history[-1] == self.history[-3] \
                and self.history[-2] == self.history[-4]:
            return True
        return False

    def break_deadlock(self, state):
        """
        加5逃出生天：生数(1-4)↔成数(6-9)严格对偶。
        5+5=10 为中宫内部循环（安全归宿）。
        依赖后续 defend 层算子异质性，避免对合返回。
        """
        return tuple(((x + 5) % 10) or 10 for x in state)
