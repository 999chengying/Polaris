# -*- coding: utf-8 -*-
"""
Polaris 端到端大整合：纯整数心智引擎微型 GPT (动态长度自适应版)
融合：动态多头路由 + 自愈注意力 + O(1) 极限记忆 + PolarisBlock主干
"""

def mod10(x):
    return x % 10

# ================= 1. 基础组件 =================
class TopologicalRotator:
    @staticmethod
    def next_post_to_pre(n: int) -> int:
        if n in (1, 2, 4, 7): return {1: 2, 2: 4, 4: 7, 7: 1}[n]
        elif n in (3, 9, 6, 8): return {3: 9, 9: 6, 6: 8, 8: 3}[n]
        return n

class TopologicalMemoryCell:
    def __init__(self, d_model=4):
        self.memory_pool = [[0] * d_model for _ in range(4)]
        self.step_count = 0
    def update_and_read(self, token_features, token_coord):
        self.step_count += 1
        u, l = token_coord
        for _ in range(self.step_count % 4):
            u, l = (TopologicalRotator.next_post_to_pre(u), TopologicalRotator.next_post_to_pre(l))
        target_slot = (u + l + self.step_count) % 4
        for i in range(len(token_features)):
            decay = (self.step_count + i) % 10
            self.memory_pool[target_slot][i] = mod10(self.memory_pool[target_slot][i] + token_features[i] + decay)
        return self.memory_pool[target_slot]

class ExpertFFN:
    def __init__(self, node_coord):
        self.bias = sum(node_coord) % 10
    def forward(self, token):
        return [mod10(val * 3 + self.bias) for val in token]

# ================= 2. 核心模块：多头融合 =================
class MultiHeadFusion:
    def dynamic_route_and_fuse(self, faces, context_weights):
        fused_upper, fused_lower = 0, 0
        for axis in ["X", "Y", "Z"]:
            val_1 = faces.get(f"{axis}1", 5)
            val_5 = faces.get(f"{axis}5", 5)
            weight = context_weights.get(axis, 5)
            if weight > 4:
                upper, lower = val_1, val_5
            else:
                upper, lower = val_5, val_1
            fused_upper = mod10(fused_upper + upper * weight)
            fused_lower = mod10(fused_lower + lower * weight)
        return (fused_upper, fused_lower)

# ================= 3. PolarisBlock =================
class PolarisBlock:
    def __init__(self, d_model):
        # 移除写死的 seq_len
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
        current_seq_len = len(Q) # 💡 动态获取当前序列长度
        
        # 1. WTA Attention
        scores = [[sum(Q[i][d] * K[j][d] for d in range(self.d_model)) % 10 for j in range(current_seq_len)] for i in range(current_seq_len)]
        mask = [[1 if scores[i][j] == max(scores[i]) else 0 for j in range(current_seq_len)] for i in range(current_seq_len)]
        attn_out = [[0] * self.d_model for _ in range(current_seq_len)]
        for i in range(current_seq_len):
            for d in range(self.d_model):
                val = sum((V[j][d] + j) for j in range(current_seq_len) if mask[i][j] == 1)
                attn_out[i][d] = mod10(val)

        # 2. MoE + 熔断 + O(1) 记忆
        block_output = []
        for i, token in enumerate(attn_out):
            coord = self._hash_project(token)
            expert_node = self._route_to_expert(coord)
            expert_out = self.experts[expert_node].forward(token)
            
            if self.d_model >= 3 and expert_out[2] % 2 == 0:
                expert_out[2] = mod10(expert_out[2] * 3) # 六爻熔断
                
            memory_coord = (expert_node[0], expert_node[1])
            memory_out = self.memory.update_and_read(expert_out, memory_coord)
            
            hybrid_out = [mod10(expert_out[d] + memory_out[d]) for d in range(self.d_model)]
            block_output.append(hybrid_out)
        return block_output

# ================= 4. 端到端模型 =================
class PolarisGPT:
    def __init__(self):
        self.vocab = {i: char for i, char in enumerate("天地玄黄宇宙洪荒日月")}
        self.reverse_vocab = {char: i for i, char in self.vocab.items()}
        
        self.fusion = MultiHeadFusion()
        # 不再传入固定的 seq_len，只需传入特征维度
        self.block1 = PolarisBlock(d_model=4)
        self.block2 = PolarisBlock(d_model=4)
        
    def text_to_features(self, text):
        features = []
        for c in text:
            base = self.reverse_vocab.get(c, 0) + 1
            features.append([base, mod10(base*2), mod10(base*3), mod10(base*5)])
        return features

    def forward(self, text):
        print(f"\n[Polaris Engine 启动] 输入文本: {text}")
        
        features = self.text_to_features(text)
        Q = [f[:] for f in features]
        K = [[mod10(v+2) for v in f] for f in features]
        V = [[mod10(v+4) for v in f] for f in features]
        
        layer1_out = self.block1.forward(Q, K, V)
        
        final_features = []
        for i, token in enumerate(layer1_out):
            context_weights = {"X": token[0], "Y": token[1], "Z": token[2]}
            faces = {"X1": token[0], "X5": token[1], "Y1": token[2], "Y5": token[3], "Z1": 5, "Z5": 5}
            
            fused_gua = self.fusion.dynamic_route_and_fuse(faces, context_weights)
            merged_feature = [token[0], fused_gua[0], fused_gua[1], token[3]]
            final_features.append(merged_feature)
            
        layer2_out = self.block2.forward(final_features, final_features, final_features)
        
        output_text = ""
        for i, out_vec in enumerate(layer2_out):
            token_id = sum(out_vec) % len(self.vocab)
            output_text += self.vocab.get(token_id, "?")
            
        print(f"  [Output] 纯整数推理结果: 【{output_text}】")
        return output_text

if __name__ == "__main__":
    print("=" * 60)
    print("☯️ Polaris 端到端微型纯整数 GPT (动态长度)")
    print("=" * 60)
    
    model = PolarisGPT()
    
    model.forward("天地玄黄")
    model.forward("宇宙")
    model.forward("日月")
