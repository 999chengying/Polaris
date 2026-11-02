# -*- coding: utf-8 -*-
"""
Polaris 应用研究：基于八卦轨道的 LLM 隐状态阶段监控器
通过路径特征与坐标面，实时判断模型的生成状态。
"""

def determine_llm_phase(current_state, prev_state):
    """
    根据当前状态和前一状态，判定模型处于哪个思维阶段。
    """
    # 定义平面集合与跨面桥
    plane_x5 = {2, 3, 1, 4}
    bridge_49 = {4, 5, 9}
    plane_x1 = {9, 7, 6, 8}
    bridge_82 = {8, 5, 2}
    
    if current_state in plane_x5 and prev_state in plane_x5:
        return "🟢 [阶段一] X=5 平面游走期 -> (模型正在平滑生成/发散联想)"
    elif current_state in bridge_49 and prev_state in bridge_49:
        return "🚀 [阶段二] 跨平面跃迁 -> (模型遭遇逻辑转折，开始深度推理)"
    elif current_state in plane_x1 and prev_state in plane_x1:
        return "🔵 [阶段三] X=1 平面游走期 -> (模型正在长程记忆重组/深度推演)"
    elif current_state in bridge_82 and prev_state in bridge_82:
        return "🌀 [阶段四] 面中心回落期 -> (模型完成总结，准备重启或输出)"
    else:
        return "⚠️ [异常] 脱离合法轨道！"

def run_phase_monitor():
    print("=" * 60)
    print("☯️ LLM 纯整数隐状态阶段监控")
    print("=" * 60)
    
    # 这是模型在生成一段话时的特征流轨迹（按照您的完美循环）
    # 2->3->1->4 (阶段1) | 4->5->9 (阶段2) | 9->7->6->8 (阶段3) | 8->5->2 (阶段4)
    trajectory = [2, 3, 1, 4, 5, 9, 7, 6, 8, 5, 2, 3]
    
    print(f"【输入】模型生成的隐状态流: {trajectory}\n")
    
    for i in range(1, len(trajectory)):
        prev_s = trajectory[i-1]
        curr_s = trajectory[i]
        
        phase_desc = determine_llm_phase(curr_s, prev_s)
        print(f"  状态: {prev_s:>2} -> {curr_s:<2} | {phase_desc}")

if __name__ == "__main__":
    run_phase_monitor()
