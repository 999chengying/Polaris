# -*- coding: utf-8 -*-
"""
Polaris 应用研究：基于拓扑阶段的动态算力分配模型
通过识别隐状态所处的循环阶段，实时调节计算资源（Token）。
"""

def dynamic_compute_allocator(current_state, prev_state):
    """
    根据拓扑阶段，返回应该分配的算力比例和对应策略。
    """
    plane_x5 = {2, 3, 1, 4}
    bridge_49 = {4, 5, 9}
    plane_x1 = {9, 7, 6, 8}
    bridge_82 = {8, 5, 2}
    
    if current_state in plane_x5 and prev_state in plane_x5:
        return 0.1, "⚡ 低算力模式 (纯整数查表)"
    elif current_state in bridge_49 and prev_state in bridge_49:
        return 0.5, "🔄 过渡模式 (激活局部专家层)"
    elif current_state in plane_x1 and prev_state in plane_x1:
        return 1.0, "🧠 满算力模式 (全量浮点 Attention)"
    elif current_state in bridge_82 and prev_state in bridge_82:
        return 0.2, "💤 降维模式 (准备输出，释放缓存)"
    else:
        return -1.0, "🚨 异常状态 (强制触发 PTPP 干预)"

def run_allocator_demo():
    print("=" * 70)
    print("☯️ LLM 动态算力分配调度器 (Dynamic Compute Allocator)")
    print("=" * 70)
    
    trajectory = [2, 3, 1, 4, 5, 9, 7, 6, 8, 5, 2, 3]
    
    total_compute_without_monitor = len(trajectory) * 1.0
    total_compute_with_monitor = 0.0

    for i in range(1, len(trajectory)):
        prev_s = trajectory[i-1]
        curr_s = trajectory[i]
        
        alloc, strategy = dynamic_compute_allocator(curr_s, prev_s)
        
        if alloc > 0:
            total_compute_with_monitor += alloc
            print(f"  状态: {prev_s:>2} -> {curr_s:<2} | 分配算力: {int(alloc*100):>3}% | {strategy}")
        else:
            print(f"  状态: {prev_s:>2} -> {curr_s:<2} | 算力: 停止 | {strategy}")

    print("-" * 70)
    print(f"【静态全局注意力总算力】: {total_compute_without_monitor:.1f} 单位")
    print(f"【动态分配总算力】:     {total_compute_with_monitor:.1f} 单位")
    saved = (1 - total_compute_with_monitor / total_compute_without_monitor) * 100
    print(f"🚀 [战果] 算力节省了: {saved:.1f}% !!!")
    print("=" * 70)

if __name__ == "__main__":
    run_allocator_demo()
