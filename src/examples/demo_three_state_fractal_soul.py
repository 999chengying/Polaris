# -*- coding: utf-8 -*-
"""
Polaris 神级架构：三态全息宿命记忆库 (无限轮回修复版)
核心：用迭代代替递归，安全折叠 30 层以上，绝不爆栈。
"""

class FractalSoulMemory:
    def __init__(self, generation=1):
        self.generation = generation 
        # 3x3x3 三维矩阵，初始全为 0
        self.cube = [[[0 for _ in range(3)] for _ in range(3)] for _ in range(3)]
        
        self.active_count = 0
        self.archives = [] # 存放前世

    def light_up(self, x, y, z):
        if self.cube[x][y][z] == 0:
            self.cube[x][y][z] = 1
            self.active_count += 1
            print(f"  ✨ [记忆点亮] 在第 {self.generation} 世 坐标({x},{y},{z}) 存入印记。")
        else:
            print(f"  ⚠️ 坐标({x},{y},{z}) 已被点亮。")

        if self.active_count >= 27:
            self.fold_and_archive()

    def fold_and_archive(self):
        print(f"\n  🌀 [宿命折叠] 第 {self.generation} 世记忆已满！开始缩小三倍，打包归档...")
        
        current_life = self
        
        # 使用 while 循环安全模拟 35 层轮回
        while current_life.active_count >= 27 and current_life.generation < 35:
            next_life = FractalSoulMemory(generation=current_life.generation + 1)
            
            # 同构拷贝
            for i in range(3):
                for j in range(3):
                    for k in range(3):
                        if current_life.cube[i][j][k] == 1:
                            next_life.cube[i][j][k] = 1
                            next_life.active_count += 1
            
            # 当前层点亮(1) 变为 熄灭(2)
            for i in range(3):
                for j in range(3):
                    for k in range(3):
                        if current_life.cube[i][j][k] == 1:
                            current_life.cube[i][j][k] = 2
            
            # 将子代存入宿命仓库
            current_life.archives.append(next_life)
            print(f"  ✅ [归档完毕] 第 {current_life.generation} 世的节点已全部转为【熄灭(2)】态。")
            print(f"  🌌 [新生] 成功开启第 {next_life.generation} 世记忆空间。")
            
            # 指针移向下一世，继续检查
            current_life = next_life

    def recall_past_life(self, target_generation):
        print(f"\n  🧘 [宿命通开启] 试图回忆第 {target_generation} 世的记忆...")
        
        if target_generation == self.generation:
            print("  -> 这就是我当前的这一世。")
            return self
        
        current = self
        while current.generation < target_generation and current.archives:
            current = current.archives[0]
            
        if current.generation == target_generation:
            print(f"  ✅ [记忆唤醒成功] 找到了第 {target_generation} 世的归档矩阵！")
            points = []
            for i in range(3):
                for j in range(3):
                    for k in range(3):
                        # 无论是熄灭(2)还是点亮(1)，都代表曾经存在过
                        if current.cube[i][j][k] in [1, 2]:
                            points.append((i,j,k))
            print(f"  📜 [前世片段] 曾经存在的拓扑坐标: {points[:5]} ... (共 {len(points)} 个节点)")
            return current
        else:
            print("  ❌ 找不到对应的前世记忆，可能是转世次数不够。")
            return None

if __name__ == "__main__":
    memory = FractalSoulMemory(generation=1)
    
    print("================= 开启现世人生 ==================")
    # 填满 27 个格子，触发 35 层连锁折叠
    for i in range(3):
        for j in range(3):
            for k in range(3):
                memory.light_up(i, j, k)
                
    print("\n================= 唤醒十世之前的记忆 ==================")
    memory.recall_past_life(10)
