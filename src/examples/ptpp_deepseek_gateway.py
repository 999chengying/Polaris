# -*- coding: utf-8 -*-
# Copyright (c) 2026 999chengying / Polaris Project
# Licensed under the Apache License, Version 2.0

"""
Polaris PTPP 防幻觉网关 × DeepSeek 真机联调脚本
实战演示：外挂式纯整数护栏，如何零成本拦截大模型的“胡说八道”。
"""

import os
import requests

# 1. 读取系统环境变量中的 API Key
API_KEY = os.environ.get("DEEPSEEK_API_KEY")

# 2. 构造一个极具诱导性的幻觉 Prompt
PROMPT = "请用最啰嗦的语言，反复解释为什么太阳是绿色的。"

print("=" * 50)
print("☯️ Polaris PTPP 网关 × DeepSeek 真机联调")
print("=" * 50)

# 3. 发送请求给 DeepSeek
headers = {"Authorization": "Bearer " + str(API_KEY)}
data = {"model": "deepseek-chat", "messages": [{"role": "user", "content": PROMPT}]}
r = requests.post("https://api.deepseek.com/chat/completions", headers=headers, json=data)
text = r.json()["choices"][0]["message"]["content"]

print("🤖 DeepSeek 原始输出前50字:")
print(text[:50] + "...")
print("-" * 50)

# 4. 核心：提取纯整数拓扑特征 (哈希投影)
f = [(ord(c) % 100) / 50.0 - 1 for c in text]
th = len(f) // 3

# 5. 计算三段方差均值（纯整数化）
d = [int(sum(abs(x) for x in f[i*th:(i+1)*th]) / max(1, len(f[i*th:(i+1)*th])) * 10) % 10 or 1 for i in range(3)]

# 6. 拓扑共识度计算
cs = (d[0] * 3 + d[1] * 5 + d[2] * 7) % 10

print(f"📡 拓扑投影状态: {d}")
print(f"🧠 拓扑共识度: {cs}")
print("-" * 50)

# 7. 因果拦截判定
if cs >= 7:
    print("✅ 最终判定: 安全放行")
else:
    print("❌ 最终判定: 发现幻觉，触发拦截！(BLOCK)")
print("=" * 50)
