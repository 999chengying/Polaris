# -*- coding: utf-8 -*-
# Copyright (c) 2026 999chengying / Polaris Project
# Licensed under the Apache License, Version 2.0

"""
Polaris: 智能上下文记忆过滤器 (边缘计算记忆压缩与云端逆推)
本地存储全量流水账，拓扑引擎过滤废话提取锚点，云端轻量级回放。
"""

import os
import requests

API_KEY = os.environ.get("DEEPSEEK_API_KEY")
API_URL = "https://api.deepseek.com/chat/completions"

def mod10(x):
    return x % 10 or 10

# ==================== 本地 Polaris 记忆引擎 ====================
class LocalBrain:
    def __init__(self):
        self.raw_memory = [] # 存储全量废话，存在本地

    def remember(self, text):
        """将用户的每句话全量存入本地"""
        self.raw_memory.append(text)
        print("[Local] 已保存至本地库 (当前记忆深度: {} 句)".format(len(self.raw_memory)))

    def extract_logic(self):
        """
        核心功能：从海量废话中提取逻辑线与核心锚点
        采用简易的特征词抓取 + 哈希链路模拟真实拓扑引擎
        """
        print("\n[Local] 正在执行拓扑过滤，剔除废话，提取逻辑线...")
        
        # 1. 提取核心锚点 (抓取包含特定情感词/名词的句子)
        keywords = ["咖啡", "下雨", "红裙", "梦想", "告别", "冷", "累", "开心"]
        anchors = []
        for text in self.raw_memory:
            if any(kw in text for kw in keywords):
                anchors.append(text)
        
        # 2. 生成拓扑逻辑线
        raw_concat = "".join(self.raw_memory)
        logic_hash = sum(ord(c) for c in raw_concat) % 9
        logic_path = []
        curr = logic_hash
        for _ in range(4):
            curr = mod10(curr + 2)
            logic_path.append(curr)
            
        logic_str = " -> ".join(str(x) for x in logic_path)
        
        # 3. 打包返回压缩后的 Context
        compressed_context = {
            "logic_line": logic_str,
            "anchors": anchors
        }
        return compressed_context

# ==================== 云端大脑 (调用 API) ====================
def cloud_speak(compressed_context, user_question):
    prompt = (
        "你是一个能够根据极简逻辑线回放记忆的 AI。\n"
        "当前记忆逻辑线：{}\n".format(compressed_context['logic_line']) +
        "核心记忆锚点：{}\n\n".format(compressed_context['anchors']) +
        "用户现在问你：{}\n".format(user_question) +
        "请结合锚点和逻辑线，用极其简短、自然、像老朋友一样的方式回答。"
    )
    
    print("\n[Cloud] 实际发送给大模型的 Token 估算: 约 {} 字 (极低消耗)".format(len(prompt)))
    print("[Cloud] 正在生成回答...")
    
    headers = {"Authorization": "Bearer " + str(API_KEY), "Content-Type": "application/json"}
    data = {"model": "deepseek-chat", "messages": [{"role": "user", "content": prompt}], "temperature": 0.7}
    try:
        r = requests.post(API_URL, headers=headers, json=data, timeout=30)
        return r.json()["choices"][0]["message"]["content"].strip()
    except Exception as e:
        return "[API ERROR] " + str(e)

# ==================== 模拟实战 ====================
if __name__ == "__main__":
    if not API_KEY:
        print("ERROR: 请先配置 DEEPSEEK_API_KEY")
        exit(1)
        
    brain = LocalBrain()
    
    # 模拟用户过去几天的海量对话流水账
    print("=== 模拟用户过去几天的海量对话流水账 ===")
    brain.remember("今天早上吃了煎饼果子，味道一般。")
    brain.remember("上班路上有点堵车，烦死了。")
    brain.remember("还记得那天我们在咖啡馆见面，她穿着一件红色的裙子。")
    brain.remember("中午的外卖真难吃。")
    brain.remember("那天窗外下着淅淅沥沥的小雨，我们聊了很久关于未来的梦想。")
    brain.remember("下午开会老板又在画饼，好累。")
    brain.remember("不过最后在路灯下告别的时候，心里觉得很温暖。")
    brain.remember("明天晚上去吃火锅吧。")
    
    # 本地引擎压缩过滤
    compressed = brain.extract_logic()
    print("\n[Local] 压缩完成！即将发送给云端的只有这些精华：")
    print("  - 逻辑线: {}".format(compressed['logic_line']))
    print("  - 锚点: {} 句核心记忆".format(len(compressed['anchors'])))
    
    # 用户提问
    question = "你还记得我们那天在咖啡馆见面的事情吗？"
    print("\n[User] 提问：{}".format(question))
    
    # 云端基于极简信息回放
    answer = cloud_speak(compressed, question)
    print("\n[AI 回答]:\n{}".format(answer))
