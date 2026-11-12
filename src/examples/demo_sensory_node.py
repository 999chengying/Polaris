# -*- coding: utf-8 -*-
# Copyright (c) 2026 999chengying / Polaris Project
# Licensed under the Apache License, Version 2.0

"""
Polaris System Architecture：顶点感官节点（脏腑脑）独立运作演示
展示：中宫为2的感官节点，如何过滤底层噪音并独立完成局部反应。
"""

# 将咱们刚跑出的新立方体截面数据固化进去
SENSORY_CUBE = {
    1: [ # X=1 截面（后向溯源自检区，已坍缩，过滤低频噪音）
        [5, 4, 9],
        [5, 1, 6],
        [5, 5, 5]
    ],
    3: [ # X=3 截面（中宫核心区，中宫变为了2！）
        [7, 3, 1],
        [8, 2, 4],
        [5, 9, 6]
    ],
    5: [ # X=5 截面（前向输出区，依然保持完整的1-9，具备独立行动力）
        [2, 8, 6],
        [3, 7, 9],
        [5, 4, 1]
    ]
}

class SensoryNode:
    def __init__(self):
        self.core_state = 2 # 感官节点的中宫是 2 (巽风/敏锐)

    def receive_stimulus(self, direction, intensity):
        print(f"\n" + "="*50)
        print(f"📡 [边缘传感器] 接收到外部刺激: 方向[{direction}], 强度[{intensity}]")
        
        # 1. 如果是正向刺激（比如眼睛看到强光），走 X=5 完备截面
        if direction == "正向":
            print(f"👁️ [局部独立处理] 探查 X=5 完备截面...")
            feedback = (intensity * 7) % 10
            print(f"  -> 发现对应拓扑节点: {feedback}，具备完整的独立判断力！")
            print(f"  -> ✅ [局部反射弧] 感官节点无需上报主脑，直接完成局部收缩/避让。")
            
        # 2. 如果是反向刺激（比如身体内部的隐痛），走 X=1 坍缩截面
        elif direction == "反向":
            print(f"🧠 [局部溯源] 探查 X=1 坍缩截面...")
            valid_values = [1, 4, 5, 6, 9]
            if intensity in valid_values:
                print(f"  -> 发现对应拓扑节点: {intensity}，触发警觉。")
            else:
                print(f"  -> ⚠️ [噪音过滤] 强度 {intensity} 不在坍缩矩阵中，判定为底层背景噪音，被感官节点自动忽略！")
                
        # 3. 极端危机：需要中枢介入
        if intensity >= 9:
            print(f"  🚨 [极度危险] 刺激超过感官节点处理上限，触发中宫=2的极度警觉！")
            print(f"  🚀 [向上汇报] 紧急通过总线，将信号抛给主脑(帝5)进行全局裁决！")

if __name__ == "__main__":
    node = SensoryNode()
    node.receive_stimulus("正向", 3)
    node.receive_stimulus("反向", 2)
    node.receive_stimulus("反向", 9)
