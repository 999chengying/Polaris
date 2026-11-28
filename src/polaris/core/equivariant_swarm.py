# -*- coding: utf-8 -*-
# Copyright (c) 2026 999chengying / Polaris Project
# Licensed under the Apache License, Version 2.0

"""
Polaris 突破口四：群等变智能体矩阵全景版
展示变阵前后，外围六爻智能体的“换防”与物理相变。
"""

class AtomicAgent:
    def __init__(self, name, base_value):
        self.name = name
        self.base_value = base_value

class EquivariantSwarm:
    def __init__(self):
        # 建立 8 个原子智能体
        self.agents = {
            9: AtomicAgent("乾-生成器", 9), 1: AtomicAgent("坤-存储器", 1),
            8: AtomicAgent("震-触发器", 8), 2: AtomicAgent("巽-路由器", 2),
            7: AtomicAgent("坎-审计器", 7), 3: AtomicAgent("离-洞察器", 3),
            6: AtomicAgent("艮-拦截器", 6), 4: AtomicAgent("兑-序列化", 4)
        }
        
        # 初始化二组甲（乾系）矩阵
        self.grid = {
            (1,1,1): self.agents[9], (5,5,5): self.agents[1],
            (5,5,1): self.agents[6], (1,1,5): self.agents[4],
            (1,5,1): self.agents[3], (5,1,5): self.agents[7],
            (5,1,1): self.agents[2], (1,5,5): self.agents[8]
        }

    def print_matrix(self):
        """打印当前 8 个顶点的智能体布防情况"""
        print(f"  [极轴 1,1,1]: {self.grid[(1,1,1)].name} | [极轴 5,5,5]: {self.grid[(5,5,5)].name}")
        print("  --- 外围六爻 ---")
        for coord in [(5,5,1), (1,1,5), (1,5,1), (5,1,5), (5,1,1), (1,5,5)]:
            print(f"  {coord}: {self.grid[coord].name}")

    def rotate_matrix_120(self):
        """物理变阵：绕体对角线旋转 120 度"""
        print("\n⚡ [中宫变阵令] 执行 120 度拓扑旋转！")
        new_grid = {}
        for (x, y, z), agent in self.grid.items():
            new_coord = (y, z, x) # x->y, y->z, z->x
            new_grid[new_coord] = agent
        self.grid = new_grid

    def process_task(self, path_coords):
        """任务顺着指定拓扑路径游走，每次撞见不同的智能体"""
        print("\n🚀 [任务流转开始]")
        for coord in path_coords:
            agent = self.grid[coord]
            print(f"  -> 路径经过 {coord}，接待的是：【{agent.name}】", end=" ")
            
            # 根据不同智能体的功能，产生不同效果
            if "拦截器" in agent.name:
                print("🛑 阻止前进！")
                break # 被拦截器直接拦下
            elif "生成器" in agent.name:
                print("💥 生成新数据！")
            elif "审计器" in agent.name:
                print("🔍 进行数据审查...")
            else:
                print("⚙️ 正常处理流转。")

if __name__ == "__main__":
    print("=" * 60)
    print("Polaris 群等变智能体矩阵 全景演示")
    print("=" * 60)

    swarm = EquivariantSwarm()
    
    # 我们设计一条固定的流转路径 (比如沿着外围的某一圈)
    path = [(1,5,1), (5,1,1), (5,5,1), (1,1,5), (5,1,5), (1,5,5)]

    print("\n--- 变阵前：原始阵型流转 ---")
    swarm.print_matrix()
    swarm.process_task(path)

    # 执行变阵
    swarm.rotate_matrix_120()
    
    print("\n--- 变阵后：阵型大换防 ---")
    swarm.print_matrix()
    print("\n🚀 [同一条路径再次流转]")
    swarm.process_task(path)
