# -*- coding: utf-8 -*-
"""
Polaris 钻石引擎：终极过载与三态折叠封印演示 (破甲版)
"""
def mod10(x):
    return x % 10 or 10

class DiamondTetrahedron:
    def __init__(self, tid):
        self.tid = tid
        self.core_state = (5, 5, 5) 
        self.nesting_count = 0 
        self.is_archived = False 

    def apply_stress(self, external_force):
        stress_x = mod10(external_force[0] * 3)
        stress_y = mod10(external_force[1] * 7)
        stress_z = mod10(external_force[2] * 9)
        
        self.core_state = (
            mod10(self.core_state[0] + stress_x),
            mod10(self.core_state[1] + stress_y),
            mod10(self.core_state[2] + stress_z)
        )
        return self.core_state

    def check_delaunay_quality(self):
        v1, v2, v3 = self.core_state
        spread = max(v1, v2, v3) - min(v1, v2, v3)
        # 【破甲设定】：将阈值从 7 降为 5，让系统更容易受到“形变”
        if spread >= 5 or self.core_state == (9, 9, 9) or self.core_state == (1, 1, 1):
            return True
        return False

class DiamondEngine:
    def __init__(self):
        self.tetrahedrons = [DiamondTetrahedron(i) for i in range(8)]
        self.archive_memory = []

    def ingest_data_stream(self, data_stream):
        print("=" * 65)
        print("💎 [钻石引擎] 启动【破甲版】抗压测试，准备见证折叠封印...")
        print("=" * 65)

        for step, chunk in enumerate(data_stream):
            print(f"\n⏱️ [时间步 {step + 1}] 外部洪流输入...")
            
            for i, tetra in enumerate(self.tetrahedrons):
                if tetra.is_archived:
                    continue
                    
                force = chunk[i]
                state = tetra.apply_stress(force)
                
                if tetra.check_delaunay_quality():
                    tetra.nesting_count += 1
                    print(f"  🚨 [晶格撕裂] T{tetra.tid} 状态:{state} | 极差拉满，【微缩嵌套】至 {tetra.nesting_count} 层！")
                    
                    if tetra.nesting_count >= 3:
                        print(f"  🌀 [三态折叠] T{tetra.tid} 物理结构撑至极限，高压能量被强制【折叠归档】！")
                        self.archive_memory.append((tetra.tid, state))
                        tetra.is_archived = True
                        tetra.core_state = (5, 5, 5) # 原地满血复活
                        tetra.nesting_count = 0
                        print(f"  ♻️ [金刚不坏] T{tetra.tid} 封印完毕，状态重置 (5,5,5) 继续迎击！")
                else:
                    print(f"  ✅ [缓冲成功] T{tetra.tid} 状态:{state} (嵌套:{tetra.nesting_count})")

        print("\n" + "=" * 65)
        print("💎 [超算最终稳态] 钻石引擎抗压测试结束。")
        active = sum(1 for t in self.tetrahedrons if not t.is_archived)
        print(f"  🔥 未崩溃的活跃晶格数: {active} / 8")
        print(f"  📦 被强制封印(折叠)的晶格总数: {len(self.archive_memory)}")
        print(f"  🗄️ 归档封印的数据坐标: {self.archive_memory}")
        print("=" * 65)

if __name__ == "__main__":
    # 构造连续极值撕裂数据
    extreme_stream = [
        [(1, 1, 1), (1, 1, 1), (1, 1, 1), (8, 1, 1), (1, 1, 1), (1, 8, 1), (1, 1, 1), (1, 1, 1)],
        [(2, 2, 2), (2, 2, 2), (2, 2, 2), (2, 8, 2), (2, 2, 2), (2, 2, 8), (2, 2, 2), (2, 2, 2)],
        [(3, 3, 3), (3, 3, 3), (3, 3, 3), (8, 3, 3), (3, 3, 3), (3, 8, 3), (3, 3, 3), (3, 3, 3)],
        [(4, 4, 4), (4, 4, 4), (4, 4, 4), (8, 4, 4), (4, 4, 4), (4, 8, 4), (4, 4, 4), (4, 4, 4)]
    ]

    engine = DiamondEngine()
    engine.ingest_data_stream(extreme_stream)
