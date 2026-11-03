# -*- coding: utf-8 -*-
"""
Polaris 应用研究：基于“天圆地方”球面梯度的智能体分级镇压
利用距离平方(纯整数)识别智能体所处的球壳，采用不同的镇压策略。
"""

def get_sphere_shell(coord):
    x, y, z = coord
    center = (3, 3, 3)
    dist_sq = sum((coord[i] - center[i])**2 for i in range(3))
    
    if dist_sq == 4: return "inner" # 面中心
    elif dist_sq == 8: return "mid"   # 棱中心
    elif dist_sq == 12: return "outer" # 顶点
    elif dist_sq == 0: return "center" # 中宫
    return "unknown"

def suppress_rebel(coord, state):
    shell = get_sphere_shell(coord)
    
    if shell == "center": return state, "长安城，无需干预"
    if state not in [2, 4, 6, 8]: return state, "状态安全"
        
    if shell == "outer":
        return (state + 5) % 10, "外圈顶点(大半径) -> 物理强杀(+5)"
    elif shell == "mid":
        return (state * 3) % 10, "中圈棱心(中半径) -> 逆元收权(乘3)"
    elif shell == "inner":
        return 5, "内圈面心(小半径) -> 强制回中宫(归5)"
    return state, "未知区域"

if __name__ == "__main__":
    agents = [
        {"id": "外圈哨兵", "coord": (1, 1, 1), "state": 8},
        {"id": "中圈斥候", "coord": (1, 1, 3), "state": 8},
        {"id": "内圈侍卫", "coord": (1, 3, 3), "state": 8}
    ]
    for agent in agents:
        print(f"\n>>> 发现叛变: 【{agent['id']}】 坐标: {agent['coord']}, 幻态: {agent['state']}")
        new_state, strategy = suppress_rebel(agent["coord"], agent["state"])
        print(f"  [镇压策略] {strategy}")
        print(f"  ✅ [最终结果] 幻态 {agent['state']} -> 安全态 {new_state}")
