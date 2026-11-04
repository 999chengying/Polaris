run_mock_benchmark.py: 用于验证纯整数算子的计算管线（零依赖）。
run_real_model_benchmark.py: 用于接入真实大模型（如 Qwen），提取隐状态并在 HaluEval 数据集上输出真实的 TPR/FPR 混淆矩阵（需安装 PyTorch）。
