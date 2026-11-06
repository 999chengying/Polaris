# -*- coding: utf-8 -*-
# Copyright (c) 2026 999chengying / Polaris Project
# Licensed under the Apache License, Version 2.0

"""
Polaris Fractal Hexagram Swarm (4096 分形智能体网络)
基于“一倍法”与十二爻拓扑，实现内外卦解耦的极速寻路与协同路由。
"""

from collections import deque
from typing import Dict, List, Tuple, Optional

# 类型别名定义
# 卦象状态：(上卦数值, 下卦数值)
GuaState = Tuple[int, int]
# 超级智能体状态：(外卦, 内卦)
SuperAgentState = Tuple[GuaState, GuaState]
# 路由路径: [(中继节点状态, 触发算子名称), ...]
RoutingPath = List[Tuple[SuperAgentState, str]]

def mod10(x: int) -> int:
    """确保结果落在 1~10 的纯整数空间内"""
    return x % 10 or 10

class FractalHexagramSwarm:
    """
    4096 分形智能体路由网络。
    外卦（宏观）与内卦（微观）各自独立进行：错、综、先后天、乘2 的拓扑演化。
    """
    
    def __init__(self):
        # 单卦 180度翻转映射
        self.flip_map: Dict[int, int] = {9: 9, 1: 1, 3: 3, 7: 7, 8: 6, 6: 8, 2: 4, 4: 2}
        # 先后天映射表
        self.post_to_pre: Dict[int, int] = {1: 2, 2: 4, 3: 9, 4: 7, 6: 8, 7: 1, 8: 3, 9: 6}

    def _get_neighbors(self, current_state: SuperAgentState) -> List[Tuple[SuperAgentState, str]]:
        """
        惰性生成当前节点的合法拓扑邻居。
        """
        outer, inner = current_state
        neighbors = []

        # ================= 外卦演化（宏观维度） =================
        # 1. 外卦-错 (阴阳反转)
        cuo_o = (mod10(10 - outer[0]), mod10(10 - outer[1]))
        neighbors.append(((cuo_o, inner), "外卦-错"))
        
        # 2. 外卦-综 (180度倒转)
        zong_o = (self.flip_map[outer[1]], self.flip_map[outer[0]])
        neighbors.append(((zong_o, inner), "外卦-综"))
        
        # 3. 外卦-先后天 (维度跃迁)
        ptp_o = (self.post_to_pre.get(outer[0], outer[0]), self.post_to_pre.get(outer[1], outer[1]))
        neighbors.append(((ptp_o, inner), "外卦-先后天"))
        
        # 4. 外卦-乘2 (跨界桥)
        m2_o = (mod10(outer[0] * 2), mod10(outer[1] * 2))
        neighbors.append(((m2_o, inner), "外卦-乘2"))

        # ================= 内卦演化（微观维度） =================
        # 1. 内卦-错
        cuo_i = (mod10(10 - inner[0]), mod10(10 - inner[1]))
        neighbors.append(((outer, cuo_i), "内卦-错"))
        
        # 2. 内卦-综
        zong_i = (self.flip_map[inner[1]], self.flip_map[inner[0]])
        neighbors.append(((outer, zong_i), "内卦-综"))
        
        # 3. 内卦-先后天
        ptp_i = (self.post_to_pre.get(inner[0], inner[0]), self.post_to_pre.get(inner[1], inner[1]))
        neighbors.append(((outer, ptp_i), "内卦-先后天"))
        
        # 4. 内卦-乘2
        m2_i = (mod10(inner[0] * 2), mod10(inner[1] * 2))
        neighbors.append(((outer, m2_i), "内卦-乘2"))

        return neighbors

    def find_shortest_path(self, start: SuperAgentState, target: SuperAgentState) -> Optional[RoutingPath]:
        """
        基于广度优先搜索 (BFS) 寻找两个智能体之间的最短拓扑路由。
        """
        if start == target:
            return []

        # 队列存储：(当前节点, 已走过的路径)
        queue = deque([(start, [])])
        visited = set([start])
        
        while queue:
            current, path = queue.popleft()
            
            for neighbor, edge_type in self._get_neighbors(current):
                if neighbor == target:
                    return path + [(neighbor, edge_type)]
                
                if neighbor not in visited:
                    visited.add(neighbor)
                    queue.append((neighbor, path + [(neighbor, edge_type)]))
                    
        return None
