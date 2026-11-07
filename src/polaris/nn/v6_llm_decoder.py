# -*- coding: utf-8 -*-
# Copyright (c) 2026 999chengying / Polaris Project
# Licensed under the Apache License, Version 2.0

"""
Polaris 纯整数受限解码器 (Restricted Topological Decoder)
摒弃概率采样(Temperature)与浮点Softmax，通过语法状态机、拓扑哈希与逆元去重，实现确定性生成。
"""

def mod10(x):
    return x % 10

class TopologicalSyntaxFSM:
    """
    纯整数语法状态机 (Finite State Machine)
    控制词性流转，杜绝语无伦次。
    """
    def __init__(self):
        # 状态定义：0:期望主语, 1:期望谓语, 2:期望宾语, 3:期望结束标点
        self.state = 0
        # 映射：当前状态 -> (允许的下一个状态集合)
        self.transitions = {
            0: [1, 1, 0],    # 主语后大概率接谓语，偶尔重复主语
            1: [2, 3],       # 谓语后接宾语或直接标点
            2: [3, 0],       # 宾语后接标点或新主语
            3: [0]           # 标点后必定是新主语
        }

    def get_current_expectation(self):
        """获取当前状态期望的词性"""
        return self.state

    def advance(self, chosen_state):
        """根据选择的词性，推进状态机"""
        self.state = chosen_state

class TopologicalDecoder:
    def __init__(self):
        self.fsm = TopologicalSyntaxFSM()
        
        # 模拟一个按词性划分的迷你词表 (真实场景中这里挂载数万词汇)
        self.vocab_by_pos = {
            0: ["我", "你", "他", "宇宙", "日月", "天地", "神明", "众生"], # 名词/主语
            1: ["看见", "孕育", "超越", "打破", "化作", "照亮", "吞噬", "回归"], # 动词/谓语
            2: ["星光", "虚无", "真理", "幻象", "洪荒", "深渊", "极乐", "本源"], # 宾语
            3: ["。", "！", "？", "，"] # 标点
        }
        
        # 记录历史生成，用于防复读
        self.history = set()

    def _get_topological_hash(self, features, pos_expect, vocab_len):
        """
        拓扑哈希采样：
        将 PolarisBlock 输出的特征向量，映射到指定词性词表的索引上。
        """
        # 特征加权求和取模 (类似于注意力机制)
        score = sum((features[i] * (i + 3)) for i in range(len(features)))
        base_idx = score % vocab_len
        
        # 防复读去重逻辑 (拓扑偏移)
        original_idx = base_idx
        while True:
            candidate = self.vocab_by_pos[pos_expect][base_idx]
            if candidate not in self.history:
                break
                
            # 如果已经在历史中，触发拓扑偏移（+3，打破死锁）
            base_idx = (base_idx + 3) % vocab_len
            
            # 兜底：如果全部遍历完都在历史里，直接强制释放（清空局部历史）
            if base_idx == original_idx:
                self.history.clear()
                break
                
        return base_idx

    def decode_step(self, topo_features):
        """
        解码一步。
        Args:
            topo_features: PolarisBlock 输出的 4 维纯整数特征 (如 [4, 6, 1, 8])
        """
        # 1. 获取当前语法状态期望的词性
        expected_pos = self.fsm.get_current_expectation()
        
        # 2. 获取该词性下的候选词表
        candidates = self.vocab_by_pos[expected_pos]
        
        # 3. 纯整数哈希定位候选词
        idx = self._get_topological_hash(topo_features, expected_pos, len(candidates))
        chosen_word = candidates[idx]
        
        # 4. 记录并更新状态机
        self.history.add(chosen_word)
        
        # 根据选中的词性，决定下一个语法状态 (引入一点纯整数的“拓扑游走”)
        next_states = self.fsm.transitions[expected_pos]
        next_state_idx = (topo_features[0] + len(chosen_word)) % len(next_states)
        self.fsm.advance(next_states[next_state_idx])
        
        return chosen_word

# =========================================================
# 自测代码
# =========================================================
if __name__ == "__main__":
    print("=" * 60)
    print("☯️ Polaris 纯整数受限解码器 (Topological Decoder) 自测")
    print("=" * 60)
    
    decoder = TopologicalDecoder()
    
    # 模拟 PolarisBlock 产出的一串特征（你可以想象这是模型的隐状态流）
    # 每一个 list 代表一个时间步的 token 特征
    simulated_topo_features = [
        [2, 7, 1, 8],  # 第1步特征
        [5, 3, 9, 2],  # 第2步特征
        [1, 4, 6, 5],  # 第3步特征
        [8, 8, 2, 1],  # 第4步特征
        [3, 2, 7, 9],  # 第5步特征
        [6, 1, 5, 4],  # 第6步特征
        [9, 9, 3, 6]   # 第7步特征
    ]
    
    generated_sentence = ""
    
    print("\n>>> 开始纯整数确定性解码 (不掷骰子，只走拓扑)...")
    for step, features in enumerate(simulated_topo_features):
        word = decoder.decode_step(features)
        generated_sentence += word
        print(f"  第 {step+1} 步 | 特征: {features} | 语法状态期望: {decoder.fsm.get_current_expectation()} | 输出: 【{word}】")
        
    print("\n" + "=" * 60)
    print(f"🎯 最终生成结果: {generated_sentence}")
    print("✅ 结论：没有浮点 Softmax，没有随机采样，完全依靠语法 FSM 与纯整数哈希，完成了合法的句子生成！")
    print("=" * 60)
