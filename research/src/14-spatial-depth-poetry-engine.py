# -*- coding: utf-8 -*-
"""
Polaris 应用研究：基于球面景深的立体拓扑诗词引擎
利用半径平方 (R^2=4, 8, 12) 赋予词汇“特写、中景、远景”的空间纵深感。
"""

VOCAB_SHELLS = {
    4: { "名词": ["苔", "石", "露", "弦", "杯", "烛", "影", "叶", "阶", "窗"], "形容": ["幽", "微", "清", "湿", "静", "冷", "暗", "轻"] },
    8: { "名词": ["竹", "径", "舟", "风", "岸", "松", "林", "桥", "庭", "帆"], "形容": ["深", "寒", "翠", "长", "空", "晚", "寂"] },
    12: { "名词": ["山", "江", "云", "天", "海", "月", "星", "川", "雪", "原"], "形容": ["孤", "远", "苍", "浩", "茫", "残", "高"] }
}

PING_WORDS = "天寒云江风空山春深林清微幽松舟桥庭帆孤苍茫高川星原"
PING_SET = set(list(PING_WORDS))

def get_ping_ze(char): return 0 if char in PING_SET else 1
def get_rhyme_group(char): return ord(char) % 6

class SpatialPoetryEngine:
    def __init__(self, seed=888):
        self.seed = seed
        
    def pseudo_random(self, max_val):
        self.seed = (self.seed * 1103515245 + 12345) % 2147483648
        return self.seed % max_val

    def generate_poem(self, topic_char):
        poem = []
        ping_ze_patterns = [[1,1,0,0,1], [0,0,1,1,0], [1,1,0,0,1], [0,0,1,1,0]]
        grammar_patterns = [[2,0,1,2,0], [2,0,1,0,0], [0,0,1,0,0], [2,0,1,0,0]]
        
        target_rhyme = get_rhyme_group(topic_char)
        used_chars = set()

        for line_idx in range(4):
            line_chars = []
            for char_idx in range(5):
                target_pz = ping_ze_patterns[line_idx][char_idx]
                target_gram = grammar_patterns[line_idx][char_idx]
                is_rhyme = (char_idx == 4 and line_idx in [1, 3])
                
                if char_idx in [0, 1]: shell = 4
                elif char_idx in [2, 3]: shell = 8
                else: shell = 12
                
                if target_gram == 1: 
                    shell = 8
                    candidates = ["落", "飞", "流", "去", "来", "入", "涌", "生", "照", "掩", "过", "寻"]
                else:
                    if target_gram == 0: category = "名词"
                    else: category = "形容"
                    candidates = VOCAB_SHELLS[shell][category]

                valid = [w for w in candidates if get_ping_ze(w) == target_pz and w not in used_chars]
                if not valid: valid = candidates

                if is_rhyme:
                    rhyme_valid = [w for w in valid if get_rhyme_group(w) == target_rhyme]
                    if rhyme_valid: valid = rhyme_valid

                offset = self.pseudo_random(len(valid))
                word = valid[offset]
                used_chars.add(word)
                line_chars.append(word)
                
            poem.append("".join(line_chars))
            
        return poem

if __name__ == "__main__":
    engine = SpatialPoetryEngine()
    poem = engine.generate_poem("月")
    print("🎯 命题：【月】 (景深: 特写 -> 中景 -> 远景)")
    for line in poem:
        print(f"    {line}")
