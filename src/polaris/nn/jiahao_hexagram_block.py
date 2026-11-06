# -*- coding: utf-8 -*-
# Copyright (c) 2026 999chengying / Polaris Project
# Licensed under the Apache License, Version 2.0

"""
Polaris JiaHao Hexagram Block (甲号用附值 - 64卦三头六臂心智层)
整合：三对上下卦并发映射、位权进位、多重相变与跨轴拓扑救援。
"""

from typing import Dict, Tuple

class JiaHaoHexagramBlock:
    """
    甲号用附值模块。
    实现 64 卦的空间并发演化、影随身体联动以及死锁自动救援。
    """
    def __init__(self):
        # 截面物理数字分布
        self.axis_digits = {
            "X": {1, 2, 3, 4, 5, 6, 7, 8, 9},
            "Y": {1, 2, 3, 4, 5, 6, 7, 8, 9},
            "Z1": {1, 4, 5, 6, 9},       # 底层轴，缺 2,3,7,8
            "Z5": {1, 2, 3, 4, 5, 7, 8, 9} # 顶层轴，缺 6
        }
        # 初始状态 (X: 1/8, Y: 9/4, Z: 6/1)
        self.state = {
            "X": {"lower": 8, "upper": 1},
            "Y": {"lower": 4, "upper": 9},
            "Z": {"lower": 1, "upper": 6}
        }
        self.middle_palace = 5

    def _mod10(self, x: int) -> int:
        return x % 10

    def _try_mutation(self, axis_name: str, upper: int, lower: int, op_type: str) -> Tuple[bool, int, int]:
        """执行相变并检查物理地址合法性"""
        digits = self.axis_digits[axis_name]
        
        if op_type == "加5":
            new_upper = (upper + 5) % 10 or 10
            new_lower = (lower + 5) % 10 or 10
        elif op_type == "乘9":
            new_upper = self._mod10(upper * 9)
            new_lower = self._mod10(lower * 9)
        else:
            return False, upper, lower
            
        if new_upper in digits and new_lower in digits:
            return True, new_upper, new_lower
        return False, new_upper, new_lower

    def _add_one_with_carry(self, axis: str) -> bool:
        """基础加法循环与中宫跳闸"""
        s = self.state[axis]
        if s["lower"] < 9:
            s["lower"] += 1
            return False
        else:
            s["lower"] = 0
            s["upper"] = 1
            self.middle_palace = 0 # 中宫转换
            self.middle_palace = 5 # 恢复
            return True

    def step(self, step_type: str = "加1", op_axis: str = "X") -> Dict[str, str]:
        """
        执行一次心智演化步进。
        
        Args:
            step_type: "加1" 或 "相变"
            op_axis: 操作轴 "X", "Y", "Z"
            
        Returns:
            当前三轴状态字典
        """
        if step_type == "加1":
            carry = self._add_one_with_carry(op_axis)
            if carry:
                # 进位触发，影随身体变阵
                self._try_mutation("Y", self.state["Y"]["upper"], self.state["Y"]["lower"], "乘9")
                self._try_mutation("Z", self.state["Z"]["upper"], self.state["Z"]["lower"], "加5")
        
        elif step_type == "相变":
            # 如果在当前轴死锁，触发跨轴救援
            success, nu, nl = self._try_mutation(op_axis, self.state[op_axis]["upper"], self.state[op_axis]["lower"], "加5")
            
            if not success:
                # 救援机制：切换到 X 轴（1-9完备）
                rescue_axis = "X"
                res_success, res_u, res_l = self._try_mutation(rescue_axis, nu, nl, "加5")
                if res_success:
                    # 影走接管
                    self.state["X"]["upper"] = res_u
                    self.state["X"]["lower"] = res_l
            else:
                self.state[op_axis]["upper"] = nu
                self.state[op_axis]["lower"] = nl

        return self._get_gua_status()

    def _get_gua_status(self) -> Dict[str, str]:
        """返回当前各轴卦象"""
        return {
            axis: f"{s['upper']}/{s['lower']}" for axis, s in self.state.items()
        }

if __name__ == "__main__":
    block = JiaHaoHexagramBlock()
    print("初始状态:", block._get_gua_status())
    print("X轴加1推进:", block.step("加1", "X"))
    print("X轴再次加1（触发进位）：", block.step("加1", "X"))
    print("Z轴加5相变（遇到缺数触发救援）：")
    # 人为制造一个 Z 轴死锁测试
    block.state["Z"]["upper"] = 3
    block.state["Z"]["lower"] = 8
    print(block.step("相变", "Z"))
