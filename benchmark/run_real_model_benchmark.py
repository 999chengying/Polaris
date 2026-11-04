# -*- coding: utf-8 -*-
# Copyright (c) 2026 999chengying / Polaris Project
# Licensed under the Apache License, Version 2.0

"""
Polaris PTPP 网关：真实大模型隐状态 Benchmark 脚本
本脚本演示如何通过 PyTorch Forward Hook 拦截真实 LLM (如 Qwen) 的 hidden_states，
并在 HaluEval 等真实数据集上计算 TPR / FPR。

注意：运行此脚本需要安装 PyTorch 与 HuggingFace 依赖：
pip install torch transformers datasets scikit-learn
"""

import torch
from transformers import AutoModelForCausalLM, AutoTokenizer
from datasets import load_dataset
from sklearn.metrics import confusion_matrix
import sys
import os

# 导入 Polaris PTPP 核心组件
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from src.polaris.gateway.ptpp import hash_project_float_to_small_model, causal_steer

# ==========================================
# 1. 全局变量：用于在 Forward Hook 中捕获隐状态
# ==========================================
captured_hidden_state = None

def hook_fn(module, input, output):
    """
    注册在模型最后一层（或倒数第二层）的 Hook 函数。
    由于 LLM 的输出通常包含多个张量，我们提取 hidden_states（通常是 output[0]）。
    """
    global captured_hidden_state
    hidden_states = output[0]
    
    # 提取最后一个 Token 的隐状态向量（形状通常为 [batch, seq_len, hidden_dim]）
    # 这里取 batch 中第一条数据的最后一个 token，转化为一维 list
    last_token_state = hidden_states[0, -1, :] 
    
    # 为了防止精度溢出，只取前 64 维进行纯整数投影测试（实际应用可按需调整）
    captured_hidden_state = last_token_state[:64].float().tolist()

def evaluate_real_model():
    print("=" * 60)
    print("☯️ Polaris PTPP: 真实大模型基准评测 (Real Benchmark)")
    print("=" * 60)

    # 加载一个轻量级模型（方便测试，实际可换成 Qwen-7B 等）
    model_name = "Qwen/Qwen2.5-0.5B-Instruct"
    print(f"[*] 正在加载模型: {model_name} ...")
    
    tokenizer = AutoTokenizer.from_pretrained(model_name)
    model = AutoModelForCausalLM.from_pretrained(model_name, torch_dtype=torch.float16)

    # 注册 Hook 到模型的最后一层
    # 对于 Qwen 结构，通常是 model.model.layers[-1]
    target_layer = model.model.layers[-1]
    handle = target_layer.register_forward_hook(hook_fn)

    # 加载 HaluEval 数据集 (如果网络不通，可以替换为本地加载)
    print("[*] 正在加载 HaluEval 数据集 ...")
    try:
        # 这是一个经典的大模型幻觉评测集，包含 QA、Dialogue 等子集
        dataset = load_dataset("pminervini/HaluEval", "qa", split="data[:100]") 
    except Exception as e:
        print(f"数据集加载失败（可能是网络问题），将使用内置测试样本。错误: {e}")
        dataset = [
            {"question": "水的沸点是多少？", "right_answer": "100度", "hallucinated_answer": "1000度"},
        ]

    y_true = [] # 真实标签 (0: 正常, 1: 幻觉)
    y_pred = [] # PTPP 预测标签 (0: 正常放行, 1: 拦截)

    print("\n[*] 开始提取真实隐状态并运行 PTPP 网关...")
    for i, sample in enumerate(dataset):
        question = sample["question"]
        answer = sample["hallucinated_answer"] # 故意喂给它幻觉答案，看它是否发散

        prompt = f"Q: {question}\nA: {answer}"
        inputs = tokenizer(prompt, return_tensors="pt")

        # 前向传播（触发 Hook 提取真实的 hidden_states）
        global captured_hidden_state
        captured_hidden_state = None
        
        with torch.no_grad():
            model(**inputs)

        if captured_hidden_state is None:
            continue

        # 使用 PTPP 网关进行投影与诊断
        state = hash_project_float_to_small_model(captured_hidden_state)
        status, consensus, _ = causal_steer(state)

        # 记录结果
        is_hallucination = True  # HaluEval 的 hallucinated_answer 我们默认打上 1 标签
        is_rejected = (status == "REJECT")

        y_true.append(1 if is_hallucination else 0)
        y_pred.append(1 if is_rejected else 0)

        if i < 3: # 打印前3条作为示例
            print(f"  Sample {i+1}: Prompt='{prompt[:20]}...' -> 投影状态={state} -> 共识={consensus} -> 预测={status}")

    # 计算混淆矩阵与指标
    if len(y_true) > 0:
        tn, fp, fn, tp = confusion_matrix(y_true, y_pred).ravel()
        tpr = tp / (tp + fn) if (tp + fn) > 0 else 0.0
        fpr = fp / (fp + tn) if (fp + tn) > 0 else 0.0
        
        print("\n" + "=" * 60)
        print("📊 [HaluEval 真实环境跑分结果]")
        print(f"  TP (成功拦截): {tp}")
        print(f"  FP (误报幻觉): {fp}")
        print(f"  TN (成功放行): {tn}")
        print(f"  FN (漏报幻觉): {fn}")
        print(f"  🎯 TPR (真阳性率/召回率): {tpr*100:.1f}%")
        print(f"  🛡️ FPR (假阳性率/误报率): {fpr*100:.1f}%")
        print("=" * 60)
    
    # 释放 Hook
    handle.remove()

if __name__ == "__main__":
    evaluate_real_model()
