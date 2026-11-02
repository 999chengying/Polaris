# -*- coding: utf-8 -*-
"""
Polaris 应用研究：带衰减与方向感的螺旋注意力
彻底解决纯整数注意力中由于模运算带来的特征同质化（复读机）问题。
"""

def calculate_spiral_metrics(q, k):
    """计算差值、环状距离与方向"""
    diff = q - k
    ring_diff = min(abs(diff), 10 - abs(diff))
    
    # 方向符号：如果 q >= k 为 1 (正向)，否则为 -1 (反向)
    direction = 1 if diff >= 0 else -1
    return ring_diff, direction

def spiral_decay_attention(Q, K, V):
    seq_len = len(Q)
    scores = []
    
    # 1. 计算带方向的螺旋得分
    for i in range(seq_len):
        row = []
        for j in range(seq_len):
            dist, direction = calculate_spiral_metrics(Q[i], K[j])
            if 1 <= dist <= 4:
                score = (10 - dist) * direction
            elif dist == 0:
                score = 5
            else:
                score = 0
            row.append(score)
        scores.append(row)

    # 2. 赢者通吃掩码 (只保留绝对值最大的最强匹配)
    mask = []
    for i in range(seq_len):
        max_abs = max(abs(s) for s in scores[i])
        row_mask = [1 if abs(s) == max_abs and max_abs > 0 else 0 for s in scores[i]]
        mask.append(row_mask)

    # 3. 特征聚合 (引入方向衰减，破解同质化)
    O = []
    for i in range(seq_len):
        val = 0
        for j in range(seq_len):
            if mask[i][j] == 1:
                direction = 1 if scores[i][j] > 0 else -1
                # 核心：根据方向符号对 V 进行正负翻转，加上位置偏置
                val += (V[j] * direction) + j
        O.append(val % 10)

    return O

if __name__ == "__main__":
    # 内部测试用例
    Q = [2, 7, 1, 8, 2]
    K = [8, 2, 1, 7, 4]
    V = [4, 9, 2, 1, 7]
    
    result = spiral_decay_attention(Q, K, V)
    print(f"输入 Q: {Q}")
    print(f"输入 K: {K}")
    print(f"输入 V: {V}")
    print(f"输出 O: {result}")
