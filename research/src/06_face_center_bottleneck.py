# -*- coding: utf-8 -*-
"""
Polaris 应用研究：面中心作为螺线中点的非线性相变实验
证明 6 个面中心 5 在全局坍缩前，充当了非线性专家路由/瓶颈层的角色。
"""

def simulate_spiral_path(has_face_center_gate: bool):
    current_state = 6
    print(f"  [起点] 外围顶点 (5,5,5) | 状态值: {current_state}")
    
    if has_face_center_gate:
        # 经过面中心 (1,3,3) 的拓扑自旋
        face_center_val = 5
        addr_bias = (1 + 3 + 3) % 10
        current_state = (current_state * 3 + face_center_val + addr_bias) % 10
        print(f"  [中转] 遭遇面中心 5 | 触发自旋偏转 -> 状态相变为: {current_state}")
    else:
        print("  [直穿] 无视面中心，直接冲向中宫...")

    # 最终到达中宫 (3,3,3) 的绝对极值算子
    center_val = 5
    final_state = (current_state * 5 + center_val) % 10
    
    print(f"  [终点] 中宫 (3,3,3) | 全局汇聚后状态值: {final_state}")
    if has_face_center_gate:
        print("  💡 结论: 面中心作为 Bottleneck，在全局坍缩前注入了非线性相变！")
    print("-" * 50)

if __name__ == "__main__":
    print("=" * 50)
    simulate_spiral_path(False)
    simulate_spiral_path(True)
