# -*- coding: utf-8 -*-
"""
Polaris 应用研究：64卦拓扑网络（终极正解版）
严格采用“180度覆卦”定义，重构综卦路由，打通全图连通性。
"""

from collections import deque

def mod10(x):
    return x % 10

class HexagramSwarm:
    def __init__(self):
        # 单卦倒置映射（八卦各自180度翻转）
        self.flip_map = {9: 9, 1: 1, 3: 3, 7: 7, 8: 6, 6: 8, 2: 4, 4: 2}
        self.post_to_pre = {1: 2, 2: 4, 3: 9, 4: 7, 6: 8, 7: 1, 8: 3, 9: 6}
        
        valid_nums = [1, 2, 3, 4, 6, 7, 8, 9]
        self.nodes = [(u, l) for u in valid_nums for l in valid_nums]
        self.graph = {node: [] for node in self.nodes}
        self._build_edges()

    def _get_zong(self, state):
        """综卦：真正的 180度倒转"""
        u, l = state
        # 上卦变成原来的下卦倒转，下卦变成原来的上卦倒转
        return (self.flip_map[l], self.flip_map[u])

    def _get_cuo(self, state):
        """错卦：阴阳反转"""
        u, l = state
        return (mod10(10 - u) or 10, mod10(10 - l) or 10)

    def _get_ptp(self, state):
        """先后天映射"""
        u, l = state
        return (self.post_to_pre.get(u, u), self.post_to_pre.get(l, l))

    def _add_edge(self, n1, n2, edge_type):
        if n2 in self.graph and n1 != n2:
            self.graph[n1].append((n2, edge_type))

    def _build_edges(self):
        for u, l in self.nodes:
            state = (u, l)
            # 1. 综卦
            self._add_edge(state, self._get_zong(state), "综卦")
            # 2. 错卦
            self._add_edge(state, self._get_cuo(state), "错卦")
            # 3. 先后天映射
            self._add_edge(state, self._get_ptp(state), "先后天")
            # 4. 乘2（跨界桥）
            m2 = (mod10(u * 2) or 10, mod10(l * 2) or 10)
            self._add_edge(state, m2, "乘2")

    def find_shortest_path(self, start, target):
        if start not in self.graph or target not in self.graph:
            return None
            
        queue = deque([(start, [])])
        visited = set([start])
        
        while queue:
            current, path = queue.popleft()
            if current == target:
                return path
            for neighbor, edge_type in self.graph[current]:
                if neighbor not in visited:
                    visited.add(neighbor)
                    queue.append((neighbor, path + [(neighbor, edge_type)]))
        return None

def run_ultimate_swarm():
    print("=" * 60)
    print("☯️ 64卦拓扑网络：全连通图终极寻路")
    print("=" * 60)
    
    swarm = HexagramSwarm()
    
    # 1. 验证综卦的绝对正确性
    print("\n>>> 验证综卦 180度倒转 法则：")
    print("  水雷屯 (8/7) 的综卦是 ->", swarm._get_zong((8,7)), "(应为7/6 山水蒙)")
    print("  泽山咸 (4/6) 的综卦是 ->", swarm._get_zong((4,6)), "(应为8/2 雷风恒)")
    print("  水火既济(7/2) 的综卦是 ->", swarm._get_zong((7,2)), "(应为4/7 火水未济)")
    
    # 2. 重新寻找咸(4,6) 到既济(7,2)的路径
    start_node = (4, 6)
    target_node = (7, 2)
    print(f"\n>>> 重新寻找路径: {start_node} -> {target_node}")
    
    path = swarm.find_shortest_path(start_node, target_node)
    if path:
        print(f"  ✅ 找到路径！共需 {len(path)} 步：")
        print(f"    起点: {start_node}")
        for step, (node, edge) in enumerate(path):
            print(f"    [第{step+1}步] --({edge})--> {node}")
    else:
        print("  🚨 依然不可达")
        
if __name__ == "__main__":
    run_ultimate_swarm()
