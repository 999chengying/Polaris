# -*- coding: utf-8 -*-
"""
Polaris 应用研究：甲号用附值——真·六面并发变阵 (三头六臂)
修复：进位触发条件、身死影走状态切换、中宫跳闸联动。
"""

def mod10(x):
    return x % 10

class ConcurrentHexagramCube:
    def __init__(self):
        self.state = {
            "X": {"lower": 8, "upper": 1},
            "Y": {"lower": 4, "upper": 9},
            "Z": {"lower": 1, "upper": 6}
        }
        self.middle_palace = 5

    def add_one_with_carry(self, axis):
        s = self.state[axis]
        if s["lower"] < 9:
            s["lower"] += 1
            return False
        else:
            s["lower"] = 0 
            s["upper"] = 1 
            self.middle_palace = 0
            self.middle_palace = 5
            return True

    def apply_mutation(self, axis, mutation_type):
        s = self.state[axis]
        if mutation_type == "乘9":
            s["lower"] = mod10(s["lower"] * 9)
            s["upper"] = mod10(s["upper"] * 9)
        elif mutation_type == "加5":
            s["lower"] = mod10(s["lower"] + 5)
            s["upper"] = mod10(s["upper"] + 5)

    def switch_dominant(self):
        print("  👑 [帝5仲裁] 切换主导权，Y轴接管主导！")
        self.state["X"] = self.state["Y"].copy()
        self.state["Y"] = self.state["Z"].copy()
        self.state["Z"] = {"lower": 1, "upper": 6}

    def print_state(self, title):
        print(f"--- {title} ---")
        print(f"  [中宫]: {self.middle_palace}")
        for axis in ["X", "Y", "Z"]:
            role = "身" if axis == "X" else ("影1" if axis == "Y" else "影2")
            gua = f"{self.state[axis]['upper']}/{self.state[axis]['lower']}"
            print(f"  [{role} {axis}轴]: 卦象 {gua}")

    def evolve(self):
        print("=" * 60)
        print("☯️ 甲号用附值：六面并发变阵 (真·三军联动)")
        print("=" * 60)
        self.print_state("初始状态")

        print("\n>>> 第 1 步：X轴下卦 +1 (当前 1/8 -> 1/9)")
        self.add_one_with_carry("X")
        self.print_state("未触发进位")

        print("\n>>> 第 2 步：X轴下卦 +1 (当前 1/9 -> 1/0，触发进位！)")
        if self.add_one_with_carry("X"):
            print("  🚨 [中宫跳闸] 5 -> 0 -> 5，触发进位相变！")
            self.apply_mutation("Y", "乘9")
            print("  🌪️ [影1 (Y轴)] 触发【乘9相变】。")
            self.apply_mutation("Z", "加5")
            print("  🌪️ [影2 (Z轴)] 触发【加5相变】。")
        self.print_state("并发演化后")

        print("\n>>> 第 3 步：身死影走")
        print("  💀 [身 (X轴)] 陷入死胡同！")
        self.switch_dominant()
        self.print_state("影走接管后")

if __name__ == "__main__":
    cube = ConcurrentHexagramCube()
    cube.evolve()
