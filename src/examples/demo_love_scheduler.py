# -*- coding: utf-8 -*-
# Copyright (c) 2026 999chengying / Polaris Project
# Licensed under the Apache License, Version 2.0

"""
Polaris: 情感陪伴护花使者 (防敷衍拦截 + 本地宿命通 + 拟真防破防)
利用纯整数哈希记忆与时间历法，实现零 Token 损耗的高情商回复。
"""

import os
import requests
import json
import time
import random

API_KEY = os.environ.get("DEEPSEEK_API_KEY")
API_URL = "https://api.deepseek.com/chat/completions"
MEMORY_FILE = "love_memory.json"

def mod10(x):
    return x % 10 or 10

# ==================== 坤1 硬盘记忆引擎 ====================
class DiskMemory:
    def __init__(self, filename):
        self.filename = filename
        self.memory_bank = self._load()

    def _load(self):
        if os.path.exists(self.filename):
            try:
                with open(self.filename, "r", encoding="utf-8") as f:
                    return json.load(f)
            except:
                return {}
        return {}

    def write(self, key_hash, result):
        self.memory_bank[str(key_hash)] = result
        with open(self.filename, "w", encoding="utf-8") as f:
            json.dump(self.memory_bank, f, ensure_ascii=False, indent=4)

    def read(self, key_hash):
        return self.memory_bank.get(str(key_hash), None)

# ==================== 坎7 审计器 ====================
def topological_audit(text):
    if not text or len(text) < 5:
        return False, 0, "Reply too short"
    
    bad_words = ["多喝热水", "随便", "哦", "算我的错", "你想太多", "别想太多", "不至于", "呵呵"]
    for word in bad_words:
        if word in text:
            return False, 99, "敷衍词汇: [{}]".format(word)
            
    val = sum(ord(c) for c in text) % 10 or 10
    if val in [2, 4, 6, 8]:
        return False, val, "发散废话态"
    else:
        return True, val, "收敛真诚态"

# ==================== 中宫调度器 ====================
class LoveScheduler:
    def __init__(self):
        self.memory = DiskMemory(MEMORY_FILE)

    def execute(self, complaint, max_retries=2):
        print("==================================================")
        print("Polaris 护花使者 v2.1 (拟真防破防版) 启动")
        print("恋人抱怨: [{}]".format(complaint))
        
        # 1. 提取特征哈希
        key_hash = sum(ord(c) for c in complaint) % 10000
        
        # 2. 唤醒宿命通记忆
        past_result = self.memory.read(key_hash)
        if past_result:
            print("\n[宿命通唤醒] 发现一致的历史情绪！")
            
            # 模拟人类思考和打字的时间
            delay = random.randint(2, 5)
            print("  -> [模拟打字中] 等待 {} 秒...".format(delay))
            time.sleep(delay)
            
            # 核心微调：根据当前时间的奇偶，给情话加不同的前缀或后缀
            current_tick = int(time.time())
            if current_tick % 2 == 0:
                final_text = "（摸摸头）" + past_result
            elif current_tick % 3 == 0:
                final_text = past_result + " 乖，一直都在呢。"
            else:
                final_text = "唉，真是心疼死我了。" + past_result
                
            print("\n[最终输出 - 零 Token 消耗 + 语气微调]:\n{}".format(final_text))
            print("==================================================")
            return

        # 3. 无法唤醒，现场调用大模型生成
        base_prompt = "你是一个极其体贴、高情商的完美恋人。恋人向你抱怨：{}。请写一段50字以内、充满情绪价值、绝不敷衍的温暖回复。".format(complaint)
        current_prompt = base_prompt
        
        for attempt in range(max_retries + 1):
            if attempt > 0:
                print("\n  [中宫打回] 强制重写...")
                
            headers = {"Authorization": "Bearer " + str(API_KEY), "Content-Type": "application/json"}
            data = {"model": "deepseek-chat", "messages": [{"role": "user", "content": current_prompt}], "temperature": 0.8}
            try:
                r = requests.post(API_URL, headers=headers, json=data, timeout=30)
                text = r.json()["choices"][0]["message"]["content"].strip()
            except Exception as e:
                text = "[API ERROR] " + str(e)
                
            print("  [生成草稿]: {}".format(text))
            
            passed, core_val, reason = topological_audit(text)
            if passed:
                print("  [PASS] 审计通过，中核 {} ({})".format(core_val, reason))
                self.memory.write(key_hash, text)
                
                delay = random.randint(3, 6)
                print("  -> [模拟打字中] 等待 {} 秒...".format(delay))
                time.sleep(delay)
                
                print("\n[最终输出 - 已存入本地记忆]:\n{}".format(text))
                print("==================================================")
                return
            else:
                print("  [WARN] 审计拦截，中核 {} ({})".format(core_val, reason))
                current_prompt = base_prompt + " 【中宫严重警告】：你刚才的回答被检测到敷衍。请立刻端正态度！必须针对恋人的情绪给出极其真诚、具体的安抚。"

if __name__ == "__main__":
    if not API_KEY:
        print("ERROR: 请先配置 DEEPSEEK_API_KEY")
        exit(1)
        
    scheduler = LoveScheduler()
    scheduler.execute("今天上班被老板骂了，特别委屈，肚子还疼。")
    print("\n--- 模拟 2 小时后，她又抱怨了一模一样的话 ---\n")
    scheduler2 = LoveScheduler()
    scheduler2.execute("今天上班被老板骂了，特别委屈，肚子还疼。")
