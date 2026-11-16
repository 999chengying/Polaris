# -*- coding: utf-8 -*-
# Copyright (c) 2026 999chengying / Polaris Project
# Licensed under the Apache License, Version 2.0

"""
Polaris 第二环：后天无尽循环巡航总线
外围 9 节点闭环 [2,3,1,4,9,7,8,6,5]，10 万步无坍缩（06/07 篇验证）
"""

ENDLESS_CYCLE = [2, 3, 1, 4, 9, 7, 8, 6, 5]


class EndlessCycle:
    """无尽循环巡航器"""

    def __init__(self):
        self.pos = 0

    def tick(self):
        val = ENDLESS_CYCLE[self.pos]
        self.pos = (self.pos + 1) % len(ENDLESS_CYCLE)
        return val
