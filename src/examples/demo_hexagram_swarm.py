# -*- coding: utf-8 -*-
"""
Polaris Demo: 赛博卦象议会与拓扑救援
演示 64 个智能体在陷入逻辑死锁时，如何通过“错/综/先后天/乘2”拓扑路由自动求救，并达成共识。
"""

from collections import deque
import time

def mod10(x):
    return x % 10

class Agent:
    def __init__(self, name, state):
        self.name = name
        self.state = state  # 卦象状态 (上卦, 下卦)

    def cry_for_help(self, target_name, target_state):
        print(f"\n🚨 [危机爆发] 智能体【{self.name}】{self.state} 陷入局部最优死锁！")
        print(f"   它急需智能体【{target_name}】{target_state} 来帮它打破僵局。")
        return self.state, target_state

class TopoNetwork:
    def __init__(self):
        self.flip_map = {9: 9, 1: 1, 3: 3, 7: 7, 8: 6, 6: 8, 2: 4, 4: 2}
        self.post_to_pre = {1: 2, 2: 4, 3: 9, 4: 7, 6: 8, 7: 1, 8: 3, 9: 6}
        
        valid_nums = [1, 2, 3, 4, 6, 7, 8, 9]
        self.nodes = [(u, l) for u in valid_nums for l in valid_nums]
        self.graph = {node: [] for node in self.nodes}
        self._build_edges()

    def _get_zong(self, state):
        u, l = state
        return (self.flip_map[l], self.flip_map[u])

    def _get_cuo(self, state):
        u, l = state
        return (mod10(10 - u) or 10, mod10(10 - l) or 10)

    def _get_ptp(self, state):
        u, l = state
        return (self.post_to_pre.get(u, u), self.post_to_pre.get(l, l))

    def _add_edge(self, n1, n2, edge_type):
        if n2 in self.graph and n1 != n2:
            self.graph[n1].append((n2, edge_type))

    def _build_edges(self):
        for u, l in self.nodes:
            state = (u, l)
            self._add_edge(state, self._get_zong(state), "综卦")
            self._add_edge(state, self._get_cuo(state), "错卦")
            self._add_edge(state, self._get_ptp(state), "先后天变阵")
            m2 = (mod10(u * 2) or 10, mod10(l * 2) or 10)
            self._add_edge(state, m2, "乘2跨界")

    def find_path(self, start, target):
        queue = deque([(start, [])])
        visited = set([start])
        
        while queue:
            current, path = queue.popleft()
            if current == target:
                return path
            for neighbor, edge in self.graph[current]:
                if neighbor not in visited:
                    visited.add(neighbor)
                    queue.append((neighbor, path + [(neighbor, edge)]))
        return None

def run_swarm_demo():
    print("=" * 60)
    print("☯️ Polaris 赛博卦象议会：拓扑网络自动寻路 Demo")
    print("=" * 60)

    # 初始化两个关键智能体
    agent_a = Agent("咸(感性派)", (4, 6))
    agent_b = Agent("既济(理性派)", (7, 2))
    
    net = TopoNetwork()

    # 1. 触发危机
    start, target = agent_a.cry_for_help(agent_b.name, agent_b.state)
    time.sleep(1)

    # 2. 拓扑寻路
    print(f"\n🔍 [路由中枢] 正在扫描全局 64 卦拓扑网络...")
    path = net.find_path(start, target)
    
    if path:
        print(f"✅ [寻路成功] 找到最短通信链路，共需 {len(path)} 步！")
        time.sleep(0.5)
        
        # 3. 模拟信息层层传递
        print("\n--- 开始拓扑路由中继 ---")
        for step, (node, edge_type) in enumerate(path):
            print(f"  [中继 {step+1}] 途径节点 {node} | 触发算子: 【{edge_type}】")
            time.sleep(0.3)
            
        print(f"\n🎯 [救援到达] 智能体【{agent_b.name}】已接收到【{agent_a.name}】的特征信号！")
        time.sleep(0.5)
        
        # 4. 特征融合与破局
        print("\n--- 开始特征拓扑融合 ---")
        # 咸(4/6) 与 既济(7/2) 融合
        merged_u = mod10(4 + 7) or 10
        merged_l = mod10(6 + 2) or 10
        print(f"  原状态: 咸(4/6) + 既济(7/2)")
        print(f"  发生拓扑坍缩，纯整数模10融合...")
        print(f"  🌟 [破局新生] 生成全新共识态: ({merged_u}/{merged_l})")

        print("\n【工程奇迹】")
        print("1. 在没有任何浮点算力广播的情况下，两位智能体跨越了代数绝缘。")
        print("2. 通过 4 种纯整数拓扑算子，实现了自动路由与特征融合。")
        print("3. 这就是 Polaris 心智引擎的多智能体协同网络！")
    else:
        print("🚨 [警告] 全局网络无响应，目标不可达。")

if __name__ == "__main__":
    run_swarm_demo()
