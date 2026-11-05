# -*- coding: utf-8 -*-
"""
Polaris 应用研究：基于纯整数拓扑的防拥堵 MoE 路由 (Topological Overflow MoE)
解决传统 MoE 路由的浮点开销与负载失衡（撞车）问题。
"""

def hash_project_to_coord(features):
    third = len(features) // 3
    segs = [features[:third], features[third:2*third], features[2*third:]]
    coord = []
    for seg in segs:
        mean_val = sum(seg) / len(seg)
        variance = sum((x - mean_val) ** 2 for x in seg) / len(seg)
        val = (int(variance * 100) + (1 if mean_val > 0 else 9)) % 10
        if val < 3: coord.append(1)
        elif val > 6: coord.append(5)
        else: coord.append(3)
    return tuple(coord)

EXPERT_NODES = [
    (3, 3, 3), (3, 1, 3), (3, 5, 3), (1, 3, 3), (5, 3, 3), 
    (3, 3, 1), (3, 3, 5), (3, 1, 1), (3, 5, 5), (3, 1, 5), (3, 5, 1)
]

def route_with_overflow(target_coord, expert_loads, max_capacity=2):
    if target_coord in EXPERT_NODES and expert_loads.get(target_coord, 0) < max_capacity:
        return target_coord, "直接命中"
        
    best_expert = None
    min_dist = float('inf')
    
    for expert in EXPERT_NODES:
        if expert_loads.get(expert, 0) < max_capacity:
            dist = sum(abs(target_coord[i] - expert[i]) for i in range(3))
            if dist < min_dist:
                min_dist = dist
                best_expert = expert
                
    return best_expert, f"溢出转移 (距离{min_dist})"
