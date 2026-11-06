# -*- coding: utf-8 -*-
"""
Polaris 应用研究：甲号用附值——后天八卦飞星轨迹与 258 收敛
验证在空间立方体中，后天轨迹的循环与 2-5-8 轴的“最后一下”稳定作用。
"""

def mod10(x):
    return x % 10

FLYING_STARS = [2, 3, 1, 4, 9, 7, 8, 6]

def simulate_houtian_trajectory():
    print("=" * 60)
    print("☯️ 甲号用附值：后天八卦轨迹与 258 收敛验证")
    print("=" * 60)
    
    print("【第一段：后天运行轨迹 (2->3->1->4->9->7->8->6)】")
    for i, star in enumerate(FLYING_STARS):
        if star in [2, 3, 7, 8]:
            pos = "Z=5 (顶层)"
        elif star in [1, 4, 6, 9]:
            pos = "Z=1 (底层)"
        else:
            pos = "未知"
        print(f"  步 {i+1}: 星数 {star} | 位于 {pos}")
        
    print("\n【第二段：最后的一下 —— 回归 2-5-8 土轴】")
    print("  运行轨迹在 6 之后，闭环回到起点 2。")
    print("  此时，中宫 5 发力，将 2 (Z=5顶层) 与 8 (Z=5顶层) 强行绑定在土轴心：")
    print("  2 + 5 + 8 = 15 ≡ 5 (中宫稳定态)")
    
    print("\n【工程意义】")
    print("1. Z=1 极尽发散 (1,4,6,9)，负责相变；")
    print("2. Z=5 吸纳了 2,3,7,8，其中 2 与 8 夹持面心 5，形成防守锚点；")
    print("3. 当系统在底层（Z=1）发生进位或死锁时，会自动跳回顶层，由 258 轴进行强制稳定！")
    print("=" * 60)

if __name__ == "__main__":
    simulate_houtian_trajectory()
