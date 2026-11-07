# -*- coding: utf-8 -*-
"""
Polaris 终极大整合：纯整数心智引擎 (Integrated Topological Engine)
串联：PolarisBlockV2 (演化) + PTPP (防幻觉) + Decoder (受限生成)
"""

def mod10(x):
    return x % 10

# ================= 1. 拓扑大脑：PolarisBlockV2 =================
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
    def __init__(self, d_model=4):
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
        current_seq_len = len(Q) 
        
        scores = [[sum(Q[i][d] * K[j][d] for d in range(self.d_model)) % 10 for j in range(current_seq_len)] for i in range(current_seq_len)]
        mask = [[1 if scores[i][j] == max(scores[i]) else 0 for j in range(current_seq_len)] for i in range(current_seq_len)]
        
        attn_out = [[0] * self.d_model for _ in range(current_seq_len)]
        for i in range(current_seq_len):
            for d in range(self.d_model):
                val = sum((V[j][d] + j) for j in range(current_seq_len) if mask[i][j] == 1)
                attn_out[i][d] = mod10(val)

        block_output = []
        for i, token in enumerate(attn_out):
            coord = self._hash_project(token)
            expert_node = self._route_to_expert(coord)
            expert_out = self.experts[expert_node].forward(token)
            
            if self.d_model > 2 and expert_out[2] % 2 == 0:
                expert_out[2] = mod10(expert_out[2] * 3) # 六爻熔断
                
            memory_out = self.memory.forward(expert_out)
            hybrid_out = [mod10(expert_out[d] + memory_out[d]) for d in range(self.d_model)]
            block_output.append(hybrid_out)
            
        return block_output

# ================= 2. 免疫系统：PTPP 防幻觉网关 =================
class PTPP_Gateway:
    @staticmethod
    def causal_steer(state):
        # 兼容 4 维及以上特征，只取前 3 维进行拓扑诊断
        d1, d2, d3 = state[0], state[1], state[2]
        consensus = (d1 * 3 + d2 * 5 + d3 * 7) % 10
        
        if consensus >= 7:
            return state, consensus, False
            
        diff = (8 - consensus) % 10
        
        # 将原始 state 转为 list 进行修补
        new_state = list(state)
        new_state[2] = mod10(new_state[2] + diff) # 只在控制轴上打补丁
        return tuple(new_state), consensus, True

# ================= 3. 发声器官：受限纯整数解码器 =================
class TopologicalSyntaxFSM:
    def __init__(self):
        self.state = 0 # 0:主语, 1:谓语, 2:宾语, 3:标点
        self.transitions = {0: [1, 1, 0], 1: [2, 3], 2: [3, 0], 3: [0]}

    def advance(self, chosen_state):
        self.state = chosen_state

class TopologicalDecoder:
    def __init__(self):
        self.fsm = TopologicalSyntaxFSM()
        self.vocab_by_pos = {
            0: ["我", "你", "他", "宇宙", "日月", "天地", "神明", "众生"], 
            1: ["看见", "孕育", "超越", "打破", "化作", "照亮", "吞噬", "回归"], 
            2: ["星光", "虚无", "真理", "幻象", "洪荒", "深渊", "极乐", "本源"], 
            3: ["。", "！", "？", "，"] 
        }
        self.history = set()

    def decode_step(self, topo_features):
        expected_pos = self.fsm.state
        candidates = self.vocab_by_pos[expected_pos]
        
        score = sum((topo_features[i] * (i + 3)) for i in range(len(topo_features)))
        idx = score % len(candidates)
        
        original_idx = idx
        while candidates[idx] in self.history:
            idx = (idx + 3) % len(candidates)
            if idx == original_idx:
                self.history.clear()
                break
                
        chosen_word = candidates[idx]
        self.history.add(chosen_word)
        
        next_states = self.fsm.transitions[expected_pos]
        next_state_idx = (topo_features[0] + len(chosen_word)) % len(next_states)
        self.fsm.advance(next_states[next_state_idx])
        
        return chosen_word

# ================= 4. 核心引擎：全链路自回归闭环 =================
class PolarisEngine:
    def __init__(self):
        self.block = PolarisBlockV2(d_model=4)
        self.decoder = TopologicalDecoder()
        self.ptpp = PTPP_Gateway()

    def generate(self, prompt, max_steps=10):
        print(f"\n🚀 [Polaris Engine 启动] 输入 Prompt: 【{prompt}】\n")
        
        seed = sum(ord(c) for c in prompt)
        current_features = [mod10(seed + i) for i in range(4)]
        
        output_text = ""
        
        for step in range(max_steps):
            Q = [current_features]
            K = [current_features]
            V = [current_features]
            block_out = self.block.forward(Q, K, V)[0]
            
            safe_features, old_consensus, intervened = self.ptpp.causal_steer(tuple(block_out))
            safe_features = list(safe_features)
            
            if intervened:
                print(f"  🚨 [步 {step+1}] PTPP 拦截幻觉！特征 {block_out} (共识度 {old_consensus}) -> 纠偏至 {safe_features}")
            
            word = self.decoder.decode_step(safe_features)
            output_text += word
            
            word_val = sum(ord(c) for c in word) % 10
            current_features = [mod10(safe_features[i] + word_val + i) for i in range(4)]
            
            print(f"  步 {step+1:02d} | 特征演化: {block_out} -> {safe_features} | 解码输出: 【{word}】")

        print(f"\n🎯 [最终生成结果]: {output_text}")
        print("=" * 60)


if __name__ == "__main__":
    print("=" * 60)
    print("☯️ Polaris 纯整数全链路闭环引擎 (自回归版)")
    print("=" * 60)
    
    engine = PolarisEngine()
    engine.generate("天地", max_steps=10)
