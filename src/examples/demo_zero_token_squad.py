# -*- coding: utf-8 -*-
# Copyright (c) 2026 999chengying / Polaris Project
# Licensed under the Apache License, Version 2.0

"""
Polaris: 零 Token 拓扑编队系统 (Zero-Token Squad Formation)
用纯整数差值直接推演领导者，彻底消灭多智能体间的寒暄与内耗。
"""

def mod10(x):
    return x % 10 or 10

# 预设 6 种拓扑环 (卷九逻辑)
LOGIC_CYCLES = {
    "初爻(顺行)": [1, 2, 3, 4, 1],
    "二爻(交错)": [1, 2, 4, 3, 1],
    "三爻(回环)": [1, 3, 2, 4, 1],
    "四爻(跳跃)": [1, 3, 4, 2, 1],
    "五爻(奇偶)": [1, 4, 2, 3, 1],
    "上爻(逆序)": [1, 4, 3, 2, 1]
}

def hash_task(task_name):
    """纯整数哈希取卦：决定采用哪种逻辑环"""
    val = sum(ord(c) for c in task_name) % 6
    cycle_names = list(LOGIC_CYCLES.keys())
    return cycle_names[val], LOGIC_CYCLES[cycle_names[val]]

def auto_form_squad(task_name):
    print("=" * 60)
    print("🚀 Polaris 零 Token 极速拓扑编队系统")
    print("=" * 60)
    
    # 1. 任务取卦
    cycle_name, cycle = hash_task(task_name)
    print(f"任务接入：【{task_name}】")
    print(f"[大模型哈希取卦] 判定该任务属【{cycle_name}】，选定拓扑闭环路径：{cycle}")
    
    # 2. 计算每步差值，寻找领导
    print("\n--- [数学拓扑推演] 系统自动任命 ---")
    leader_idx = -1
    max_neg_diff = 0 # 寻找最大的负差值
    
    for i in range(len(cycle) - 1):
        current_node = cycle[i]
        next_node = cycle[i + 1]
        diff = next_node - current_node
        
        if diff > 0:
            role = "冲锋/做工"
            status = f"承担正向差值 +{diff}"
        else:
            role = "统筹/回流"
            status = f"承担负向差值 {diff}"
            if diff < max_neg_diff:
                max_neg_diff = diff
                leader_idx = i

        print(f"  节点 {current_node} -> {next_node} | 差值: {diff:>2} | 职能: {role} | 状态: {status}")

    # 3. 宣布领导
    leader_node = cycle[leader_idx]
    print(f"\n👑 [中宫 5 宣告] 节点【{leader_node}】承受最大负差值 ({max_neg_diff})，负责统筹与分钱，自动涌现为【总指挥】！")

    # 4. 下发任务
    print(f"\n--- [{leader_node}号总指挥 下达作战指令] ---")
    for i in range(len(cycle) - 1):
        current_node = cycle[i]
        next_node = cycle[i + 1]
        diff = next_node - current_node
        
        if current_node == leader_node:
            continue
            
        if diff > 0:
            print(f"  {leader_node} 命令 {current_node} 号：立刻前往 {next_node} 号位置，执行【爆破/突击任务】。")
        else:
            print(f"  {leader_node} 命令 {current_node} 号：退居防线，对 {next_node} 号位置进行【火力支援】。")

    print("\n" + "=" * 60)
    print("✅ 编队完毕！未消耗任何大模型 Token，未发生任何寒暄。")

if __name__ == "__main__":
    task = "前方雷区排雷"
    auto_form_squad(task)
