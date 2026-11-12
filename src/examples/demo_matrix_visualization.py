# -*- coding: utf-8 -*-
"""
Polaris 路线三：纯整数矩阵可视化演示
在终端中直接高亮打印 3x3 九宫格，展示大脑的拓扑干涉过程。
"""
import time

# 终端高亮颜色代码
RED = "\033[91m"
GREEN = "\033[92m"
YELLOW = "\033[93m"
BLUE = "\033[94m"
RESET = "\033[0m"

def print_matrix(title, active_positions):
    print(f"\n[{title}]")
    # 3x3 矩阵
    for r in range(3):
        row_str = "  "
        for c in range(3):
            # 中心点 (1,1) 记为帝5
            if r == 1 and c == 1:
                val = " 5 "
            else:
                # 根据坐标赋予 1-9 的值 (为了视觉好看)
                val = f" {r*3+c+1} "
            
            # 如果当前位置在激活列表中，高亮显示
            is_active = (r, c) in active_positions
            if is_active:
                row_str += f"[{RED}{val}{RESET}]"
            else:
                row_str += f" {val} "
        print(row_str)
    print()

def simulate_brain_visualization():
    print("=" * 60)
    print("☯️ Polaris 拓扑矩阵：脑区并发干涉可视化")
    print("=" * 60)
    
    # 假设输入了一句话，触发了前、左、右脑的联动
    print(f"\n👤 外部刺激: 【前方发现猛兽！】")
    time.sleep(0.5)
    
    # 1. 前脑激活 (0, 1)
    print_matrix("第一步：前脑(感知)激活", [(0, 1)])
    time.sleep(0.5)
    
    # 2. 左脑、右脑随之激活 (1, 0) 和 (1, 2)
    print_matrix("第二步：左脑(记忆)与右脑(推演)并发", [(0, 1), (1, 0), (1, 2)])
    time.sleep(0.5)
    
    # 3. 后脑(信仰/底线)拉满 (2, 1)
    print_matrix("第三步：后脑(底线)拉满，引发中核干涉", [(0, 1), (1, 0), (1, 2), (2, 1)])
    time.sleep(0.5)
    
    # 4. 中核帝5觉醒
    print(f"\n👑 [中核帝5觉醒]：六合数据汇聚，生成最终心智态！")
    print(f"    {GREEN}-> 状态锁定为：离火(3)，触发战斗反应！{RESET}\n")
    
if __name__ == "__main__":
    simulate_brain_visualization()
