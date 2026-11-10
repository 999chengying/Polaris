# -*- coding: utf-8 -*-
"""
Polaris 终极心智引擎：五言绝句生成 (心智驱动版)
展示 外部刺激 -> 六爻比应(Cross-Attention) -> 情绪频段 -> 意象生成 的全链路。
"""

VOCAB_2 = {
    "HOT":    ["烈日", "长空", "飞火", "狂歌", "明光", "耀世", "赤炎", "长风"],
    "COLD":   ["孤城", "寒渊", "暗夜", "冷雪", "悲风", "泣血", "残月", "深渊"],
    "CALM":   ["明月", "清泉", "高山", "幽谷", "云淡", "风轻", "闲云", "古木"],
    "BLOCK":  ["闭门", "绝壁", "重山", "困兽", "死局", "断剑", "残垣", "孤影"],
    "FLUID":  ["云影", "游龙", "飞花", "幻梦", "缥缈", "清风", "流水", "浮萍"]
}

VOCAB_3 = {
    "HOT":    ["破苍穹", "向天笑", "照九州", "舞长风", "燃星火", "震九霄", "烈如歌", "吞山河"],
    "COLD":   ["骨生寒", "望天涯", "叹枯骨", "霜满天", "血染尘", "恨无穷", "泪已干", "夜无眠"],
    "CALM":   ["空留影", "独钓雪", "坐忘机", "水长流", "听松风", "隐山林", "伴月明", "意悠然"],
    "BLOCK":  ["路难行", "锁千愁", "拔剑顾", "恨无极", "退无路", "万骨枯", "音尘绝", "意难平"],
    "FLUID":  ["任平生", "随风舞", "过无痕", "渺无声", "天地宽", "一叶舟", "江海寄", "散如烟"]
}

class PolarisMind:
    def __init__(self):
        # 内部心智层（上卦），初始状态全为绝对平静（5）
        self.meta_cognition = {1: 5, 3: 5, 5: 5} 

    def interact(self, prompt):
        # 1. 外部感知映射（远景、中景、近景）
        text = prompt.replace(" ", "").replace("，", "")
        third = len(text) // 3
        segs = [text[:third], text[third:2*third], text[2*third:]]
        
        def safe_mod(s):
            if not s: return 6
            v = (sum(ord(c) for c in s) % 9) + 1
            return 8 if v == 5 else v
            
        external_states = {1: safe_mod(segs[0]), 3: safe_mod(segs[1]), 5: safe_mod(segs[2])}
        
        # 2. 六爻比应（Cross-Attention 心智碰撞）
        for x_plane in [1, 3, 5]:
            ext_val = external_states[x_plane]
            int_val = self.meta_cognition[x_plane]
            resonance = (ext_val * int_val) % 10 
            
            if resonance == 0 or resonance == 5:
                new_int_val = (int_val * 3 + ext_val) % 10
                if new_int_val == 5: new_int_val = 8 
            else:
                new_int_val = (int_val + ext_val) % 10
                if new_int_val == 0: new_int_val = 1
                
            self.meta_cognition[x_plane] = new_int_val

        return (self.meta_cognition[1], self.meta_cognition[3], self.meta_cognition[5])

class FiveCharDecoder:
    def __init__(self):
        self.history = set()

    def pick(self, vocab, score, offset):
        idx = (score + offset) % len(vocab)
        orig = idx
        while vocab[idx] in self.history:
            idx = (idx + 3) % len(vocab)
            if idx == orig: break
        word = vocab[idx]
        self.history.add(word)
        return word

    def generate_poem(self, mind_state):
        core = mind_state[2] # 取近景/元认知层决定情绪
        if core in [3, 9]: mood = "HOT"
        elif core in [7, 1]: mood = "COLD"
        elif core in [6, 4]: mood = "BLOCK"
        elif core == 8: mood = "FLUID"
        else: mood = "CALM"

        score = (mind_state[0]*1 + mind_state[1]*3 + mind_state[2]*5) % 10
        poem = []
        for i in range(4):
            w2 = self.pick(VOCAB_2[mood], score, i * 2)
            w3 = self.pick(VOCAB_3[mood], score, i * 3)
            poem.append(w2 + w3 + ("。" if i % 2 != 0 else "，"))
        return poem, mood

def run_demo():
    print("=" * 60)
    print("☯️ Polaris 终极心智引擎：五言绝句生成")
    print("=" * 60)
    
    brain = PolarisMind()
    prompts = [
        "高山流水琴三弄，明月清风酒一樽",
        "大军压境兵临城下，孤城岌岌可危",
        "春风拂面百花齐放，万物复苏生长"
    ]
    
    for p in prompts:
        print(f"\n👤 输入感知: 【{p}】")
        current_mind = brain.interact(p)
        print(f"🧠 心智特征: 远[{current_mind[0]}] 中[{current_mind[1]}] 近[{current_mind[2]}]")
        
        decoder = FiveCharDecoder()
        poem, mood = decoder.generate_poem(current_mind)
        print(f"🎭 主导情绪频段: {mood}")
        print(f"📜 [心智生成]:")
        print(f"    {poem[0]} {poem[1]}")
        print(f"    {poem[2]} {poem[3]}")

if __name__ == "__main__":
    run_demo()
