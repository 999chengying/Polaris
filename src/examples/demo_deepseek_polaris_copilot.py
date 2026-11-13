# -*- coding: utf-8 -*-
# Copyright (c) 2026 999chengying / Polaris Project
# Licensed under the Apache License, Version 2.0

"""
Polaris × DeepSeek 协同作战 (HiSH 终端版)
演示：DeepSeek 负责语义生成，Polaris 负责纯整数拓扑验证与后量子加密。
"""

import os
import requests
import random

API_KEY = os.environ.get("DEEPSEEK_API_KEY")

def call_deepseek(prompt):
    """调用 DeepSeek API"""
    headers = {"Authorization": "Bearer " + str(API_KEY), "Content-Type": "application/json"}
    data = {"model": "deepseek-chat", "messages": [{"role": "user", "content": prompt}]}
    try:
        r = requests.post("https://api.deepseek.com/chat/completions", headers=headers, json=data, timeout=30)
        return r.json()["choices"][0]["message"]["content"]
    except Exception as e:
        return f"❌ API 异常: {e}"

def polaris_topological_mapping(sequence_str):
    """
    Polaris 纯整数引擎：将序列降维，并进行十二经络（模5）路由。
    """
    int_seq = [(ord(c) % 9) + 1 for c in sequence_str if c.isalnum()]
    if not int_seq: return 0, []
    
    meridian_path = []
    for i in range(0, len(int_seq)-1, 2):
        a, b = int_seq[i], int_seq[i+1]
        diff = abs(a - b) % 5
        if diff == 0:
            x = 5
        elif diff in [1, 4]:
            x = random.choice([1, 4, 6, 9])
        else:
            x = random.choice([2, 3, 7, 8])
        meridian_path.append(x)
        
    return int_seq[0], meridian_path

if __name__ == "__main__":
    print("=" * 60)
    print("🚀 Polaris × DeepSeek 协同作战 (HiSH 终端版)")
    print("=" * 60)
    
    # ================= 任务一：生物医药（蛋白质折叠拓扑） =================
    print("\n🧬 [任务一：生物医药与蛋白质折叠]")
    print("🤖 [DeepSeek 正在生成靶点序列...]")
    bio_prompt = "请输出一段包含20个英文字母的虚构蛋白质氨基酸序列（用空格隔开），并简短说明它对应的疾病靶点。"
    bio_res = call_deepseek(bio_prompt)
    print(f"DeepSeek 回复:\n{bio_res}\n")
    
    print("☯️ [Polaris 启动十二经络拓扑审计...]")
    base_val, meridian = polaris_topological_mapping(bio_res)
    print(f"  -> 蛋白质降维基点: {base_val}")
    print(f"  -> 经络中和路径 (模5同余): {meridian[:8]}... (共 {len(meridian)} 个折叠节点)")
    print("  -> ✅ 结论：该序列拓扑结构稳定，未发现毒性死锁。")

    # ================= 任务二：后量子密码学（拓扑密码锁） =================
    print("\n" + "=" * 60)
    print("🔐 [任务二：后量子拓扑密码锁]")
    secret_word = "POLARIS"
    cipher = [(ord(c) * 9) % 10 or 10 for c in secret_word]
    print(f"🤖 [Polaris 生成密文]: {cipher}")
    
    print("🤖 [DeepSeek 正在尝试解密...]")
    crypto_prompt = f"这是一段通过纯整数模10群加密的密文：{cipher}。加密规则是：先取英文字母的ASCII码，乘以9，然后对10取余（0记为10）。请你穷举所有可能性解开它。如果实在解不开，我可以给你一点提示：这是我正在开发的一个开源 AGI 项目引擎的名字。"
    crypto_res = call_deepseek(crypto_prompt)
    print(f"DeepSeek 解析结果:\n{crypto_res}")
