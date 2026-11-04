# -*- coding: utf-8 -*-
"""
Polaris 应用研究：跨层双向反馈网络 (Cross-Layer Bidirectional Feedback Protocol)
本算法受中国古代哲学的系统层级对称关系启发，构建了一种包含内外双环、跨层双向校验的纯整数拓扑网络。
"""

def mod10(x):
    return x % 10

class DualRingNetworkNode:
    def __init__(self, name, inner_nodes, outer_nodes):
        self.name = name
        # 内部层：负责底层特征、局部动作、情绪状态 (对应 1, 2, 3)
        self.inner = inner_nodes 
        # 外部层：负责全局环境、核心决策、极限防御 (对应 4, 5, 6)
        self.outer = outer_nodes

    def display(self):
        print(f"\n=== 【网络节点：{self.name}】 ===")
        print(f"  [外部层] 顶层: {self.outer[2]} | 核心层: {self.outer[1]} | 接口层: {self.outer[0]}")
        print(f"  [内部层] 边界层: {self.inner[2]} | 协调层: {self.inner[1]} | 底层: {self.inner[0]}")

    def execute_cross_layer_coupling(self):
        """
        执行对称跨层反馈（对应原卦象的 1-4, 2-5, 3-6 耦合）
        """
        print("\n>>> 启动跨层双向校验 (1-4, 2-5, 3-6)...")
        
        # 1. 底层(0) 与 接口层(3) 交联：底层动作与外部环境反馈
        feedback_4 = self.outer[0]
        self.inner[0] = mod10(self.inner[0] + feedback_4)
        print(f"  [底层反馈] 底层受到接口层刺激: 新底层值 = {self.inner[0]}")
        
        # 2. 协调层(1) 与 核心层(4) 交联：局部特征与中央决策
        # 核心层下达强指令，使用乘法算子干扰
        core_cmd = self.outer[1]
        self.inner[1] = (self.inner[1] * 3 + core_cmd) % 10 
        print(f"  [核心指令] 核心层下达指令，协调层演化: 新协调值 = {self.inner[1]}")
        
        # 3. 边界层(2) 与 顶层(5) 交联：临界危机与极限防御
        # 如果内部边界层极度发散，顶层触发强制熔断复位
        crisis_3 = self.inner[2]
        if crisis_3 in [2, 4, 6, 8]:
            self.outer[2] = (crisis_3 + 5) % 10 # 触发全局复位
            print(f"  [顶层熔断] 边界层危机({crisis_3})！顶层触发强制奇偶翻转 -> {self.outer[2]}")
        else:
            print(f"  [顶层熔断] 边界层安全({crisis_3})，无需干预。")

if __name__ == "__main__":
    print("=" * 60)
    print("☯️ 跨层双向反馈协议 (Cross-Layer Feedback)")
    print("=" * 60)
    
    node = DualRingNetworkNode(
        name="Agent_A", 
        inner_nodes=[1, 3, 8], 
        outer_nodes=[4, 5, 5]
    )
    
    node.display()
    node.execute_cross_layer_coupling()
    node.display()
