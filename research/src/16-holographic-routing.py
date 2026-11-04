# -*- coding: utf-8 -*-
"""
Polaris 应用研究：三维全息拓扑路由网络 (3D Holographic Routing)
融合：四角柱阶梯、逆元收权、阿基米德螺线、天圆地方球壳防御。
"""

def get_sphere_shell(coord):
    """判断当前坐标所处的球壳层级"""
    dist_sq = sum((coord[i] - 3)**2 for i in range(3))
    if dist_sq == 4: return "inner"
    elif dist_sq == 8: return "mid"
    elif dist_sq == 12: return "outer"
    elif dist_sq == 0: return "center"
    return "unknown"

def route_inner_pillar(state):
    """内层：四角柱平滑阶梯"""
    if state in [1, 2, 3]:
        return (state % 3) + 1, "内层: 角柱阶梯 (+1)"
    elif state in [6, 7, 8]:
        return 6 + ((state - 6 + 1) % 3), "内层: 角柱阶梯 (+1)"
    return state, "内层: 静止"

def route_mid_inverse(state):
    """中层：逆元收权"""
    if state in [2, 4, 6, 8]: # 处于危险偶数态
        return (state * 3) % 10, "中层: 逆元收权 (*3)"
    return state, "中层: 正常巡航"

def route_outer_spiral(state):
    """外层：阿基米德螺线广角探索 + 帝5镇压"""
    if state in [2, 4, 6, 8]: # 极远端的极端发散
        return (state + 5) % 10, "外层: 螺线探索中遇险 -> 帝5宇称翻转 (+5)"
    return state, "外层: 螺线广角探索"

class AgentNode:
    def __init__(self, agent_id, coord, initial_state):
        self.id = agent_id
        self.coord = coord
        self.state = initial_state
        self.shell = get_sphere_shell(coord)

    def execute_step(self):
        print(f"\n>>> 节点 {self.id} | 坐标 {self.coord} | 处于【{self.shell}】球壳")
        print(f"    [初始状态] 幻值: {self.state}")
        
        if self.shell == "inner":
            new_state, strategy = route_inner_pillar(self.state)
        elif self.shell == "mid":
            new_state, strategy = route_mid_inverse(self.state)
        elif self.shell == "outer":
            new_state, strategy = route_outer_spiral(self.state)
        else:
            new_state, strategy = self.state, "中宫: 绝对稳态"
            
        print(f"    [路由执行] {strategy}")
        print(f"    ✅ [演化结果] {self.state} -> {new_state}")
        self.state = new_state

if __name__ == "__main__":
    print("=" * 60)
    print("☯️ 终极形态：三维全息拓扑路由网络")
    print("=" * 60)
    
    agents = [
        AgentNode("内层巡逻兵", (1, 3, 3), 1), 
        AgentNode("中层斥候", (1, 1, 3), 8),   
        AgentNode("外层探险家", (1, 1, 1), 8)  
    ]
    
    for agent in agents:
        agent.execute_step()
