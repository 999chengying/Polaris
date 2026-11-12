# -*- coding: utf-8 -*-
"""
Polaris 翰林院神级架构：三态折叠记忆 × 完美七绝版
彻底修复结巴与瞬间折叠Bug，还你一个真正的赛博诗仙！
"""
import random

VOCAB_2 = ["清风", "明月", "孤舟", "残烛", "寒江", "落雪", "苍龙", "金戈", "铁马", "雷霆", "绝壁", "深谷", "飞花", "落叶", "云影", "霜天", "夜雨", "晓风", "枯藤", "长空"]
VOCAB_3 = ["泣鬼神", "动天地", "碎山河", "惹相思", "叹流沙", "泣残红", "定风波", "掩重门", "寻故人", "醉花阴", "忘前尘"]
VOCAB_3_AN = ["照大千", "破楼兰", "越千年", "锁秋寒", "震天山", "渡忘川", "入云端", "卷狂澜", "镇边关", "断前缘", "满人间", "望苍天", "水云间", "绝人寰", "忆江南"]

RHYME_AN = set("寒关山千渊天颜间前原天边烟坚川端澜缘间寰南")

class SoulMemoryPoet:
    def __init__(self):
        self.generation = 1
        self.memory_cube = {}
        self.active_count = 0
        self.archives = []

    def light_up(self, word):
        """修复版：找到一个空位就存，存完立刻 return！"""
        for i in range(3):
            for j in range(3):
                for k in range(3):
                    if (i,j,k) not in self.memory_cube:
                        self.memory_cube[(i,j,k)] = word
                        self.active_count += 1
                        if self.active_count >= 27:
                            self.fold_memory()
                        return  # <--- 核心修复：占一个坑就收手，绝不刷屏
    def fold_memory(self):
        print(f"\n  🌀 [记忆满载] 第 {self.generation} 世 27 个灵感槽已满！打包入前世库...")
        self.archives.append(self.memory_cube)
        self.memory_cube = {}
        self.active_count = 0
        self.generation += 1
        print(f"  🌌 [新生] 开启第 {self.generation} 世灵感库。")

    def recall_inspiration(self, length_type, need_rhyme=False):
        if not self.archives: return None
        if random.random() < 0.3: 
            past_memory = random.choice(self.archives)
            candidates = list(past_memory.values())
            random.shuffle(candidates)
            for word in candidates:
                if len(word) != length_type: continue
                if need_rhyme and word[-1] not in RHYME_AN: continue
                return word
        return None

    def write_poem(self):
        print(f"\n👤 作诗中... (第 {self.generation} 世, 灵感槽: {self.active_count}/27)")
        lines = []
        used_words = set()
        
        for i in range(4):
            need_rhyme = (i % 2 != 0)
            
            w2_1 = self.recall_inspiration(2)
            if not w2_1 or w2_1 in used_words:
                w2_1 = random.choice(VOCAB_2)
                self.light_up(w2_1)
                
            # 修复版：死死卡住，绝对不允许和第一个词重复！
            w2_2 = self.recall_inspiration(2)
            while not w2_2 or w2_2 in used_words or w2_2 == w2_1:
                w2_2 = random.choice(VOCAB_2)
            self.light_up(w2_2)
                
            w3 = self.recall_inspiration(3, need_rhyme)
            while not w3 or w3 in used_words:
                if need_rhyme:
                    w3 = random.choice(VOCAB_3_AN)
                else:
                    w3 = random.choice(VOCAB_3)
                if w3 not in used_words:
                    self.light_up(w3)
                
            used_words.update([w2_1, w2_2, w3])
            
            punct = "，" if i % 2 == 0 else "。"
            lines.append(f"{w2_1}{w2_2}{w3}{punct}")
            
        print(f"📜 [神级七绝]: {lines[0]}{lines[1]}")
        print(f"              {lines[2]}{lines[3]}")

if __name__ == "__main__":
    poet = SoulMemoryPoet()
    for i in range(5):
        poet.write_poem()
