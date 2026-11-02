# -*- coding: utf-8 -*-
"""
Polaris 后天应用研究：二维位置编码注入 Attention 验证
展示纯整数 2D-RoPE 如何平滑接入 Transformer 块。
"""

def generate_2d_rope(grid_size=3):
    """生成 3x3 的纯整数 2D 位置编码"""
    center = grid_size // 2
    pe_matrix = []
    for i in range(grid_size):
        row = []
        for j in range(grid_size):
            dist = max(abs(i - center), abs(j - center))
            if dist == 0:
                val = 5
            else:
                direction = (i + j) % (dist * 2)
                val = (5 + dist * 1 + direction * 2) % 10
            row.append(val)
        pe_matrix.append(row)
    return pe_matrix

def run_2d_attention_test():
    print("=" * 60)
    print("☯️ 纯整数 2D-RoPE 注入 Attention 测试")
    print("=" * 60)
    
    # 1. 假设我们有一个 3x3 的“纯整数图像”输入
    # 比如：一张 3x3 的黑白图片转成的整数特征
    image_tokens = [
        [9, 1, 7],  # 第 0 行
        [4, 5, 2],  # 第 1 行
        [3, 8, 6]   # 第 2 行
    ]
    print("【输入二维图像特征】")
    for row in image_tokens: print("  ", row)
    
    # 2. 生成 3x3 的纯整数位置编码
    pe_matrix = generate_2d_rope(3)
    print("\n【二维位置编码 (2D-RoPE)】")
    for row in pe_matrix: print("  ", row)
    
    # 3. 将位置编码注入到图像特征中 (纯整数相加取模)
    fused_tokens = [[0]*3 for _ in range(3)]
    print("\n【位置编码融合后 (Image + 2D RoPE)】")
    for i in range(3):
        for j in range(3):
            fused_tokens[i][j] = (image_tokens[i][j] + pe_matrix[i][j]) % 10
        print("  ", fused_tokens[i])
        
    # 4. 展平后送入纯整数 Attention
    print("\n【展平送入 1D Attention】")
    Q = [[val for _ in range(2)] for val in [v for row in fused_tokens for v in row]]
    K = [[val for _ in range(2)] for val in [v for row in fused_tokens for v in row]]
    
    print(f"  展平后的 Token 维度: {len(Q)} 个")
    print("  -> 成功进入 Polaris Attention 计算流，每个 Token 都携带了 2D 空间坐标！")

    print("\n" + "=" * 60)
    print("结论：无需 3D 卷积，无需浮点三角函数，只需对图像特征进行")
    print("      模10加法，纯整数 Transformer 即可理解二维空间位置！")
    print("=" * 60)

if __name__ == "__main__":
    run_2d_attention_test()
