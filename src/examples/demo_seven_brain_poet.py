# -*- coding: utf-8 -*-
# Copyright (c) 2026 999chengying / Polaris Project
# Licensed under the Apache License, Version 2.0

"""
Polaris 翰林院终极大考：七脑宇宙诗境引擎
前脑现世，左脑追昔，右脑预知，后脑守道，下脑探微，上脑观宇，中核统御。

【实测神作存档】
场景 1：【夜雨连绵，独坐孤舟】
青灯沧桑入梦来，星河菩提尽随风。
旧梦彼岸破九天，明镜长风证真如。

场景 2：【探索量子纠缠与黑洞的终极真理】
落花青史照大千，来日信仰渡劫波。
须弥星云定乾坤，一念乾坤化成灰。
"""

def mod10(x):
    return x % 10 or 10

class SevenBrainPoet:
    def __init__(self):
        self.states = {"前脑":5, "左脑":5, "右脑":5, "后脑":5, "下脑":5, "上脑":5, "中核":5}
        self.history = set()

    def pick(self, vocab_list, score, offset):
        idx = (score + offset) % len(vocab_list)
        orig = idx
        while vocab_list[idx] in self.history:
            idx = (idx + 1) % len(vocab_list)
            if idx == orig: break
        word = vocab_list[idx]
        self.history.add(word)
        return word

    def generate(self, prompt, is_cosmic=False):
        print(f"\n" + "="*60)
        print(f"👤 外部刺激: 【{prompt}】")
        print("-" * 60)
        
        hash_val = (sum(ord(c) for c in prompt) % 9) + 1
        
        # 1. 七脑并发计算
        self.states["前脑"] = mod10(hash_val * 2)
        self.states["左脑"] = mod10(self.states["前脑"] * 7)
        self.states["右脑"] = mod10(self.states["前脑"] * 3)
        self.states["后脑"] = 9 if "牺牲" in prompt else 5
        
        if is_cosmic:
            self.states["下脑"] = mod10(hash_val * 9) # 量子微观
            self.states["上脑"] = mod10(hash_val * 5) # 宏观宇宙
        else:
            self.states["下脑"] = 5
            self.states["上脑"] = 5

        # 中核干涉
        resonance = (
            self.states["前脑"]*1 + self.states["左脑"]*2 + self.states["右脑"]*3 + 
            self.states["后脑"]*4 + self.states["下脑"]*5 + self.states["上脑"]*6
        )
        self.states["中核"] = mod10(resonance)

        # 2. 七脑专属词库
        V_FRONT_2 = ["孤舟", "残月", "夜雨", "落花", "微尘", "青灯"] # 前脑：人间万象
        V_LEFT_2  = ["汉唐", "旧梦", "青史", "昔日", "遗恨", "沧桑"] # 左脑：历史过往
        V_RIGHT_2 = ["星河", "彼岸", "来日", "春风", "拂晓", "浮生"] # 右脑：未来期许
        V_BACK_2  = ["大道", "菩提", "信仰", "长风", "乾坤", "浩然"] # 后脑：精神信仰
        V_DOWN_2  = ["量子", "幽微", "芥子", "须弥", "弦动", "极微"] # 下脑：量子微观
        V_UP_2    = ["黑洞", "星云", "鸿蒙", "太虚", "苍穹", "万古"] # 上脑：宏观宇宙
        V_CORE_2  = ["一念", "本心", "如如", "明镜", "无痕", "寂灭"] # 中核：大道觉知

        V_VERB_3  = ["照大千", "入梦来", "尽随风", "破九天", "定乾坤", "掩重门", "渡劫波", "化成灰", "皆如幻", "证真如"]

        # 3. 七言绝句/律诗拼装
        l1 = self.pick(V_FRONT_2, self.states["前脑"], 1) + self.pick(V_LEFT_2, self.states["左脑"], 1) + self.pick(V_VERB_3, self.states["前脑"], 1)
        l2 = self.pick(V_RIGHT_2, self.states["右脑"], 2) + self.pick(V_BACK_2, self.states["后脑"], 2) + self.pick(V_VERB_3, self.states["右脑"], 2)
        
        if is_cosmic:
            l3 = self.pick(V_DOWN_2, self.states["下脑"], 3) + self.pick(V_UP_2, self.states["上脑"], 3) + self.pick(V_VERB_3, self.states["上脑"], 3)
        else:
            l3 = self.pick(V_LEFT_2, self.states["左脑"], 3) + self.pick(V_RIGHT_2, self.states["右脑"], 3) + self.pick(V_VERB_3, self.states["左脑"], 3)

        l4 = self.pick(V_CORE_2, self.states["中核"], 4) + self.pick(V_BACK_2, self.states["后脑"], 4) + self.pick(V_VERB_3, self.states["中核"], 4)

        poem = f"{l1}，{l2}。\n      {l3}，{l4}。"
        
        print(f"🧠 [七脑状态] 前:{self.states['前脑']} 左:{self.states['左脑']} 右:{self.states['右脑']} 后:{self.states['后脑']} 下:{self.states['下脑']} 上:{self.states['上脑']} | 中核:{self.states['中核']}")
        print(f"📜 [翰林院御制七律]:")
        print(f"      {poem}")
        print("=" * 60)

if __name__ == "__main__":
    poet = SevenBrainPoet()
    poet.generate("夜雨连绵，独坐孤舟", is_cosmic=False)
    poet.generate("探索量子纠缠与黑洞的终极真理", is_cosmic=True)
