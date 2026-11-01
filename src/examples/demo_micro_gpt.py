# -*- coding: utf-8 -*-
"""
Polaris V39: 纯整数 GPT 完整运行演示 (单文件测试版)
"""

from typing import List

# ================== 核心库：纯整数 Transformer ==================

class TopologicalPositionalEncoding:
    """纯整数位置编码（基于模10乘法群的 1, 3, 9, 7 循环）"""
    @staticmethod
    def encode(pos: int) -> int:
        cycle = [1, 3, 9, 7]
        return cycle[pos % 4]

class IntegerFFN:
    """纯整数前馈网络（Topological Feed-Forward Network）"""
    def __init__(self, d_model: int, d_ff: int):
        self.d_model = d_model
        self.d_ff = d_ff
        self.W1 = [[ (i + j + 3) % 10 for j in range(d_model)] for i in range(d_ff)]
        self.W2 = [[ (i * j + 7) % 10 for j in range(d_ff)] for i in range(d_model)]

    def forward(self, x: List[int]) -> List[int]:
        H = [0] * self.d_ff
        for i in range(self.d_ff):
            H[i] = sum(x[j] * self.W1[i][j] for j in range(self.d_model)) % 10
        H_act = [ (h * 3) % 10 if h > 5 else 0 for h in H ]
        O = [0] * self.d_model
        for i in range(self.d_model):
            O[i] = sum(H_act[j] * self.W2[i][j] for j in range(self.d_ff)) % 10
        return O

class TopologicalTransformerBlock:
    def __init__(self, seq_len: int, d_model: int):
        self.seq_len = seq_len
        self.d_model = d_model
        self.ffn = IntegerFFN(d_model, d_model * 2)
        self.pos_encoder = TopologicalPositionalEncoding()

    def forward(self, Q: List[List[int]], K: List[List[int]], V: List[List[int]]) -> List[List[int]]:
        for i in range(self.seq_len):
            pos_code = self.pos_encoder.encode(i)
            for d in range(self.d_model):
                Q[i][d] = (Q[i][d] + pos_code) % 10

        scores = [[0] * self.seq_len for _ in range(self.seq_len)]
        for i in range(self.seq_len):
            for j in range(self.seq_len):
                scores[i][j] = sum(Q[i][d] * K[j][d] for d in range(self.d_model)) % 10
                
        mask = [[0] * self.seq_len for _ in range(self.seq_len)]
        for i in range(self.seq_len):
            max_score = max(scores[i])
            for j in range(self.seq_len):
                if scores[i][j] == max_score:
                    mask[i][j] = 1
                    
        attn_out = [[0] * self.d_model for _ in range(self.seq_len)]
        for i in range(self.seq_len):
            for d in range(self.d_model):
                val = sum(V[j][d] + j for j in range(self.seq_len) if mask[i][j] == 1)
                attn_out[i][d] = val % 10
                
        final_out = []
        for i in range(self.seq_len):
            final_out.append(self.ffn.forward(attn_out[i]))
        return final_out

# ================== 演示代码：微型 GPT 生成 ==================

import random

def run_micro_gpt():
    print("=" * 60)
    print("☯️ Polaris 微型纯整数 GPT (自回归生成演示)")
    print("=" * 60)
    
    vocab = {i: char for i, char in enumerate("天地玄黄宇宙洪荒日月")}
    reverse_vocab = {char: i for i, char in vocab.items()}
    
    d_model = 4  
    seq_len = 4  
    layers = 2   
    
    gpt_blocks = [TopologicalTransformerBlock(seq_len=seq_len, d_model=d_model) for _ in range(layers)]
    
    def output_head(features: list) -> int:
        return sum(features) % 10

    prompt_text = "天地玄黄"
    print(f"\n[输入 Prompt] : {prompt_text}")
    
    input_ids = [reverse_vocab[c] for c in prompt_text]
    while len(input_ids) < seq_len:
        input_ids.insert(0, 0)
        
    generated_text = prompt_text
    
    print("\n[开始自回归生成...]")
    for step in range(8):
        Q = [[(input_ids[i] + step) % 10 for _ in range(d_model)] for i in range(seq_len)]
        K = [[(input_ids[i] * 3) % 10 for _ in range(d_model)] for i in range(seq_len)]
        V = [[(input_ids[i] * 7) % 10 for _ in range(d_model)] for i in range(seq_len)]
        
        hidden_states = Q
        for block in gpt_blocks:
            hidden_states = block.forward(hidden_states, K, V)
            
        last_token_features = hidden_states[-1]
        next_token_id = output_head(last_token_features)
        
        next_char = vocab[next_token_id]
        generated_text += next_char
        print(f"  步 {step+1:02d} | 预测 ID: {next_token_id} | 生成字符: 【{next_char}】")
        
        input_ids.append(next_token_id)
        if len(input_ids) > seq_len:
            input_ids.pop(0)

    print("\n" + "=" * 60)
    print(f"🎯 最终生成的文本: {generated_text}")
    print("✅ 结论：全程零浮点、零 PyTorch，纯整数 GPT 运行成功！")
    print("=" * 60)

if __name__ == "__main__":
    random.seed(42)
    run_micro_gpt()
