# -*- coding: utf-8 -*-
# Copyright (c) 2026 999chengying / Polaris Project
# Licensed under the Apache License, Version 2.0

"""
Polaris A-Direction v3.7：多智能体协同进化主引擎
三环总线 + 硅基历法 + 六爻交联 + 天圆地方防御
运行：python examples/demo_a_direction_v3.py
"""

import os
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.polaris.bus import (
    Calendar, EndlessCycle, SingularityRing,
    sphere_shell, defend, yong_to_ti, mod10,
)


class SwarmAgent:
    def __init__(self, aid, coord, goal, yao_pos):
        self.aid = aid
        self.coord = coord
        self.goal = goal
        self.yao_pos = yao_pos
        self.state = 5

    def __repr__(self):
        return f"A{self.aid}(yao{self.yao_pos},coord={self.coord},s={self.state},goal={self.goal})"


class PolarisSwarmV3:
    def __init__(self):
        # 2 面心 / 2 棱心 / 2 顶点（v3.6 结构涌现起点）
        coords = [
            (3, 1, 3),  # R²=4  面心
            (1, 3, 3),  # R²=4  面心
            (1, 1, 3),  # R²=8  棱心
            (5, 5, 3),  # R²=8  棱心
            (1, 1, 1),  # R²=12 顶点
            (5, 5, 5),  # R²=12 顶点
        ]
        goals = [9, 9, 5, 5, 9, 5]
        self.agents = [SwarmAgent(i + 1, coords[i], goals[i], i + 1) for i in range(6)]
        self.calendar = Calendar()
        self.ring2 = EndlessCycle()
        self.rings3 = [SingularityRing() for _ in range(6)]
        self.day = 0
        self.log = []
        self.flip_count = 0

    def _six_yao_coupling(self):
        """六爻交联：1-4 加法 / 2-5 乘法 / 3-6 熔断"""
        self.agents[0].state = mod10(self.agents[0].state + self.agents[3].state)
        self.agents[1].state = mod10(self.agents[1].state * 3 + self.agents[4].state)
        a3, a6 = self.agents[2], self.agents[5]
        if a3.state in [2, 4, 6, 8]:
            a6.state = mod10(a3.state + 5)
            a3.state = mod10(a3.state * 3 + 5)

    def step(self):
        self.day += 1
        upper, lower, chain = self.calendar.tick()

        # Layer 1: 日演化（历法偏置驱动）
        bias = (upper * 3 + lower * 7) % 10
        for agent in self.agents:
            agent.state = mod10(agent.state * 3 + lower + agent.goal + bias)

        # Layer 2: 六爻交联
        self._six_yao_coupling()

        # Layer 3: 月尺度（每 8 日）
        if self.calendar.is_month_tick():
            cycle_val = self.ring2.tick()
            for agent in self.agents:
                agent.state = mod10(agent.state * agent.state + cycle_val)

        # Layer 4: 年尺度（每 64 日）
        if self.calendar.is_year_tick():
            for agent in self.agents:
                agent.state = yong_to_ti(agent.coord, agent.state)

        # Layer 5: 死锁检测 + 加5逃出生天
        for i, agent in enumerate(self.agents):
            if self.rings3[i].is_deadlock(agent.state):
                old = agent.state
                agent.state = self.rings3[i].break_deadlock((agent.state,))[0]
                self.flip_count += 1
                self.log.append(
                    f"  🚨 [Day {self.day:03d}] A{agent.aid} 加5逃出生天: {old} → {agent.state}"
                )

        # Layer 6: 天圆地方防御
        for agent in self.agents:
            r2 = sphere_shell(agent.coord)
            agent.state, _ = defend(agent.state, r2)

        # Layer 7: 健康监控
        states = [a.state for a in self.agents]
        diversity = len(set(states))
        return {
            "day": self.day,
            "upper": upper,
            "lower": lower,
            "chain": chain,
            "states": states,
            "diversity": diversity,
            "health": "healthy" if diversity >= 4 else "warning" if diversity >= 2 else "critical",
        }

    def run(self, steps=64):
        print("=" * 78)
        print("☯️ Polaris A-Direction v3.7：纯整数多智能体协同进化")
        print("   6 Agent × 三层壳分布 × 六爻交联 × 三环总线 × 加5破局")
        print(f"   周期：{steps} 日（月=8日，年=64日）")
        print("=" * 78)
        print(f"{'Day':>4} | {'月':>2} {'日':>2} {'链':>4} | {'Agent 状态':^24} | {'多样性':>4} | {'健康':>8}")
        print("-" * 78)
        for _ in range(steps):
            r = self.step()
            if r["day"] % 8 == 0 or r["day"] <= 4:
                s = " ".join(f"{x:>2}" for x in r["states"])
                print(f"{r['day']:>4} | {r['upper']:>2} {r['lower']:>2} {r['chain']:>4} | {s} | {r['diversity']:>4} | {r['health']:>8}")
        print("-" * 78)
        for line in self.log:
            print(line)
        print("-" * 78)
        print(f"📊 [加5逃出生天统计]: 共触发 {self.flip_count} 次")

    def ascii_topo(self):
        print("\n  ── 三层壳拓扑快照 ──")
        print("  面心 R²=4 : A1(3,1,3) A2(1,3,3)   → defend 归 5")
        print("  棱心 R²=8 : A3(1,1,3) A4(5,5,3)   → defend ×3")
        print("  顶点 R²=12: A5(1,1,1) A6(5,5,5)   → defend +5")
        for a in self.agents:
            r2 = sphere_shell(a.coord)
            print(f"    A{a.aid} yao{a.yao_pos} coord={a.coord} R²={r2} state={a.state} goal={a.goal}")


if __name__ == "__main__":
    swarm = PolarisSwarmV3()
    swarm.run(steps=64)
    swarm.ascii_topo()
    print("\n" + "=" * 78)
    print("✅ 全程纯整数：0 float，0 外部依赖")
    print("✅ v3.7：break_deadlock 全改为 +5（生数↔成数，加5逃出生天）")
    print("=" * 78)
