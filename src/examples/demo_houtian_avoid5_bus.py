# -*- coding: utf-8 -*-
"""
Polaris 通信总线：第二环 (后天八卦极限环巡航)
展示：通过路径互换(86互换)完美避开中宫5，形成外围无死角感知扫描。
"""

class HoutianScanBus:
    def __init__(self):
        # 定义外围 8 个顶点宫的连接路径
        # 标准路径包含 [..., 8, 6, 2, ...]
        # 我们将其修改为路径互换的极限环：[..., 6, 8, 2, ...]
        self.ring_path = [1, 9, 7, 6, 8, 2, 4, 3]
        # 注意：这个序列绝对不会出现 5，因为它是外围极限环。
        
    def cruise_scan(self, start_node, steps=8):
        print("=" * 60)
        print(f"🌐 Polaris 第二环启动：从顶点[{start_node}]切入外围巡航")
        print("=" * 60)
        
        if start_node not in self.ring_path:
            print("❌ 错误：感知节点必须位于外围顶点宫（不包含中宫5）。")
            return

        current_idx = self.ring_path.index(start_node)
        visited = []
        
        for i in range(steps):
            current_node = self.ring_path[current_idx]
            visited.append(current_node)
            
            # 打印当前巡航状态
            print(f"  🔍 [感知扫描 {i+1}] 当前环绕至顶点宫: {current_node} | 状态: 正常采集")
            
            # 移动到下一个节点（形成莫比乌斯环）
            current_idx = (current_idx + 1) % len(self.ring_path)
            
            # 【核心逻辑：路径互换提示】
            # 在这里我们可以看到，当路径走到 6 时，下一个直接是 8，完美绕开了中宫5。
            if current_node == 6:
                print("     ⚠️ [触发86互换] 原路径: 6 -> (穿过中宫5) -> 8")
                print("     ⚡ [拓扑改道] 新路径: 6 -> 8 (直接跳跃，避开中宫死锁)")
                
        print("-" * 60)
        print(f"🎯 [巡航结束] 已成功遍历外围 8 个顶点宫，中宫 5 未被触发。")
        print(f"   闭环轨迹: {' -> '.join(map(str, visited))} -> (回到起点)")
        print("=" * 60)

if __name__ == "__main__":
    bus = HoutianScanBus()
    
    # 模拟一个传感器（比如左前雷达）扫描到了 8 顶点（震/雷）区域
    bus.cruise_scan(start_node=8, steps=8)
