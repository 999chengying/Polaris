# -*- coding: utf-8 -*-
"""
Polaris 应用研究：分形指令记忆引擎 (时间与空间解耦修复版)
"""

class FractalInstructionMemory:
    def __init__(self):
        # 修复：将 8 种操作符映射到 XY 平面的 8 个外围顶点
        # 不再包含 Z 坐标，Z 轴全部留给“时间步”使用
        self.op_to_xy = {
            "错卦": (0, 0),
            "综卦": (1, 0),
            "先后天": (2, 0),
            "全乘3": (0, 1),
            "全加5": (2, 1),
            "内卦乘3": (0, 2),
            "外卦乘3": (1, 2),
            "全加1": (2, 2)
        }
        self.xy_to_op = {v: k for k, v in self.op_to_xy.items()}

    def encode(self, base_state, path):
        """将基态和路径指令编码，存入分形立方体。"""
        # 3x3x3 的 27 宫格
        cube = [[[0 for _ in range(3)] for _ in range(3)] for _ in range(3)]
        
        # 1. 存储基态 (永远放在中心点)
        cube[1][1][1] = base_state
        
        # 2. 存储指令路径 (Z 轴 0,1,2 代表 3 个时间步)
        for step, op_name in enumerate(path):
            if step > 2:
                print("⚠️ 超出3步，物理内存已满！")
                break
            
            # 获取指令在 XY 平面的坐标
            x, y = self.op_to_xy[op_name]
            
            # 将该指令刻在第 step 层的 (x, y) 坐标上
            cube[step][y][x] = 1  
            
        return cube

    def decode(self, cube):
        """从分形立方体中读取出基态与指令路径。"""
        base_state = cube[1][1][1]
        recovered_path = []
        
        # 读取路径：按时间步遍历 Z 轴的 0, 1, 2 层
        for step in range(3):
            layer = cube[step]
            # 遍历该层的 XY 平面
            for y in range(3):
                for x in range(3):
                    if layer[y][x] == 1:
                        op_name = self.xy_to_op.get((x, y))
                        if op_name:
                            recovered_path.append(op_name)
                            
        return base_state, recovered_path


if __name__ == "__main__":
    print("=" * 60)
    print("☯️ 分形指令记忆引擎 (时间与空间解耦修复版)")
    print("=" * 60)
    
    memory = FractalInstructionMemory()
    base_state = (1, 1)
    path = ["全加5", "外卦乘3", "外卦乘3"]
    
    print(f"原始输入 -> 基态: {base_state}, 指令串: {path}")
    
    cube = memory.encode(base_state, path)
    
    print("\n[物理写入] 分形立方体内部存储矩阵:")
    for z in range(3):
        print(f"  --- Z层 {z+1} ---")
        for row in cube[z]:
            print(f"    {row}")
            
    decoded_base, decoded_path = memory.decode(cube)
    
    print(f"\n[全息唤醒] 从立方体读取 -> 基态: {decoded_base}, 指令串: {decoded_path}")
    
    if decoded_base == base_state and decoded_path == path:
        print("\n✅ 完美！记忆已被完美压缩，并精确存储在分形空间中。")
    else:
        print("\n❌ 解码不一致，请检查坐标映射。")
