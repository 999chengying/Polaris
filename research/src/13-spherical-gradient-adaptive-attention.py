# -*- coding: utf-8 -*-
"""
Polaris 应用研究：基于球面梯度的自适应局部注意力 (SGAA)
根据 Query 距离中宫的半径，动态决定其注意力窗口的大小（纯整数计算）。
"""

def get_sphere_shell(coord):
    return sum((coord[i] - 3)**2 for i in range(3))

def generate_dynamic_mask(query_coord, all_key_coords):
    shell = get_sphere_shell(query_coord)
    
    if shell == 4: radius_limit = 3
    elif shell == 8: radius_limit = 5
    elif shell == 12: radius_limit = 9
    else: radius_limit = 1

    mask = []
    for k_coord in all_key_coords:
        dist = sum(abs(query_coord[i] - k_coord[i]) for i in range(3))
        mask.append(1 if dist <= radius_limit else 0)
            
    return shell, radius_limit, mask

if __name__ == "__main__":
    k_coords = [(3, 3, 3), (1, 3, 3), (1, 1, 3), (1, 1, 1), (5, 5, 5)]
    q_coords = [(1, 3, 3), (1, 1, 3), (1, 1, 1)]
    
    for i, q in enumerate(q_coords):
        shell, limit, mask = generate_dynamic_mask(q, k_coords)
        print(f"\n>>> 测试 Query {i+1}: 坐标 {q}")
        print(f"  [空间定位] 距离平方: {shell} (视野半径限制: {limit})")
        print(f"  [动态掩码] {mask}")
        active_count = sum(mask)
        print(f"  [计算效能] 此 Query 只需计算 {active_count} 个 Key 的 Attention")
