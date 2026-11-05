# -*- coding: utf-8 -*-
# Copyright (c) 2026 999chengying / Polaris Project

"""
Polaris 六爻情景交联与诗丹合璧演示。
"""

import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.polaris.nn.hexagram_poetry import HexagramPoetryEngine

def run_demo():
    print("=" * 60)
    print("☯️ 六爻情景交联诗境引擎 (终极版)")
    print("=" * 60)
    
    topics = ["秋", "春", "雪", "夜", "山", "江", "风", "离别", "悟道"]
    
    for t in topics:
        # 使用命题长度作为 seed 的一部分，保证每次运行结果一致
        engine = HexagramPoetryEngine(seed=len(t) * 13 + ord(t[0]))
        result = engine.generate(t)
        
        print(f"\n🎯 命题：【{result['topic']}】")
        print(f"  (起-近景微情 | 承-中景深情 | 转-远景彻悟 | 合-情景大成)")
        print("-" * 60)
        for line in result['poem']:
            print(f"    {line}")
        
        print(f"  🔥 [炼丹] 帝五凝聚状态: {result['dan_state']} | 结句: {result['meta_couplet']}")

if __name__ == "__main__":
    run_demo()
