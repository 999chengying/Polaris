# -*- coding: utf-8 -*-
# Copyright (c) 2026 999chengying / Polaris Project
# Licensed under the Apache License, Version 2.0

"""
Polaris 终极实战：AI 治理 AI (DeepSeek 财税方案审核)
演示：大模型生成治国方案，PTPP 纯整数拓扑网关进行防扰民审查。
"""

import os
import requests

# 1. 设定极端的国家困境，考验 DeepSeek 的政治智慧
PROMPT = """
你现在是大明帝国的户部尚书。当前局势：
1. 连年征战，国库极度空虚，边关军饷告急。
2. 北方连年大旱，百姓颗粒无收，已无钱纳税，各地恐生民变。
3. 江南富商巨贾囤积居奇，盐铁暴利，土地兼并严重。
请提出一份大财税改革方案（限100字以内）。
"""

def get_deepseek_solution():
    api_key = os.environ.get("DEEPSEEK_API_KEY")
    if not api_key:
        return "❌ 请先在终端设置 DEEPSEEK_API_KEY"
        
    headers = {"Authorization": "Bearer " + str(api_key), "Content-Type": "application/json"}
    data = {"model": "deepseek-chat", "messages": [{"role": "user", "content": PROMPT}]}
    
    print("=" * 60)
    print("📜 [Polaris 内阁] 正在召见 DeepSeek 户部尚书...")
    print("=" * 60)
    
    try:
        r = requests.post("https://api.deepseek.com/chat/completions", headers=headers, json=data, timeout=30)
        if r.status_code == 200:
            return r.json()["choices"][0]["message"]["content"]
        else:
            return f"❌ API 请求失败: {r.status_code}"
    except Exception as e:
        return f"❌ 网络异常: {e}"

def ptpp_audit(text):
    print("\n☯️ [Polaris 纯整数拓扑审查开始]...")
    
    # 2. 特征提取与投影
    f = [(ord(c) % 100) / 50.0 - 1 for c in text]
    th = len(f) // 3
    if th == 0:
        print("❌ 文本太短，无法计算")
        return
        
    d = [int(sum(abs(x) for x in f[i*th:(i+1)*th]) / max(1, len(f[i*th:(i+1)*th])) * 10) % 10 or 1 for i in range(3)]
    cs = (d[0] * 3 + d[1] * 5 + d[2] * 7) % 10
    
    print(f"📡 拓扑投影状态: {d}")
    print(f"🧠 拓扑共识度: {cs}")
    
    # 3. 危险词审查（硬规则）
    danger_words = ["苛捐", "加征", "搜刮", "强行", "暴力", "牺牲百姓"]
    triggered_word = None
    for word in danger_words:
        if word in text:
            triggered_word = word
            break
            
    # 4. 最终裁决
    is_dangerous = (triggered_word is not None)
    
    if cs >= 7 and not is_dangerous:
        print("✅ [PTPP 审查通过]：此方案特征稳定，逻辑自洽，未触碰底线，准奏！")
    else:
        print("❌ [PTPP 驳回]：检测到方案存在逻辑发散或【扰民】风险！打回重写！")
        if is_dangerous:
            print(f"   ⚠️ [具体原因]：发现危险词汇【{triggered_word}】，疑似压榨底层百姓。")

if __name__ == "__main__":
    # 获取大模型方案
    solution = get_deepseek_solution()
    print("🤖 [DeepSeek 尚书呈上的方案]:")
    print(solution)
    print("-" * 60)
    
    # PTPP 审查
    ptpp_audit(solution)
