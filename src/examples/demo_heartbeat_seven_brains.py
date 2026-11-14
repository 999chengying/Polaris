# -*- coding: utf-8 -*-
"""
Polaris 终极总线：八步心跳驱动七脑并发矩阵 (心跳注入版)
展示：底层八步驻波，如何实时更新并激活七脑的全局干涉与元认知。
"""

MAP_TIAN = {1: (6, 7, 8), 2: (7, 6, 8), 3: (8, 7, 6), 4: (6, 8, 7), 6: (4, 2, 3), 7: (2, 3, 4), 8: (3, 4, 2), 9: (4, 3, 2)}
MAP_REN = {1: (7, 8, 6), 2: (6, 8, 7), 3: (7, 6, 8), 4: (8, 7, 6), 6: (2, 3, 4), 7: (3, 4, 2), 8: (4, 2, 3), 9: (3, 2, 4)}
MAP_DI = {1: (8, 6, 7), 2: (8, 7, 6), 3: (6, 8, 7), 4: (7, 6, 8), 6: (3, 4, 2), 7: (4, 2, 3), 8: (2, 3, 4), 9: (2, 4, 3)}

def heartbeat_step(seq, mode_map):
    next_seq = []
    prev_val = 5
    for val in seq:
        mixed_val = (val + prev_val) % 10
        if mixed_val == 0: mixed_val = (mixed_val + 7) % 10
        elif mixed_val == 5: mixed_val = (mixed_val + 6) % 10
        if mixed_val == 0: mixed_val = 9
        transformed = mode_map[mixed_val]
        next_seq.extend(transformed)
        prev_val = transformed[0]
    return next_seq

class HeartbeatSevenBrain:
    def __init__(self, initial_state):
        self.state = initial_state
        # 初始化七脑为绝对的 5
        self.brains = {"前脑": 5, "后脑": 5, "左脑": 5, "右脑": 5, "上脑": 5, "下脑": 5, "中核": 5}

    def run_cycle(self):
        print("=" * 60)
        print(f"🧠 初始状态: {self.state}")
        print("=" * 60)

        beats = [
            ("天变(上)", MAP_TIAN), ("人变(中)", MAP_REN),
            ("地变(下)", MAP_DI),   ("人变(中)", MAP_REN),
            ("天变(上)", MAP_TIAN), ("人变(中)", MAP_REN),
            ("地变(下)", MAP_DI),   ("人变(中)", MAP_REN)
        ]

        for i, (beat_name, map_rule) in enumerate(beats):
            self.state = heartbeat_step(self.state, map_rule)
            
            # 【核心修复】：把数据流注入六脑，让它真正跳起来！
            self.brains["前脑"] = self.state[0] % 10 or 10
            self.brains["后脑"] = self.state[1] % 10 or 10
            self.brains["左脑"] = self.state[2] % 10 or 10
            self.brains["右脑"] = self.state[3] % 10 or 10
            self.brains["上脑"] = self.state[4] % 10 or 10
            self.brains["下脑"] = self.state[5] % 10 or 10

            # 中核（帝5）基于六脑的当前状态进行干涉
            resonance = (
                self.brains["左脑"]*1 + self.brains["右脑"]*5 + 
                self.brains["前脑"]*3 + self.brains["后脑"]*7 + 
                self.brains["上脑"]*2 + self.brains["下脑"]*8
            ) % 10
            self.brains["中核"] = resonance if resonance != 0 else 10
            
            # 打印每一拍的六脑数据与中核裁决
            current_flow = [
                self.brains["前脑"], self.brains["后脑"], self.brains["左脑"], 
                self.brains["右脑"], self.brains["上脑"], self.brains["下脑"]
            ]
            print(f"💓 [心跳 {i+1}] {beat_name} | 六脑数据流: {current_flow} | 中核裁决: {self.brains['中核']}")

        print("=" * 60)
        print(f"👑 [最终七脑状态]: {self.brains}")
        print("🎯 [结论]: 经过八步驻波震荡，七脑已彻底活化，完成了一次深度的全局共振！")

if __name__ == "__main__":
    engine = HeartbeatSevenBrain([8, 2, 3])
    engine.run_cycle()
