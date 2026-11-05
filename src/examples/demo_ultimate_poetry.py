# -*- coding: utf-8 -*-
# Copyright (c) 2026 999chengying / Polaris Project

"""
Polaris 终极诗境引擎演示。
基于 PolarisBlock V2（稀疏注意力 + 无限记忆 + 六爻熔断）的纯整数诗境生成。
"""

import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# 假设您已经将刚才的代码存为了 ultimate_poetry_system.py
from src.polaris.nn.ultimate_poetry_system import UltimatePoetrySystem

def main():
    print("=" * 60)
    print("☯️ Polaris 终极诗境引擎 (五言六句炼丹版)")
    print("=" * 60)
    
    # 可以尝试更换 "春", "雪", "离别" 等主题
    topics = ["秋", "春", "离别"]
    
    for topic in topics:
        system = UltimatePoetrySystem(topic)
        system.run()
        print("-" * 60)

if __name__ == "__main__":
    main()
