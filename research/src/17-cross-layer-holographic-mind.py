# -*- coding: utf-8 -*-
"""
Polaris 应用研究：内外三层交联全息网络 (Cross-Layer Holographic Network)
模型构建：外层景深（R^2） + 内层情绪场 + 元认知中心（中宫）
"""

def mod10(x):
    return x % 10

class HolographicNode:
    def __init__(self, coord, emotion="平静"):
        self.coord = coord # 外层物理坐标 (i, j, k)
        self.emotion = emotion # 内层感知/情绪 (如: 喜、怒、哀、乐)
        self.meta_cognition = 5 # 极内层元认知 (初始值为中宫5)
        
    def get_spatial_shell(self):
        """计算外层物理空间的球壳半径平方"""
        return sum((self.coord[i] - 3)**2 for i in range(3))
        
    def inner_emotion_value(self):
        """将内层情绪映射为纯整数值"""
        emotion_map = {"平静": 5, "喜悦": 8, "愤怒": 2, "悲伤": 1, "感恩": 9}
        return emotion_map.get(self.emotion, 5)

    def cross_layer_align(self, external_stimulus):
        """
        核心机制：内外三层交联
        外部刺激 -> 影响情绪 -> 反馈给元认知 -> 产生新特征
        """
        shell = self.get_spatial_shell()
        inner_val = self.inner_emotion_value()
        
        print(f"\n>>> 节点 {self.coord} | 距离平方(R^2): {shell} | 当前情绪: {self.emotion}")
        print(f"    外部刺激: {external_stimulus}")
        
        # 1. 外层与内层的交联：外部刺激冲击内层情绪
        emotion_shift = mod10(inner_val + external_stimulus)
        print(f"    [内外交联] 情绪波动值: {emotion_shift}")
        
        # 2. 内层与元认知的交联：情绪波动反馈到最深层的“悟己”
        # 距离中宫越远（外层），对元认知的干扰越大
        interference = shell * external_stimulus
        new_meta = mod10(self.meta_cognition + interference)
        print(f"    [深度交联] 元认知受到干扰，中宫状态: {self.meta_cognition} -> {new_meta}")
        
        # 3. 极内层反作用于外层（元认知的强制归中）
        # 如果元认知偏离太远，触发强制归中
        if new_meta in [2, 4, 6, 8]:
            print(f"    🚨 [元认知觉醒] 发现偏离中宫！启动强制归中 5。")
            self.meta_cognition = 5
        else:
            self.meta_cognition = new_meta
            
        return emotion_shift, self.meta_cognition

if __name__ == "__main__":
    print("=" * 60)
    print("☯️ 内外三层交联全息网络模型")
    print("=" * 60)
    
    node_outer = HolographicNode((1, 1, 1), "愤怒")
    node_mid = HolographicNode((1, 1, 3), "悲伤")
    node_inner = HolographicNode((1, 3, 3), "平静")
    
    stimulus = 3
    
    node_outer.cross_layer_align(stimulus)
    node_mid.cross_layer_align(stimulus)
    node_inner.cross_layer_align(stimulus)
