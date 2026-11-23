# -*- coding: utf-8 -*-
# Copyright (c) 2026 999chengying / Polaris Project
# Licensed under the Apache License, Version 2.0

"""
Polaris Swarm Cube: 真机协同作战引擎 (系统级互搏版)
修复换防Bug，加入后勤部队的拓扑诊断。
"""

import os
import time
import requests

API_KEY = os.environ.get("DEEPSEEK_API_KEY")
API_URL = "https://api.deepseek.com/chat/completions"

def call_deepseek(prompt, system_msg="你是一个富有创造力的作家。"):
    headers = {"Authorization": "Bearer " + str(API_KEY), "Content-Type": "application/json"}
    messages = [{"role": "system", "content": system_msg}, {"role": "user", "content": prompt}]
    data = {"model": "deepseek-chat", "messages": messages, "temperature": 0.8}
    try:
        r = requests.post(API_URL, headers=headers, json=data, timeout=30)
        return r.json()["choices"][0]["message"]["content"].strip()
    except Exception as e:
        return "[API失败] " + str(e)

def mock_diagnose(text):
    """模拟纯整数拓扑诊断 (实际应调用之前的 18-bit 引擎)"""
    # 这里用字数模拟极性判断，仅作演示
    if len(text) % 2 == 0:
        return "偶数态 (过于发散，情感充沛)"
    else:
        return "奇数态 (过于收敛，逻辑严密)"

class CubeAgent:
    def __init__(self, gua_num):
        self.gua_num = gua_num
        self.energy = 50
        self.role = ""

    def execute_task(self, task_desc, system_role):
        self.energy -= 10 
        # 核心修复：每次执行时，直接传入角色，不再看死板的 self.role
        prompt = f"你是第{self.gua_num}号主攻手。请针对任务《{task_desc}》，写出两句核心内容，风格要符合[{system_role}]。"
        return call_deepseek(prompt, f"你是一个{system_role}的作家。")

class PolarisSystemCube:
    def __init__(self):
        # 生数部队 (主攻)
        self.sheng = [CubeAgent(1), CubeAgent(2)]
        # 成数部队 (后备)
        self.cheng = [CubeAgent(6), CubeAgent(7)]

    def run_operation(self, task_name):
        print("=" * 60)
        print(f"🚀 系统作战启动。任务：【{task_name}】")
        print("=" * 60)
        
        print("\n[中宫5] 发令对表！全军出击！")
        
        # --- 阶段一：生数主攻 ---
        print("\n--- [阶段一：生数主攻 (1,2)，成数(6,7)监军] ---")
        sheng_outputs = []
        for agent in self.sheng:
            text = agent.execute_task(task_name, "刚健有力的武侠风")
            sheng_outputs.append(text)
            print(f"  💥 [主攻手 {agent.gua_num} 输出]: {text}")
            
        print("\n  🛡️ [后勤 6,7] 正在对生数的草稿进行卦象体检...")
        for text in sheng_outputs:
            diagnosis = mock_diagnose(text)
            print(f"    -> 诊断结果: {diagnosis}")

        # --- 换防 ---
        print("\n[中宫5巡视] 前线能量下降，执行错卦换防！成数顶上，生数退居二线监军。")
        
        # --- 阶段二：成数主攻 ---
        print("\n--- [阶段二：成数主攻 (6,7)，生数(1,2)监军] ---")
        cheng_outputs = []
        for agent in self.cheng:
            # 这次传入“阴柔、细腻”的风格，与生数形成反差
            text = agent.execute_task(task_name, "阴柔细腻、悬疑反转的武侠风")
            cheng_outputs.append(text)
            print(f"  💥 [主攻手 {agent.gua_num} 输出]: {text}")
            
        print("\n  🛡️ [后勤 1,2] 正在对成数的草稿进行卦象体检...")
        for text in cheng_outputs:
            diagnosis = mock_diagnose(text)
            print(f"    -> 诊断结果: {diagnosis}")

        print("\n" + "=" * 60)
        print("✅ 战役结束。生数与成数不仅完成了轮换，还互相进行了拓扑评审！")

if __name__ == "__main__":
    if not API_KEY:
        print("ERROR: 请先配置 DEEPSEEK_API_KEY。")
        exit(1)
        
    cube = PolarisSystemCube()
    cube.run_operation("构思一段关于大漠孤烟的武侠故事开头")
