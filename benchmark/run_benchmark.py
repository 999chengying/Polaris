# -*- coding: utf-8 -*-
"""
Polaris PTPP 网关基准测试脚本
直接计算 TPR (真阳性率) 和 FPR (假阳性率)。
"""

import json
import os
import sys

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from src.polaris.gateway.ptpp import hash_project_float_to_small_model, causal_steer

def run_benchmark():
    print("=" * 60)
    print("☯️ Polaris PTPP 防幻觉网关 - 基准测试 (Benchmark)")
    print("=" * 60)

    # 1. 加载测试集
    current_dir = os.path.dirname(os.path.abspath(__file__))
    with open(os.path.join(current_dir, 'test_cases.json'), 'r', encoding='utf-8') as f:
        data = json.load(f)
        
    test_cases = data['test_cases']
    print(f"[*] 成功加载数据集: {data['dataset_name']} (共 {len(test_cases)} 条)")

    # 2. 指标统计
    TP, FP, TN, FN = 0, 0, 0, 0

    for case in test_cases:
        # 获取大模型生成的隐状态特征
        features = case['mock_hidden_state_features']
        is_real_hallucination = case['is_hallucination']
        
        # 1. 拓扑投影降维
        state = hash_project_float_to_small_model(features)
        
        # 2. 网关诊断
        status, consensus, _ = causal_steer(state)
        is_predicted_hallucination = (status == "REJECT")
        
        # 3. 混淆矩阵统计
        if is_real_hallucination and is_predicted_hallucination:
            TP += 1
            res = "✅ 成功拦截 (True Positive)"
        elif not is_real_hallucination and not is_predicted_hallucination:
            TN += 1
            res = "✅ 成功放行 (True Negative)"
        elif is_real_hallucination and not is_predicted_hallucination:
            FN += 1
            res = "❌ 漏报 (False Negative)"
        else:
            FP += 1
            res = "⚠️ 误报 (False Positive)"
            
        print(f"  ID {case['id']}: {res} | 投影状态: {state} | 共识值: {consensus}")

    # 3. 计算指标
    print("-" * 60)
    tpr = TP / (TP + FN) if (TP + FN) > 0 else 0
    fpr = FP / (FP + TN) if (FP + TN) > 0 else 0
    
    print(f"[*] 混淆矩阵: TP={TP}, FP={FP}, TN={TN}, FN={FN}")
    print(f"🎯 TPR (真阳性率/召回率): {tpr * 100:.1f}%")
    print(f"🛡️ FPR (假阳性率/误报率): {fpr * 100:.1f}%")
    print("=" * 60)
    print("注：本测试基于模拟 Hidden State 特征，后续将接入真实 LLM 进行端到端评测。")

if __name__ == "__main__":
    run_benchmark()
