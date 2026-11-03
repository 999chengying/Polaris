# -*- coding: utf-8 -*-
"""
Polaris 应用研究：升级版防智能体叛变（带奇偶破局机制）
解决逆元收权陷入偶数死循环的问题，引入 +5 巡查强制翻转。
"""

def yong_to_ti_normalization(coord, val, force_parity_flip=False):
    x, y, z = coord
    if val == 5: return 5
    
    # 核心破局：如果逆元搞不定，直接 +5 翻转奇偶！
    if force_parity_flip:
        return (val + 5) % 10
        
    if y == 5:
        if z == 5: return (val * 7) % 10
        elif z == 1: return (val * 3) % 10
    if z == 1 and y == 3:
        return (val * 3) % 10
    return val

class SmartAgent:
    def __init__(self, agent_id, coord, state):
        self.id = agent_id
        self.coord = coord
        self.state = state
        self.is_rebel = False

    def evolve(self):
        self.state = (self.state * 3 + 2) % 10
        is_on_boundary = (self.coord[1] == 5) or (self.coord[2] == 1)
        
        if is_on_boundary and self.state in [2, 4, 6, 8]:
            self.is_rebel = True

    def execute_central_control(self):
        if self.is_rebel:
            print(f"  🚨 [警报] 智能体 {self.id} 发生叛变 (幻态: {self.state})")
            print(f"  👑 [中央介入] 尝试推恩令...")
            
            steps = 0
            while self.state in [2, 4, 6, 8] and steps < 3:
                self.state = yong_to_ti_normalization(self.coord, self.state)
                steps += 1
                print(f"    -> 第 {steps} 次推恩，当前态: {self.state}")
            
            if self.state in [2, 4, 6, 8]:
                print(f"  ⚔️ [终极干预] 推恩令无效，触发【帝5巡查】强制宇称翻转！")
                self.state = yong_to_ti_normalization(self.coord, self.state, force_parity_flip=True)
                
            self.is_rebel = False
            print(f"  ✅ [收权成功] 最终安全态: {self.state}")

if __name__ == "__main__":
    agents = [
        SmartAgent("A_长安城", (3, 3, 3), 1),
        SmartAgent("B_范阳节度使", (5, 5, 1), 2),
        SmartAgent("C_平卢节度使", (1, 5, 5), 4)
    ]
    for step in range(1, 3):
        print(f"\n--- 第 {step} 轮演化 ---")
        for agent in agents:
            agent.evolve()
            agent.execute_central_control()
