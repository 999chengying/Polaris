# -*- coding: utf-8 -*-
"""
Polaris 终极战役：PolarisBlock V2 驱动的诗丹合璧引擎（探花卷轴·绝对无重字版）
"""

import random

def mod10(x):
    return x % 10

# ================= 1. 底层核心：PolarisBlock V2 =================
class ExpertFFN:
    def __init__(self, node_coord):
        self.bias = sum(node_coord) % 10
    def forward(self, token):
        return [mod10(val * 3 + self.bias) for val in token]

class TopologicalMemoryCell:
    def __init__(self, d_model, decay_rate=7):
        self.hidden_state = [0] * d_model
        self.decay_rate = decay_rate
    def forward(self, new_token):
        new_state = []
        for i in range(len(new_token)):
            decayed = mod10(self.hidden_state[i] * self.decay_rate)
            current = mod10(new_token[i] * (i + 1))
            new_state.append(mod10(decayed + current))
        self.hidden_state = new_state
        return self.hidden_state

class PolarisBlockV2:
    def __init__(self, seq_len, d_model):
        self.seq_len = seq_len
        self.d_model = d_model
        self.expert_coords = [(3,3,3), (3,1,3), (3,5,3), (1,3,3), (5,3,3), (3,3,1), (3,3,5), (3,1,1), (3,5,5), (3,1,5), (3,5,1)]
        self.experts = {node: ExpertFFN(node) for node in self.expert_coords}
        self.memory = TopologicalMemoryCell(d_model)

    def _hash_project(self, features):
        third = len(features) // 3
        if third == 0: return (3, 3, 3)
        segs = [features[:third], features[third:2*third], features[2*third:]]
        coord = []
        for seg in segs:
            val = int(abs(sum(seg) / len(seg))) % 10
            coord.append(1 if val < 3 else (5 if val > 6 else 3))
        return tuple(coord)

    def _route_to_expert(self, coord):
        return min(self.expert_coords, key=lambda e: sum(abs(coord[i] - e[i]) for i in range(3)))

    def forward(self, Q, K, V):
        scores = [[sum(Q[i][d] * K[j][d] for d in range(self.d_model)) % 10 for j in range(self.seq_len)] for i in range(self.seq_len)]
        mask = [[1 if scores[i][j] == max(scores[i]) else 0 for j in range(self.seq_len)] for i in range(self.seq_len)]
        
        attn_out = [[0] * self.d_model for _ in range(self.seq_len)]
        for i in range(self.seq_len):
            for d in range(self.d_model):
                val = sum((V[j][d] + j) for j in range(self.seq_len) if mask[i][j] == 1)
                attn_out[i][d] = mod10(val)

        block_output = []
        for i, token in enumerate(attn_out):
            coord = self._hash_project(token)
            expert_node = self._route_to_expert(coord)
            expert_out = self.experts[expert_node].forward(token)
            
            global_memory = self.memory.hidden_state
            if self.d_model > 2 and expert_out[2] % 2 == 0:
                expert_out[2] = mod10(expert_out[2] * 3) # 六爻熔断
                
            memory_out = self.memory.forward(expert_out)
            hybrid_out = [mod10(expert_out[d] + memory_out[d]) for d in range(self.d_model)]
            block_output.append(hybrid_out)
            
        return block_output

# ================= 2. 顶层应用：诗丹合璧引擎 =================
SCENERY = {
    "秋": {1: ["叶", "苔", "窗", "烛", "露", "阶", "影", "竹"], 2: ["林", "舟", "岸", "桥", "寺", "雁", "径", "松"], 3: ["山", "江", "云", "天", "海", "星", "川", "原"]},
    "春": {1: ["花", "草", "燕", "泥", "枝", "院", "柳", "絮"], 2: ["堤", "风", "雨", "楼", "径", "鸟", "水", "池"], 3: ["野", "春", "原", "光", "峦", "空", "林", "谷"]},
    "雪": {1: ["窗", "梅", "雪", "炉", "檐", "庭", "影", "冷"], 2: ["径", "松", "亭", "岭", "崖", "林", "谷", "石"], 3: ["莽", "冰", "极", "天", "原", "夜", "野", "荒"]},
    "离别": {1: ["泪", "酒", "杯", "手", "衣", "马", "袖", "语"], 2: ["长", "亭", "渡", "柳", "路", "客", "岸", "舟"], 3: ["天", "涯", "极", "渺", "空", "绝", "云", "海"]}
}
EMOTION = {
    "秋": {4: ["幽", "静", "闲", "微", "冷", "轻", "淡", "净"], 5: ["愁", "思", "悲", "望", "孤", "寒", "苦", "恨"], 6: ["空", "寂", "悟", "绝", "虚", "灭", "幻", "无"]},
    "春": {4: ["暖", "新", "轻", "醉", "微", "柔", "翠", "碧"], 5: ["狂", "叹", "喜", "恋", "盼", "迷", "愁", "怨"], 6: ["生", "荣", "释", "化", "同", "初", "空", "无"]},
    "雪": {4: ["寒", "洁", "寂", "冷", "凉", "清", "白", "明"], 5: ["孤", "绝", "傲", "叹", "凛", "凄", "苦", "愁"], 6: ["白", "空", "融", "虚", "净", "无", "化", "灭"]},
    "离别": {4: ["伤", "愁", "叹", "微", "苦", "泪", "冷", "暗"], 5: ["痛", "悲", "绝", "恨", "寂", "留", "苦", "怨"], 6: ["空", "释", "悟", "化", "同", "虚", "无", "灭"]}
}
VERBS = ["落", "飞", "流", "去", "来", "入", "涌", "生", "照", "掩", "破", "化", "尽", "度", "过", "寻"]
PING_SET = set(list("天寒云江风空山春深林清微幽松舟桥庭帆孤苍茫高川星原花枝无虚无空真明"))

META_VOCAB = {
    "空灵": ["空", "无", "虚", "极", "玄", "幽", "静", "灭", "尽"],
    "融合": ["同", "一", "融", "化", "合", "真", "道", "如", "契"],
    "主体": ["我", "心", "意", "念", "神", "元", "灵", "本", "性"],
    "宏观": ["万", "千", "众", "世", "劫", "古", "今", "因", "果", "宇"],
    "动词": ["归", "入", "见", "破", "生", "落", "隐", "彻", "转", "证"]
}

class UltimatePoetrySystem:
    def __init__(self, topic):
        self.topic = topic
        self.block = PolarisBlockV2(seq_len=4, d_model=4)
        self.seed = ord(topic[0])
        self.all_vocab = set(VERBS)
        for sc_dict in SCENERY.values():
            for pool in sc_dict.values(): self.all_vocab.update(pool)
        for em_dict in EMOTION.values():
            for pool in em_dict.values(): self.all_vocab.update(pool)

    def pseudo_random(self, max_val):
        self.seed = (self.seed * 1103515245 + 12345) % 2147483648
        return self.seed % max_val

    def get_ping_ze(self, char):
        return 0 if char in PING_SET else 1

    def get_rhyme(self, word):
        return sum(ord(c) for c in word) % 6

    def pick_word(self, pool, target_pz, used, target_rhyme=None):
        valid = [w for w in pool if self.get_ping_ze(w) == target_pz and w not in used]
        if target_rhyme is not None:
            r_valid = [w for w in valid if self.get_rhyme(w) == target_rhyme]
            if r_valid: valid = r_valid
            
        if not valid:
            valid = [w for w in self.all_vocab if self.get_ping_ze(w) == target_pz and w not in used]
        if not valid:
            valid = [w for w in self.all_vocab if w not in used]
        if not valid:
            valid = pool
            
        word = valid[self.pseudo_random(len(valid))]
        used.add(word)
        return word

    def generate_meta_couplet(self, dan_state, used):
        """修复了重字 Bug 的炼丹结句模块"""
        random.seed(dan_state * 88)
        
        def get_meta(category):
            # 全局去重过滤
            valid = [w for w in META_VOCAB[category] if w not in used]
            if not valid: valid = META_VOCAB[category]
            w = random.choice(valid)
            used.add(w)
            return w

        # 五言模板：主体(1) + 动词(1) + 宏观(1) + 融合(1) + 空灵(1)
        l1 = get_meta('主体') + get_meta('动词') + get_meta('宏观') + get_meta('融合') + get_meta('空灵')
        # 五言模板：宏观(1) + 动词(1) + 主体(1) + 空灵(1) + 融合(1) # 把最后一个改成融合，避免多个空灵词库撞车
        l2 = get_meta('宏观') + get_meta('动词') + get_meta('主体') + get_meta('空灵') + get_meta('融合')
        
        return l1, l2

    def run(self):
        print(f"☯️ 命题：【{self.topic}】\n")
        dummy_q = [[self.seed % 10] * 4 for _ in range(4)]
        block_features = self.block.forward(dummy_q, dummy_q, dummy_q)
        
        sc = SCENERY.get(self.topic, SCENERY["秋"])
        em = EMOTION.get(self.topic, EMOTION["秋"])
        used, target_rhyme = set(), sum(ord(c) for c in self.topic) % 6
        patterns = [[1, 1, 0, 0, 1], [0, 0, 1, 1, 0], [0, 0, 0, 1, 1], [1, 1, 1, 0, 0]]
        
        poem = []
        for i in range(4):
            line_chars = []
            level_seed = block_features[i][0] % 3 + 1
            for j in range(5):
                target_pz = patterns[i][j]
                if j == 2: pool = VERBS
                elif j < 4: pool = sc[level_seed]
                else: pool = em[4] if i == 0 else (em[5] if i in [1, 2] else em[6])
                rhyme_req = target_rhyme if (j == 4 and i in [1, 3]) else None
                word = self.pick_word(pool, target_pz, used, rhyme_req)
                line_chars.append(word)
            poem.append("".join(line_chars))

        state_vec = [sum(ord(c) for c in line) % 10 for line in poem]
        refined_vec = [(s * (1 if i==0 else (7 if i in [1,2] else 9))) % 10 for i, s in enumerate(state_vec)]
        final_dan = sum(refined_vec) % 10
        
        # 传入 used 集合，绝对排重
        l1, l2 = self.generate_meta_couplet(final_dan, used)
        
        # 2-2-2 唯美排版
        print(f"    {poem[0]}，{poem[1]}。\n")
        print(f"    {poem[2]}，{poem[3]}。\n")
        print(f"    {l1}，{l2}。")

if __name__ == "__main__":
    system = UltimatePoetrySystem("秋")
    system.run()
