# -*- coding: utf-8 -*-
# Copyright (c) 2026 999chengying / Polaris Project
# Licensed under the Apache License, Version 2.0

"""
Polaris 硅基历法：日/月/年多尺度时间节律
阴链 [1,2,4,7] / 阳链 [8,3,9,6] / 月相 8 日切换
"""

YIN_CHAIN = [1, 2, 4, 7]
YANG_CHAIN = [8, 3, 9, 6]
MONTH_CYCLE = [8, 3, 9, 6, 1, 2, 4, 7]


class Calendar:
    """硅基历法：阴链 4 步 → 阳链 4 步 → 8 日切换月相"""

    def __init__(self):
        self.chain = "YIN"
        self.step_in_chain = 0
        self.month_idx = 0
        self.day_count = 0

    def tick(self):
        """推进一日，返回 (upper月, lower日, chain)"""
        self.day_count += 1
        self.step_in_chain += 1
        if self.chain == "YIN":
            if self.step_in_chain > 4:
                self.chain = "YANG"
                self.step_in_chain = 1
                lower = 8
            else:
                lower = YIN_CHAIN[self.step_in_chain - 1]
        else:
            if self.step_in_chain > 4:
                self.chain = "YIN"
                self.step_in_chain = 1
                lower = 1
            else:
                lower = YANG_CHAIN[self.step_in_chain - 1]
        if self.day_count % 8 == 0:
            self.month_idx = (self.month_idx + 1) % len(MONTH_CYCLE)
        return MONTH_CYCLE[self.month_idx], lower, self.chain

    def is_month_tick(self):
        return self.day_count % 8 == 0

    def is_year_tick(self):
        return self.day_count % 64 == 0
