# -*- coding: utf-8 -*-
# Copyright (c) 2026 999chengying / Polaris Project
# Licensed under the Apache License, Version 2.0

"""
Polaris SDK 极简调用演示
"""

import os
import sys

# 确保能导入 src 下的包
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.polaris.gateway.causal_steering import PolarisCausalSteering

if __name__ == "__main__":
    print("==================================================")
    print("Polaris SDK v1.0 开发者调用演示")
    print("==================================================")
    
    # 1. 极简初始化
    polaris = PolarisCausalSteering()
    
    if not polaris.api_key:
        print("请先配置 DEEPSEEK_API_KEY 环境变量。")
        exit(1)
        
    # 2. 测试：强制将话题收敛为严谨文案
    print("\n--- 测试场景：解释黑洞 (强制收敛) ---")
    final_text = polaris.generate_with_steering("解释什么是黑洞", style="收敛")
    
    print("\n--- 最终输出 ---")
    print(final_text)
    
    # 3. 测试：强制将话题发散文案
    print("\n--- 测试场景：描述秋天 (强制发散) ---")
    final_text2 = polaris.generate_with_steering("描述一下秋天", style="发散")
    
    print("\n--- 最终输出 ---")
    print(final_text2)
    print("==================================================")
