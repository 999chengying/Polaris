# -*- coding: utf-8 -*-
# Copyright (c) 2026 999chengying / Polaris Project
# Licensed under the Apache License, Version 2.0

"""
Polaris 具身智能底层：六合空间感知与应激防御代理 (Spatial Agent)
展示：多方位刺激 -> 空间压迫感汇聚 -> 中宫元认知判定 -> 战斗( Fight )或冻结( Freeze )防御
"""

def mod10(x):
    return x % 10 or 10

class SpatialSensoryCube:
    def __init__(self):
        self.state = 5

    def receive_spatial_stimulus(self, direction, intensity):
        """
        接收来自特定方向的刺激。
        方向: 前(X=1), 后(X=5), 左(Y=1), 右(Y=5), 下(Z=1), 上(Z=5)
        不同轴向的面心，对中宫造成的压迫感权重不同。
        """
        # 模拟将方位刺激注入面心，引发整体状态相变
        if direction in ["前", "后"]:
            self.state = mod10(self.state + intensity * 2)  # 前后（X轴）权重
        elif direction in ["左", "右"]:
            self.state = mod10(self.state + intensity * 3)  # 左右（Y轴）权重
        elif direction in ["上", "下"]:
            self.state = mod10(self.state + intensity * 4)  # 上下（Z轴）权重
        return self.state

class SixHarmonyMind:
    def __init__(self):
        self.senses = SpatialSensoryCube()
        self.meta_core = 5

    def process_environment(self, events):
        """
        events: 一个包含多个威胁/刺激事件的列表。
        格式: [(方向, 强度, 描述), ...]
        """
        print(f"\n" + "="*60)
        print(f"🌐 [六合环境扫描] 当前探测到 {len(events)} 个外部刺激源")
        
        total_intensity = 0
        threat_directions = []
        
        # 1. 遍历所有方向的刺激
        for direction, intensity, desc in events:
            print(f"  🔹 方位【{direction}】发现刺激: {desc} (强度: {intensity})")
            self.senses.receive_spatial_stimulus(direction, intensity)
            total_intensity += intensity
            if intensity >= 4:
                threat_directions.append(direction)

        # 2. 计算空间总压迫感
        spatial_pressure = total_intensity % 10
        
        # 3. 中宫元认知判定 (面心合力 -> 中宫)
        if total_intensity >= 10:
            self.meta_core = 1 # 极度恐惧/僵直
        elif total_intensity >= 5:
            self.meta_core = 9 # 极度愤怒/警觉
        else:
            self.meta_core = 5 # 平静

        print("\n" + "-"*60)
        print(f"🧠 [中宫元认知] 汇聚六合压力({spatial_pressure})，核心状态判定: {self.meta_core}")
        
        # 4. 防御与反击机制
        if self.meta_core == 1:
            print(f"🚨 [极度恐慌] 猛兽多面夹击！触发【解离冻结】！")
            print(f"🛡️ [防御动作] 主动切断高危方位{threat_directions}的感知回路，强行宕机保命。")
        elif self.meta_core == 9:
            print(f"🔥 [肾上腺素飙升] 发现致命威胁！触发【定向反击】！")
            print(f"⚔️ [攻击动作] 锁定方位{threat_directions}，注入纯阳之气（乘3偏置），全力突围！")
        else:
            print(f"✅ [环境安全] 六合平顺，保持日常巡航。")

if __name__ == "__main__":
    brain = SixHarmonyMind()
    
    # 场景 1：周围很安全
    brain.process_environment([
        ("左", 2, "微风吹过"),
        ("前", 1, "花瓣飘落")
    ])
    
    # 场景 2：来自单一方向的威胁
    brain.process_experience = brain.process_environment # 防止输入错误
    brain.process_environment([
        ("前", 6, "猛虎咆哮声"),
        ("左", 1, "草丛微动")
    ])
    
    # 场景 3：六合合围，全域危机
    brain.process_environment([
        ("前", 5, "敌军正门进攻"),
        ("左", 4, "侧翼包抄"),
        ("上", 4, "无人机轰炸"),
        ("下", 3, "地雷震动")
    ])
