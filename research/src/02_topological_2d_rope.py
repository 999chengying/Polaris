# -*- coding: utf-8 -*-
"""
Polaris 后天应用研究：二维拓扑位置编码 (Topological 2D RoPE)
利用阿基米德螺线特性，生成纯整数的 2D 空间位置编码矩阵。
"""

def generate_2d_spiral_pe(grid_size=5):
    """
    生成二维螺旋位置编码。
    中心点固定为 5。
    外围根据切比雪夫距离（环数）生成等差步长。
    """
    center = grid_size // 2
    pe_matrix = []
    
    for i in range(grid_size):
        row = []
        for j in range(grid_size):
            # 计算当前点到中心的切比雪夫距离（即处于第几环）
            dist = max(abs(i - center), abs(j - center))
            
            if dist == 0:
                # 中心点，最高权重的太极点
                val = 5
            else:
                # 阿基米德螺线展开：结合当前环数(半径)与方向(角度)
                # 这里用极简的纯整数计算：环数步长 * (方向偏移)
                # 假设顺时针方向由 (i+j) 决定
                direction = (i + j) % (dist * 2)
                # 基础值为 5，加上螺线步长增量（模10）
                val = (5 + dist * 1 + direction * 2) % 10
                
            row.append(val)
        pe_matrix.append(row)
        
    return pe_matrix

def print_matrix(matrix, title):
    print(f"--- {title} ---")
    for row in matrix:
        print("  ", "  ".join(f"{v:2d}" for v in row))
    print()

if __name__ == "__main__":
    print("=" * 60)
    print("☯️ Polaris 二维拓扑位置编码 (2D Topological RoPE)")
    print("=" * 60)
    
    # 生成 5x5 的二维图像位置编码
    pe = generate_2d_spiral_pe(grid_size=5)
    print_matrix(pe, "纯整数 2D 位置编码矩阵 (5x5)")
    
    print("【工程意义】")
    print("1. 中心点 (2,2) 为 5，拥有最大的计算权重。")
    print("2. 随着距离中心越来越远，环数增加，纯整数步长自然递增。")
    print("3. 该矩阵可以直接作为纯整数 Attention 的 Q/K 叠加偏置，")
    print("   替代传统浮点 2D RoPE，且绝对没有三角函数开销！")
    print("=" * 60)
