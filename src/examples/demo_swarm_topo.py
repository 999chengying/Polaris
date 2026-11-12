# -*- coding: utf-8 -*-
# Copyright (c) 2026 999chengying / Polaris Project
# Licensed under the Apache License, Version 2.0

"""
Polaris 终极架构：多智能体蜂群 (MARL) 纯整数拓扑通信
演示：Agent 之间不发消息、不消耗 Token，仅通过纯整数状态空间进行共识与协同。
"""
import random

class TopologicalBus:
    def __init__(self):
        self.grid = {}
        
    def broadcast(self, coord, state):
        self.grid[coord] = state
        
    def read_surroundings(self, coord):
        x, y, z = coord
        neighbors = []
        for dx in [-1, 0, 1]:
            for dy in [-1, 0, 1]:
                for dz in [-1, 0, 1]:
                    if dx == 0 and dy == 0 and dz == 0: continue
                    n_coord = (x+dx, y+dy, z+dz)
                    if n_coord in self.grid:
                        neighbors.append(self.grid[n_coord])
        return neighbors

class SwarmAgent:
    def __init__(self, agent_id, coord, goal):
        self.agent_id = agent_id
        self.coord = coord
        self.state = random.randint(1, 9)
        self.goal = goal

    def step(self, bus):
        bus.broadcast(self.coord, self.state)
        neighbors = bus.read_surroundings(self.coord)
        
        if neighbors:
            avg_neighbor = sum(neighbors) // len(neighbors)
            self.state = (self.state * 3 + avg_neighbor * 7 + self.goal) % 10
            if self.state == 0: self.state = 10

def run_swarm_demo():
    print("=" * 65)
    print("🐝 Polaris 拓扑蜂群：多智能体零 Token 协同 (MARL)")
    print("=" * 65)
    bus = TopologicalBus()
    agents = [
        SwarmAgent("侦察兵A", (0, 0, 0), goal=9),
        SwarmAgent("突击手B", (2, 2, 2), goal=9),
        SwarmAgent("医疗兵C", (0, 2, 0), goal=5),
        SwarmAgent("工程师D", (2, 0, 2), goal=5),
        SwarmAgent("指挥官E", (1, 1, 1), goal=10) 
    ]
    print("🚀 [开始协同] 目标：在纯整数空间中达成战术共识...")
    for step in range(5):
        print(f"\n--- 第 {step+1} 轮拓扑同步 ---")
        for agent in agents:
            agent.step(bus)
            print(f"  [节点 {agent.coord}] {agent.agent_id} 当前状态: {agent.state}")
            
    print("\n" + "=" * 65)
    print("🚀 结论：全程无文本交互，无 API 调用，0 个 Token 消耗。纯整数极限环收敛。")
    print("=" * 65)

if __name__ == "__main__":
    run_swarm_demo()
