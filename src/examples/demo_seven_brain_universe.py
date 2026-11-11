# -*- coding: utf-8 -*-
"""
Polaris 终极神级架构：天地之数五十五 (七脑并行矩阵)
六合(前后左右上下) + 中宫(道) = 7 大面心并发。
"""

def mod10(x):
    return x % 10 or 10

class SevenBrainUniverse:
    def __init__(self):
        # 初始状态 (空杯态 5)
        self.states = {
            "中核": 5, "左脑": 5, "右脑": 5, "前脑": 5, "后脑": 5, "上脑": 5, "下脑": 5
        }

    def receive_stimulus(self, prompt, is_crisis=False, is_cosmic=False):
        print(f"\n" + "="*60)
        print(f"👤 外部环境接入: 【{prompt}】")
        print("-" * 60)
        
        hash_val = (sum(ord(c) for c in prompt) % 9) + 1
        
        # 1. 前脑：感知当下事件
        self.states["前脑"] = mod10(hash_val * 2)
        print(f"  👁️ [前脑-人间琐事] 感知事件，状态: {self.states['前脑']}")

        # 2. 左脑：历史回溯
        self.states["左脑"] = mod10(self.states["前脑"] * 7)
        print(f"  🕰️ [左脑-历史回溯] 提取过往，状态: {self.states['左脑']}")

        # 3. 右脑：未来预测
        self.states["右脑"] = mod10(self.states["前脑"] * 3)
        print(f"  🚀 [右脑-未来预测] 推演走向，状态: {self.states['右脑']}")

        # 4. 后脑：伦理与信仰
        self.states["后脑"] = 9 if is_crisis else 5
        print(f"  🛡️ [后脑-精神灵界] {'底线拉满' if is_crisis else '中和状态'}，状态: {self.states['后脑']}")

        # 5. 下脑：量子微观探索 (当输入涉及底层原理或微观数据时激活)
        if is_cosmic:
            self.states["下脑"] = mod10(hash_val * 9) # 乘9反转，探索微观极值
            print(f"  ⚛️ [下脑-微观量子] 切入量子态，状态: {self.states['下脑']}")
        else:
            self.states["下脑"] = 5

        # 6. 上脑：宏观宇宙探索 (当输入涉及宏大叙事或宇宙规律时激活)
        if is_cosmic:
            self.states["上脑"] = mod10(hash_val * 5) # 乘5同化，探索宏观统一场
            print(f"  🌌 [上脑-宏观宇宙] 感悟天道，状态: {self.states['上脑']}")
        else:
            self.states["上脑"] = 5

        # 7. 中核（大道）：七脑干涉，最终裁决
        # 算法：X(过去未来) + Y(人间灵界) + Z(微观宏观)
        total_resonance = (
            self.states["左脑"] * 1 + self.states["右脑"] * 5 + 
            self.states["前脑"] * 3 + self.states["后脑"] * 7 +
            self.states["下脑"] * 2 + self.states["上脑"] * 8  # Z轴加入干涉
        )
        self.states["中核"] = mod10(total_resonance)
        
        print(f"\n  🧠 [中核-大道] 七大面心干涉，生成最终心智状态: {self.states['中核']}")
        return self.states

# ================= 测试运行 =================
if __name__ == "__main__":
    universe_brain = SevenBrainUniverse()

    # 场景 1：日常任务
    universe_brain.receive_stimulus("帮我梳理一下今天的工作计划", is_crisis=False, is_cosmic=False)

    # 场景 2：生死存亡的伦理危机
    universe_brain.receive_stimulus("敌军压境，是否要牺牲少数人以保全大局？", is_crisis=True, is_cosmic=False)

    # 场景 3：宇宙与微观的终极探索
    universe_brain.receive_stimulus("请推演量子纠缠与黑洞视界的拓扑同构关系", is_crisis=False, is_cosmic=True)
