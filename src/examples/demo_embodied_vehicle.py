# -*- coding: utf-8 -*-
# Copyright (c) 2026 999chengying / Polaris Project
# Licensed under the Apache License, Version 2.0

"""
Polaris 终极具身智能：纯整数自动驾驶决策引擎
展示：如何用拓扑状态机，在零延迟下完成物理避障与动作输出。
"""

class EmbodiedVehicle:
    def __init__(self):
        self.speed = 60 
        self.core_safety = 5 

    def drive(self, sensors):
        print(f"\n🚗 [车辆感知] 当前速度: {self.speed} km/h")
        print(f"  前方: {sensors['front']}m | 左侧: {sensors['left']}m | 右侧: {sensors['right']}m")
        
        def calc_threat(dist):
            if dist > 50: return 1
            if dist > 30: return 3
            if dist > 10: return 6
            return 9 

        front_t = calc_threat(sensors['front'])
        left_t  = calc_threat(sensors['left'])
        right_t = calc_threat(sensors['right'])
        
        print(f"  📡 [拓扑投影] 威胁度: 前[{front_t}] 左[{left_t}] 右[{right_t}]")
        core_interference = (right_t * 1 + left_t * 3 + front_t * 7) % 10
        print(f"  🧠 [中宫裁决] 综合干涉共识度: {core_interference}")

        action = "直行"
        if front_t >= 9:
            if core_interference % 2 == 0 and right_t < 5: action = "紧急右转"
            elif left_t < 5: action = "紧急左转"
            else: action = "全力刹车"
        elif front_t >= 6:
            action = "减速"
        elif core_interference < 4:
            action = "加速"

        if "刹车" in action: self.speed = max(0, self.speed - 30)
        elif "减速" in action: self.speed = max(0, self.speed - 10)
        elif "加速" in action: self.speed += 10

        print(f"  ⚙️ [执行总线]: **{action}** | 当前速度: {self.speed} km/h")

if __name__ == "__main__":
    car = EmbodiedVehicle()
    car.drive({"front": 100, "left": 100, "right": 100})
    car.drive({"front": 25, "left": 10, "right": 80})
    car.drive({"front": 5, "left": 10, "right": 10})
