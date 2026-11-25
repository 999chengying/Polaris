# -*- coding: utf-8 -*-
# Copyright (c) 2026 999chengying / Polaris Project
# Licensed under the Apache License, Version 2.0

"""
Polaris: 宇宙历法群智编队与理科实战引擎 (密码学算法设计)
让多智能体自动完成“架构设计 -> 漏洞审计 -> 终极缝合”的完整理科研发闭环。
"""

import os
import time
import requests

USE_REAL_API = True 
API_KEY = os.environ.get("DEEPSEEK_API_KEY")
API_URL = "https://api.deepseek.com/chat/completions"

def mod10(x):
    return x % 10 or 10

# ==================== 1. 宇宙历法引擎 ====================
JUMP_CYCLE = [1, 6, 2, 9, 3, 8, 4, 7]

def get_base_gua(index):
    base_seq = [1, 2, 3, 4, 6, 7, 8, 9]
    return base_seq[index % 8]

class CosmicClock:
    def get_time_info(self):
        timestamp = int(time.time())
        sec_unit = timestamp // 4
        return {
            "sec_gua": get_base_gua(sec_unit % 8),
            "sec_jump": JUMP_CYCLE[sec_unit % 8],
            "timestamp": timestamp
        }

# ==================== 2. 零 Token 拓扑编队 ====================
LOGIC_CYCLES = {
    "初爻(顺行)": [1, 2, 3, 4, 1],
    "二爻(交错)": [1, 2, 4, 3, 1],
    "三爻(回环)": [1, 3, 2, 4, 1],
    "四爻(跳跃)": [1, 3, 4, 2, 1],
    "五爻(奇偶)": [1, 4, 2, 3, 1],
    "上爻(逆序)": [1, 4, 3, 2, 1]
}

def hash_task_with_time(task_name, time_gua):
    val = (sum(ord(c) for c in task_name) + time_gua * 7) % 6
    cycle_names = list(LOGIC_CYCLES.keys())
    return cycle_names[val], LOGIC_CYCLES[cycle_names[val]]

# ==================== 3. 智能体与大模型接口 ====================
class SwarmAgent:
    def __init__(self, gua_num, role):
        self.gua_num = gua_num
        self.role = role 
        self.energy = 50

    def execute_task(self, task_desc, sub_task, style_prompt):
        self.energy -= 10 
        if self.role == "后勤":
            return ""
            
        if not USE_REAL_API or not API_KEY:
            return f"[模拟] {self.gua_num}号的{style_prompt}片段。"

        headers = {"Authorization": "Bearer " + str(API_KEY), "Content-Type": "application/json"}
        prompt = (
            f"你是第{self.gua_num}号研究员，当前任务是：{task_desc}。\n"
            f"你负责的具体子任务：{sub_task}\n"
            f"你的专业风格：{style_prompt}\n"
            f"请直接给出你的专业推导或漏洞分析，严禁废话，严禁Markdown标题。"
        )
        data = {"model": "deepseek-chat", "messages": [{"role": "user", "content": prompt}], "temperature": 0.7}
        
        try:
            r = requests.post(API_URL, headers=headers, json=data, timeout=30)
            return r.json()["choices"][0]["message"]["content"].strip().replace("**", "")
        except Exception as e:
            return "[API网络异常] " + str(e)

    def merge_squad_outputs(self, task_desc, outputs):
        self.energy -= 10
        if not USE_REAL_API or not API_KEY:
            return "[模拟缝合] 总指挥将以上内容完美融合。"

        merged_text = "\n\n".join([f"【第{i+1}号提交】{text}" for i, text in enumerate(outputs) if text])
        prompt = (
            f"你是本次项目总指挥。以下是你手下多位研究员针对《{task_desc}》提出的架构设计与漏洞审计报告。\n"
            f"请将这些碎片化的草稿整合、润色，输出一份极其严谨、逻辑闭环、无懈可击的最终技术白皮书草案。\n"
            f"必须解决所有人提出的漏洞，给出最终的算法公式或拓扑流程。不要废话，直接输出白皮书正文。\n\n"
            f"草稿：\n{merged_text}"
        )
        
        headers = {"Authorization": "Bearer " + str(API_KEY), "Content-Type": "application/json"}
        data = {"model": "deepseek-chat", "messages": [{"role": "user", "content": prompt}], "temperature": 0.5}
        try:
            r = requests.post(API_URL, headers=headers, json=data, timeout=40)
            return r.json()["choices"][0]["message"]["content"].strip()
        except Exception as e:
            return "[API网络异常] 拼接失败。"

# ==================== 4. 核心战役引擎 ====================
class PolarisScienceCombat:
    def __init__(self):
        self.clock = CosmicClock()
        self.sheng_agents = [SwarmAgent(i, "前线") for i in [1, 2, 3, 4]]
        self.cheng_agents = [SwarmAgent(i, "后勤") for i in [6, 7, 8, 9]]
        self.leader_num = 0

    def start_war(self, task_name):
        print("=" * 60)
        print("🔬 Polaris 宇宙历法与理科实战引擎")
        print("=" * 60)
        
        time_info = self.clock.get_time_info()
        print(f"[中宫5 对表] UNIX 时间戳: {time_info['timestamp']} | 秒级天时: 【{time_info['sec_gua']}】")
        
        cycle_name, cycle = hash_task_with_time(task_name, time_info["sec_gua"])
        print(f"任务接入：【{task_name}】 -> 判定属【{cycle_name}】，闭环：{cycle}")
        
        # 任命总指挥
        candidates = []
        max_neg_diff = 0
        for i in range(len(cycle) - 1):
            diff = cycle[i + 1] - cycle[i]
            if diff < 0:
                candidates.append((cycle[i], diff))
                if diff < max_neg_diff: max_neg_diff = diff
                
        best_candidates = [c for c in candidates if c[1] == max_neg_diff]
        if len(best_candidates) > 1:
            self.leader_num = best_candidates[time_info['sec_jump'] % len(best_candidates)][0]
        else:
            self.leader_num = best_candidates[0][0] if best_candidates else cycle[0]

        print(f"👑 [中宫 5 宣告] 节点【{self.leader_num}】为【总指挥】！")
        
        # --- 阶段一：生数部队主攻（负责架构设计） ---
        print(f"\n--- [阶段一：生数部队 架构主攻] ---")
        
        # 给生数分配不同的子任务
        sub_tasks_sheng = {
            1: "设计基于洛书矩阵与时间戳的【密钥生成规则】",
            2: "设计核心【加密函数】，充分利用模10的乘法单位群(1,3,7,9)",
            3: "设计【雪崩效应扩散层】，确保1位明文改变引发全局密文巨变",
            4: "设计整体【消息分组结构与防死锁同步机制】"
        }
        
        all_outputs = []
        for agent in self.sheng_agents:
            sub_task = sub_tasks_sheng.get(agent.gua_num, "")
            text = agent.execute_task(task_name, sub_task, "严谨、追求极简与工程可落地的密码学架构师")
            all_outputs.append(text)
            print(f"  💥 {agent.gua_num}号: {text[:60]}...")
                
        # --- 阶段二：阴阳换防 ---
        for a in self.sheng_agents: a.role = "后勤"
        for a in self.cheng_agents: a.role = "前线"
        
        # --- 阶段三：成数部队主攻（负责白帽审计与极端测试） ---
        print(f"\n--- [阶段二：成数部队 白帽审计] ---")
        
        sub_tasks_cheng = {
            6: "针对以上设计，寻找是否存在【对称死锁】或【弱密钥】漏洞",
            7: "模拟【选择明文攻击(CPA)】，看是否能通过差分分析还原密钥",
            8: "评估该算法的【算力开销】，并提出在FPGA/单片机上的硬件优化方案",
            9: "测试【极端输入】(如全0、全9、中宫死锁)，验证是否会引发系统热寂"
        }
        
        for agent in self.cheng_agents:
            sub_task = sub_tasks_cheng.get(agent.gua_num, "")
            text = agent.execute_task(task_name, sub_task, "极其刻薄、专挑毛病的白帽黑客与红队测试专家")
            all_outputs.append(text)
            print(f"  💥 {agent.gua_num}号: {text[:60]}...")

        # --- 阶段四：总指挥缝合 ---
        print(f"\n--- [阶段三：总指挥 {self.leader_num}号 终极缝合] ---")
        final_doc = self.leader_num_merge(task_name, all_outputs)
        print("\n📖 【最终输出技术白皮书草案】:")
        print(final_doc)

        print("\n" + "=" * 60)
        print(f"✅ 战役结束！总指挥 {self.leader_num}号 统御有方，理科算法研发闭环！")

    def leader_num_merge(self, task_name, outputs):
        commander = next((a for a in self.sheng_agents + self.cheng_agents if a.gua_num == self.leader_num), None)
        if commander:
            commander.role = "前线" 
            return commander.merge_squad_outputs(task_name, outputs)
        return "未找到总指挥"

if __name__ == "__main__":
    if not API_KEY:
        print("⚠️ 未检测到 DEEPSEEK_API_KEY，自动切换为模拟模式。\n")
        USE_REAL_API = False
        
    combat = PolarisScienceCombat()
    # 理科任务：设计一套基于纯整数的加密算法
    combat.start_war("设计一套基于洛书矩阵与模10群的纯整数轻量级加密算法")
