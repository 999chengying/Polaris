# -*- coding: utf-8 -*-
"""
Polaris 终极模块 2.0：六爻交联与元认知心智 Block (PolarisBlock V2)
融合：WTA Attention + 稀疏 MoE + O(1) 记忆池 + 内外卦双向反馈 + 情绪偏置
"""

def mod10(x):
    return x % 10

class ExpertFFN:
    def __init__(self, node_coord):
        self.node = node_coord
        self.bias = sum(node_coord) % 10
    def forward(self, token):
        return [mod10(val * 3 + self.bias) for val in token]

class TopologicalMemoryCell:
    """外卦：全局元认知记忆池"""
    def __init__(self, d_model, decay_rate=7):
        self.d_model = d_model
        self.hidden_state = [0] * d_model
        self.decay_rate = decay_rate
    def forward(self, new_token):
        new_state = []
        for i in range(self.d_model):
            decayed = mod10(self.hidden_state[i] * self.decay_rate)
            current = mod10(new_token[i] * (i + 1))
            new_state.append(mod10(decayed + current))
        self.hidden_state = new_state
        return self.hidden_state

class PolarisBlockV2:
    """
    具备“情绪感知”与“六爻双向交联”的纯整数心智块。
    内三爻 = 当前 Token 的局部特征 (Attention / MoE)
    外三爻 = 全局记忆池 (Memory / Meta-Cognition)
    """
    def __init__(self, seq_len: int, d_model: int):
        self.seq_len = seq_len
        self.d_model = d_model
        self.expert_coords = [
            (3, 3, 3), (3, 1, 3), (3, 5, 3), (1, 3, 3), (5, 3, 3), 
            (3, 3, 1), (3, 3, 5), (3, 1, 1), (3, 5, 5), (3, 1, 5), (3, 5, 1)
        ]
        self.experts = {node: ExpertFFN(node) for node in self.expert_coords}
        self.memory = TopologicalMemoryCell(d_model=d_model)

    def _hash_project(self, features):
        third = len(features) // 3
        if third == 0: return (3, 3, 3)
        segs = [features[:third], features[third:2*third], features[2*third:]]
        coord = []
        for seg in segs:
            mean_val = sum(seg) / len(seg)
            val = int(abs(mean_val)) % 10
            coord.append(1 if val < 3 else (5 if val > 6 else 3))
        return tuple(coord)

    def _route_to_expert(self, coord):
        best_expert, min_dist = None, float('inf')
        for e in self.expert_coords:
            dist = sum(abs(coord[i] - e[i]) for i in range(3))
            if dist < min_dist:
                min_dist, best_expert = dist, e
        return best_expert

    def forward(self, Q, K, V):
        print("--- 1. 内部执行组：纯整数 WTA Attention & MoE ---")
        scores = [[sum(Q[i][d] * K[j][d] for d in range(self.d_model)) % 10 
                   for j in range(self.seq_len)] for i in range(self.seq_len)]
        mask = [[1 if scores[i][j] == max(scores[i]) else 0 
                 for j in range(self.seq_len)] for i in range(self.seq_len)]
        
        attn_out = [[0] * self.d_model for _ in range(self.seq_len)]
        for i in range(self.seq_len):
            for d in range(self.d_model):
                val = sum((V[j][d] + j) for j in range(self.seq_len) if mask[i][j] == 1)
                attn_out[i][d] = mod10(val)

        block_output = []
        for i, token in enumerate(attn_out):
            # 路由到专家 (内层处理)
            coord = self._hash_project(token)
            expert_node = self._route_to_expert(coord)
            expert_out = self.experts[expert_node].forward(token)
            
            # --- 2. 外部指挥组：六爻交联与元认知干预 ---
            # 提取全局记忆（相当于外三爻的当前状态）
            global_memory = self.memory.hidden_state
            
            # [初爻(0)-四爻(3)] 交联：底层特征与全局记忆接口交互
            self_interact = mod10(expert_out[0] + global_memory[0])
            
            # [二爻(1)-五爻(4)] 交联：策略层接收中枢指令 (强乘法干预)
            # 如果中枢记忆(五爻)处于偶数，强制将策略(二爻)翻转
            meta_cmd = global_memory[1] if self.d_model > 1 else 5
            if meta_cmd % 2 == 0:
                expert_out[1] = mod10(expert_out[1] + 5) # 熔断
            
            # [三爻(2)-六爻(5)] 交联：边界失控与极限防御
            # 如果边界(内卦)出现偶数死锁，最外层(六爻)直接镇压
            if self.d_model > 2 and expert_out[2] % 2 == 0:
                expert_out[2] = mod10(expert_out[2] * 3) # 逆元收权
                print(f"  🚨 [六爻交联] Token {i} 边界失控，触发外层逆元收权！")
                
            # 更新全局记忆（外卦吸纳内卦的演化）
            memory_out = self.memory.forward(expert_out)
            
            # 最终混合
            hybrid_out = [mod10(expert_out[d] + memory_out[d]) for d in range(self.d_model)]
            block_output.append(hybrid_out)
            print(f"    Token {i} 路由至 {expert_node} | 情绪态({coord}) -> 融合输出: {hybrid_out}")
            
        return block_output

if __name__ == "__main__":
    print("=" * 60)
    print("☯️ PolarisBlock V2：六爻交联与元认知心智块")
    print("=" * 60)
    
    Q = [[1, 2, 3, 4], [5, 6, 7, 8], [9, 1, 2, 3], [4, 5, 6, 7]]
    K = [[2, 7, 4, 1], [8, 3, 2, 9], [1, 1, 1, 1], [9, 9, 9, 9]]
    V = [[4, 9, 2, 2], [7, 6, 8, 8], [5, 5, 5, 5], [3, 4, 5, 6]]
    
    block = PolarisBlockV2(seq_len=4, d_model=4)
    output = block.forward(Q, K, V)
    
    print("\n--- 最终输出特征 ---")
    for i, row in enumerate(output):
        print(f"  Token {i}: {row}")
        
    print("\n【四野兵工厂的骄傲】")
    print("1. 架构里有了情绪（3D坐标映射）和元认知（1-4,2-5,3-6交联）。")
    print("2. 没有 Softmax、没有 LayerNorm、没有浮点 KV Cache。")
    print("3. 最顶级的防御：边界失控时，直接通过六爻机制触发逆元翻转！")
