# -*- coding: utf-8 -*-
"""
Polaris 三维点灯变卦模拟器 (字典纠错版)
"""

# 定义 X=1 (上卦) 和 X=5 (下卦) 的 3x3 空间截面矩阵
MATRIX_X1 = [
    [7, 3, 6],
    [2, 5, 4],
    [9, 1, 8]
]

MATRIX_X5 = [
    [2, 9, 1],
    [6, 5, 8],
    [4, 7, 3]
]

# 修正后的卦名字典（严格对照上下卦数字）
GUA_NAMES = {
    (1,6): "谦 (地山谦)", (9,4): "履 (天泽履)",
    (9,6): "遁 (天山遁)", (1,4): "临 (地泽临)",  # 此处修正为临卦
    (9,9): "乾 (乾为天)", (1,1): "坤 (坤为地)",
    (4,6): "咸 (泽山咸)", (7,8): "屯 (水雷屯)",
    (1,3): "明夷 (地火明夷)", (3,9): "大有 (火天大有)"
}

def get_gua_name(upper, lower):
    return GUA_NAMES.get((upper, lower), f"未知卦({upper}{lower})")

def draw_plane(matrix, active_val, layer_name):
    print(f"  [{layer_name}] 激活值: {active_val}")
    for row in matrix:
        row_str = ""
        for val in row:
            if val == active_val:
                row_str += f" [ \033[91m*{val}*\033[0m ] " 
            else:
                row_str += f" [  {val}  ] "
        print("      " + row_str)
    print()

class Polaris3DCube:
    def __init__(self, upper, lower):
        self.upper = upper  
        self.lower = lower  
        
    def show_state(self, title="当前状态"):
        print(f"\n--- {title} ---")
        print(f"  ☯️ 卦象：【{get_gua_name(self.upper, self.lower)}】")
        draw_plane(MATRIX_X1, self.upper, "X=1 截面 (上卦)")
        draw_plane(MATRIX_X5, self.lower, "X=5 截面 (下卦)")
        
    def cuo_transform(self):
        print(">>> 触发算子：【整体错卦 (Layer 2)】")
        print(f"    上卦变换: {self.upper} × 9 ≡ {self.upper * 9 % 10 or 10}")
        print(f"    下卦变换: {self.lower} × 9 ≡ {self.lower * 9 % 10 or 10}")
        self.upper = self.upper * 9 % 10 or 10
        self.lower = self.lower * 9 % 10 or 10
        
    def single_decouple_transform(self, axis, new_val):
        print(f">>> 触发算子：【单边解耦 (Layer 3)】只改变 {axis} 卦")
        if axis == 'upper':
            print(f"    上卦变换: 熄灭 {self.upper}，点亮 {new_val}")
            self.upper = new_val
        elif axis == 'lower':
            print(f"    下卦变换: 熄灭 {self.lower}，点亮 {new_val}")
            self.lower = new_val

if __name__ == "__main__":
    print("=" * 60)
    print("☯️ Polaris 三维拓扑变卦全流程演示 (字典纠错版)")
    print("=" * 60)
    
    cube = Polaris3DCube(upper=1, lower=6)
    cube.show_state("【初始状态】")
    
    cube.single_decouple_transform(axis='upper', new_val=9)
    cube.show_state("【单边解耦后】")
    
    cube.cuo_transform()
    cube.show_state("【整体错卦后】")
    
    print("=" * 60)
