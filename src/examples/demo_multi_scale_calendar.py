# -*- coding: utf-8 -*-
# Copyright (c) 2026 999chengying / Polaris Project
# Licensed under the Apache License, Version 2.0

"""
Polaris 终极历法：多尺度时间节律引擎 (日/月双轮驱动)
"""

def mod10(x):
    return x % 10 or 10

class TemporalGear:
    def __init__(self):
        self.forward_map = {1:2, 2:4, 4:7, 7:1, 8:3, 3:9, 9:6, 6:8}
        self.month_cycle = [8, 3, 9, 6, 1, 2, 4, 7]
        
    def run_calendar(self, steps=64, start_lower=1, start_upper=8):
        print(f"🪐 [历法引擎启动] 初始状态: 上卦(月)={start_upper}, 下卦(日)={start_lower}")
        print("=" * 65)
        current_lower = start_lower
        current_upper = start_upper
        month_idx = self.month_cycle.index(start_upper)
        for step in range(1, steps + 1):
            current_lower = self.forward_map[current_lower]
            if step % 8 == 0:
                month_idx = (month_idx + 1) % len(self.month_cycle)
                current_upper = self.month_cycle[month_idx]
                print(f"🌕 [月相更迭] 下卦完成一个周期！上卦(月)变化为: {current_upper}")
            gua_name = f"{current_upper}/{current_lower}"
            if step <= 16 or step % 8 == 0:
                print(f"  [第 {step:02d} 日] 卦象状态: {gua_name}")
        print("=" * 65)
        print(f"🏁 [周期结束] 经过 {steps} 步，成功遍历了完整的 64 卦组合！")
        print(f"  最终状态: 上卦(月)={current_upper}, 下卦(日)={current_lower}")
        print("=" * 65)

if __name__ == "__main__":
    gear = TemporalGear()
    gear.run_calendar(steps=64)
