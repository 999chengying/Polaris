# -*- coding: utf-8 -*-
"""
Polaris 后天应用研究：基于阿基米德螺线的纯整数路径规划
实现无死角的全图覆盖，适用于具身智能的盲扫与探索。
"""

def spiral_search_route(size=5):
    grid = [[0 for _ in range(size)] for _ in range(size)]
    center = size // 2
    r, c = center, center
    grid[r][c] = 1 
    
    directions = [(0, 1), (1, 0), (0, -1), (-1, 0)]
    dir_idx = 0
    step_length = 1
    current_step = 2
    
    while current_step <= size * size:
        for _ in range(2):
            dr, dc = directions[dir_idx % 4]
            for _ in range(step_length):
                r += dr
                c += dc
                if 0 <= r < size and 0 <= c < size:
                    grid[r][c] = current_step
                    current_step += 1
            dir_idx += 1 
        step_length += 1 
        if current_step > size * size:
            break
    return grid

if __name__ == "__main__":
    # 测试运行
    route_grid = spiral_search_route(5)
    for row in route_grid:
        print("  ".join(f"{v:2d}" for v in row))
