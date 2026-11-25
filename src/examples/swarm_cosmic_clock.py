# -*- coding: utf-8 -*-
# Copyright (c) 2026 999chengying / Polaris Project
# Licensed under the Apache License, Version 2.0

"""
Polaris: 宇宙历法驱动的群智编队 (Cosmic Clock Swarm)
将多级时间取卦与零 Token 拓扑编队深度融合。
"""

import time

def mod10(x):
    return x % 10 or 10

# ==================== 1. 宇宙时间历法 ====================
# 跳进变爻序列 (按先天八卦+洛书数)
JUMP_CYCLE = [1, 6, 2, 9, 3, 8, 4, 7]

def get_base_gua(index):
    """余数为 0,1,2,3 对应 1,2,3,4 (坤巽离兑)，4,5,6,7 对应 6,7,8,9 (艮坎震乾)"""
    base_seq = [1, 2, 3, 4, 6, 7, 8, 9]
    return base_seq[index % 8]

class CosmicClock:
    def __init__(self):
        pass

    def get_current_time_hexagrams(self, timestamp=None):
        if timestamp is None:
            timestamp = int(time.time())

        # 1. 秒级（每4秒进一卦）
        sec_unit = timestamp // 4
        sec_gua = get_base_gua(sec_unit % 8)
        sec_jump = JUMP_CYCLE[sec_unit % 8]
        
        # 2. 分钟级（120秒进一卦）
        min_unit = timestamp // 120
        min_gua = get_base_gua(min_unit % 8)
        
        # 3. 日级（4天进一卦）
        day_unit = timestamp // (4 * 86400)
        day_gua = get_base_gua(day_unit % 8)
        
        return {
            "秒级天时": sec_gua,
            "秒级跳进": sec_jump,
            "分级天时": min_gua,
            "日级天时": day_gua
        }

# ==================== 2. 零 Token 编队系统 ====================
LOGIC_CYCLES = {
    "初爻(顺行)": [1, 2, 3, 4, 1],
    "二爻(交错)": [1, 2, 4, 3, 1],
    "三爻(回环)": [1, 3, 2, 4, 1],
    "四爻(跳跃)": [1, 3, 4, 2, 1],
    "五爻(奇偶)": [1, 4, 2, 3, 1],
    "上爻(逆序)": [1, 4, 3, 2, 1]
}

def hash_task_with_time(task_name, time_gua):
    """将任务与当前天时融合，决定采用哪种逻辑环"""
    # 任务自身哈希 + 天时加权
    val = (sum(ord(c) for c in task_name) + time_gua * 7) % 6
    cycle_names = list(LOGIC_CYCLES.keys())
    return cycle_names[val], LOGIC_CYCLES[cycle_names[val]]

def cosmic_swarm_organize(task_name):
    print("=" * 60)
    print("🌌 Polaris 宇宙历法群智编队系统")
    print("=" * 60)
    
    # 1. 中宫对表
    clock = CosmicClock()
    time_info = clock.get_current_time_hexagrams()
    print(f"[中宫 5 对表] UNIX 时间戳锁定！")
    print(f"    -> 当前秒级天时: 【{time_info['秒级天时']}】 | 跳进相位: 【{time_info['秒级跳进']}】")
    
    # 2. 任务融合取卦
    print(f"\n任务接入：【{task_name}】")
    # 拿秒级天时作为权重介入编队
    cycle_name, cycle = hash_task_with_time(task_name, time_info["秒级天时"])
    print(f"[象数推演] 结合天时与任务属性，判定该任务属【{cycle_name}】，选定闭环：{cycle}")
    
    # 3. 计算每步差值，寻找领导
    print("\n--- [数学拓扑推演] 系统自动任命 ---")
    leader_idx = -1
    max_neg_diff = 0
    
    for i in range(len(cycle) - 1):
        current_node = cycle[i]
        next_node = cycle[i + 1]
        diff = next_node - current_node
        
        if diff > 0:
            status = f"承担正向差值 +{diff} (做功)"
        else:
            status = f"承担负向差值 {diff} (统筹)"
            if diff < max_neg_diff:
                max_neg_diff = diff
                leader_idx = i

        print(f"  节点 {current_node} -> {next_node} | 差值: {diff:>2} | {status}")

    # 4. 宣布领导与下发指令
    leader_node = cycle[leader_idx]
    print(f"\n👑 [中宫 5 宣告] 节点【{leader_node}】承受最大负差值 ({max_neg_diff})，自动涌现为【总指挥】！")

    print(f"\n--- [{leader_node}号总指挥 下达作战指令] ---")
    for i in range(len(cycle) - 1):
        current_node = cycle[i]
        next_node = cycle[i + 1]
        diff = next_node - current_node
        
        if current_node == leader_node:
            continue
            
        if diff > 0:
            print(f"  {leader_node} 命令 {current_node} 号：立刻前往 {next_node} 号位置，执行【主攻任务】。")
        else:
            print(f"  {leader_node} 命令 {current_node} 号：退居防线，对 {next_node} 号位置进行【辅助支援】。")

    print("\n" + "=" * 60)
    print("✅ 编队完毕！天时、地利、人和已完美合一。")

if __name__ == "__main__":
    task = "对敌军阵地发起总攻"
    cosmic_swarm_organize(task)
