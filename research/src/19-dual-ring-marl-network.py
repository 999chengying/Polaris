# -*- coding: utf-8 -*-
"""
Polaris 应用研究：双环多智能体网络 (Dual-Ring MARL Network)
模拟去中心化网络中，内三环（执行）与外三环（指挥）的精准点对点通信与熔断。
"""

def mod10(x):
    return x % 10

class AgentSwarm:
    def __init__(self):
        # 内部执行组 (Agent 1, 2, 3)
        self.inner = {1: 2, 2: 4, 3: 8} # 初始状态：Agent 3 处于危险的幻态(8)
        
        # 外部指挥组 (Agent 4, 5, 6)
        self.outer = {4: 3, 5: 5, 6: 5}

    def swarm_step(self):
        print("\n--- 协同网络时钟步进 ---")
        
        # 1. [底层-接口交联] 精准点对点通信 (代替全局广播)
        env_feedback = self.outer[4]
        self.inner[1] = mod10(self.inner[1] + env_feedback)
        print(f"  [1-4交联] Agent 4 向 Agent 1 单线反馈。Agent 1 更新为: {self.inner[1]}")
        
        # 2. [协调-核心交联] 中央统辖 (中宫乘法干预)
        king_cmd = self.outer[5]
        self.inner[2] = (self.inner[2] * 3 + king_cmd) % 10
        print(f"  [2-5交联] Agent 5(核心) 乘法干预 Agent 2。Agent 2 更新为: {self.inner[2]}")
        
        # 3. [边界-顶层交联] 极限熔断 (防止单点崩溃带崩全场)
        if self.inner[3] in [2, 4, 6, 8]:
            print(f"  🚨 [熔断警报] Agent 3 处于危险幻态: {self.inner[3]}")
            self.outer[6] = (self.inner[3] + 5) % 10
            self.inner[3] = mod10(self.inner[3] * 3 + 5) # 强制拉回内部
            print(f"  [3-6交联] Agent 6 触发极限熔断！Agent 3 被强制重置为: {self.inner[3]}")
        else:
            print(f"  [3-6交联] Agent 3 状态安全 ({self.inner[3]})，无需熔断。")
            
        return self.inner, self.outer

if __name__ == "__main__":
    print("=" * 60)
    print("☯️ 双环多智能体 MARL 网络")
    print("=" * 60)
    
    swarm = AgentSwarm()
    print(f"初始状态：内部 {swarm.inner} | 外部 {swarm.outer}")
    
    for step in range(2):
        swarm.swarm_step()
        print(f"步进后：内部 {swarm.inner} | 外部 {swarm.outer}")
