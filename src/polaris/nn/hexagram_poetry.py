# -*- coding: utf-8 -*-
# Copyright (c) 2026 999chengying / Polaris Project
# Licensed under the Apache License, Version 2.0

"""
Polaris Hexagram Poetry Engine
基于六爻情景交联与元认知炼丹炉的纯整数诗境生成模块。
"""

import random
from typing import List, Dict, Optional

class HexagramPoetryEngine:
    """
    六爻情景交联与炼丹还虚引擎。
    1. 将内三爻（景深）与外三爻（情深）交联，生成五言绝句。
    2. 将诗词通过 1/7/9 算子炼化，凝聚金丹。
    3. 将金丹化为高维哲学结句。
    """
    
    def __init__(self, seed: int = 888):
        self.seed = seed
        
        self.scenery: Dict[str, Dict[int, List[str]]] = {
            "秋": {1: ["叶", "苔", "窗", "烛", "露", "阶"], 2: ["竹", "林", "舟", "岸", "桥", "寺"], 3: ["山", "江", "云", "天", "海", "星"]},
            "春": {1: ["花", "草", "燕", "泥", "枝", "院"], 2: ["柳", "堤", "风", "雨", "楼", "径"], 3: ["野", "春", "原", "光", "峦", "空"]},
            "雪": {1: ["窗", "梅", "雪", "炉", "檐", "庭"], 2: ["径", "松", "亭", "岭", "崖", "林"], 3: ["莽", "冰", "极", "天", "原", "夜"]},
            "夜": {1: ["灯", "帐", "床", "影", "帘", "香"], 2: ["月", "江", "渡", "鸦", "街", "钟"], 3: ["冥", "极", "太", "虚", "星", "穹"]},
            "山": {1: ["石", "苔", "阶", "洞", "泉", "藤"], 2: ["松", "岭", "崖", "寺", "云", "鹤"], 3: ["峰", "极", "天", "浩", "渺", "苍"]},
            "江": {1: ["岸", "沙", "舟", "帆", "浪", "柳"], 2: ["渡", "桥", "潮", "雨", "风", "客"], 3: ["海", "天", "际", "无", "穷", "阔"]},
            "风": {1: ["窗", "帘", "叶", "尘", "袖", "鬓"], 2: ["林", "崖", "浪", "原", "疾", "微"], 3: ["穹", "极", "浩", "荡", "虚", "空"]},
            "离别": {1: ["泪", "酒", "杯", "手", "衣", "马"], 2: ["长", "亭", "渡", "柳", "路", "客"], 3: ["天", "涯", "极", "渺", "空", "绝"]},
            "悟道": {1: ["心", "念", "尘", "镜", "台", "骨"], 2: ["空", "禅", "虚", "幻", "梦", "影"], 3: ["极", "无", "太", "真", "本", "源"]}
        }
        
        self.emotion: Dict[str, Dict[int, List[str]]] = {
            "秋": {4: ["幽", "静", "闲", "微", "冷", "轻"], 5: ["愁", "思", "悲", "望", "孤", "寒"], 6: ["空", "寂", "悟", "绝", "虚", "灭"]},
            "春": {4: ["暖", "新", "轻", "醉", "微", "柔"], 5: ["狂", "叹", "喜", "恋", "盼", "迷"], 6: ["生", "荣", "释", "化", "同", "初"]},
            "雪": {4: ["寒", "洁", "寂", "冷", "凉", "清"], 5: ["孤", "绝", "傲", "叹", "凛", "凄"], 6: ["白", "空", "融", "虚", "净", "无"]},
            "夜": {4: ["静", "深", "幽", "暗", "寂", "沉"], 5: ["孤", "叹", "愁", "恐", "惘", "迷"], 6: ["冥", "空", "彻", "破", "虚", "无"]},
            "山": {4: ["隐", "远", "险", "静", "苍", "翠"], 5: ["高", "雄", "孤", "叹", "绝", "冷"], 6: ["极", "空", "化", "同", "归", "虚"]},
            "江": {4: ["浩", "渺", "长", "流", "平", "远"], 5: ["宽", "涌", "激", "荡", "悲", "叹"], 6: ["穷", "空", "际", "彻", "融", "无"]},
            "风": {4: ["微", "轻", "凉", "拂", "急", "狂"], 5: ["散", "断", "卷", "破", "残", "送"], 6: ["空", "尽", "虚", "灭", "同", "归"]},
            "离别": {4: ["伤", "愁", "叹", "微", "苦", "泪"], 5: ["痛", "悲", "绝", "恨", "寂", "留"], 6: ["空", "释", "悟", "化", "同", "虚"]},
            "悟道": {4: ["清", "静", "明", "寂", "微", "照"], 5: ["彻", "透", "空", "虚", "破", "绝"], 6: ["真", "如", "极", "本", "无", "化"]}
        }
        
        self.meta_vocab: Dict[str, List[str]] = {
            "空灵": ["空", "无", "虚", "极", "玄", "幽", "静", "灭"],
            "融合": ["同", "一", "融", "化", "合", "真", "道", "如"],
            "主体": ["我", "心", "意", "念", "神", "元", "灵", "本"],
            "宏观": ["万", "千", "众", "世", "劫", "古", "今", "因", "果"],
            "动词": ["归", "入", "见", "破", "生", "落", "隐", "彻", "转"]
        }
        
        self.verbs: List[str] = ["落", "飞", "流", "去", "来", "入", "涌", "生", "照", "掩", "过", "寻", "抱", "染", "破", "化", "尽"]
        self.ping_set = set(list("天寒云江风空山春深林清微幽松舟桥庭帆孤苍茫高川星原花枝风春庭无虚无空真明"))
        self.patterns = [
            [1, 1, 0, 0, 1],
            [0, 0, 1, 1, 0],
            [0, 0, 0, 1, 1],
            [1, 1, 1, 0, 0]
        ]

    def _pseudo_random(self, max_val: int) -> int:
        self.seed = (self.seed * 1103515245 + 12345) % 2147483648
        return self.seed % max_val

    def _get_ping_ze(self, char: str) -> int:
        return 0 if char in self.ping_set else 1

    def _get_rhyme(self, word: str) -> int:
        """支持单字或双字词"""
        return sum(ord(c) for c in word) % 6

    def _pick_word(self, pool: List[str], target_pz: int, used: set, target_rhyme: Optional[int] = None) -> str:
        valid = [w for w in pool if self._get_ping_ze(w) == target_pz and w not in used]
        if target_rhyme is not None:
            rhyme_valid = [w for w in valid if self._get_rhyme(w) == target_rhyme]
            if rhyme_valid: valid = rhyme_valid
        if not valid: valid = pool
        
        word = valid[self._pseudo_random(len(valid))]
        used.add(word)
        return word

    def generate(self, topic: str) -> Dict[str, Any]:
        """
        生成六爻诗并炼化结句。
        
        Returns:
            包含前调诗句、金丹状态与元认知结句的字典
        """
        poem = []
        used = set()
        target_rhyme = self._get_rhyme(topic)
        
        sc = self.scenery.get(topic, self.scenery["秋"])
        em = self.emotion.get(topic, self.emotion["秋"])
        
        hexagram_matrix = [
            [(sc[1]), (em[4]), (self.verbs), (sc[1]), (em[4])],
            [(sc[2]), (em[5]), (self.verbs), (sc[2]), (em[5])],
            [(sc[3]), (em[6]), (self.verbs), (sc[3]), (em[6])],
            [(sc[3]), (em[6]), (self.verbs), (sc[1]), (em[4])] 
        ]

        for i in range(4):
            line_chars = []
            is_rhyme = (i in [1, 3])
            for j in range(5):
                target_pz = self.patterns[i][j]
                pool = hexagram_matrix[i][j]
                rhyme_req = target_rhyme if (j == 4 and is_rhyme) else None
                word = self._pick_word(pool, target_pz, used, rhyme_req)
                line_chars.append(word)
            poem.append("".join(line_chars))
            
        # 炼丹
        final_dan = self._alchemy(poem)
        # 化诗
        meta_couplet = self._generate_meta_couplet(final_dan)
        
        return {
            "topic": topic,
            "poem": poem,
            "dan_state": final_dan,
            "meta_couplet": meta_couplet
        }
        
    def _alchemy(self, poem_lines: List[str]) -> int:
        """元认知炼丹炉"""
        state_vec = [sum(ord(c) for c in line) % 10 for line in poem_lines]
        refined_vec = [ (s * (1 if i==0 else (7 if i in [1,2] else 9))) % 10 for i, s in enumerate(state_vec)]
        return sum(refined_vec) % 10

    def _generate_meta_couplet(self, dan_state: int) -> str:
        random.seed(dan_state * 88)
        
        if dan_state % 2 == 0:
            line1 = f"{random.choice(self.meta_vocab['宏观'])}{random.choice(self.meta_vocab['动词'])}{random.choice(self.meta_vocab['主体'])}{random.choice(self.meta_vocab['空灵'])}{random.choice(self.meta_vocab['空灵'])}"
            line2 = f"{random.choice(self.meta_vocab['主体'])}{random.choice(self.meta_vocab['动词'])}{random.choice(self.meta_vocab['宏观'])}{random.choice(self.meta_vocab['融合'])}{random.choice(self.meta_vocab['空灵'])}"
        else:
            line1 = f"{random.choice(self.meta_vocab['主体'])}{random.choice(self.meta_vocab['动词'])}{random.choice(self.meta_vocab['宏观'])}{random.choice(self.meta_vocab['融合'])}"
            line2 = f"{random.choice(self.meta_vocab['宏观'])}{random.choice(self.meta_vocab['动词'])}{random.choice(self.meta_vocab['空灵'])}{random.choice(self.meta_vocab['空灵'])}"
                    
        if len(line1) > 5: line1 = line1[:5]
        if len(line2) > 5: line2 = line2[:5]
        while len(line1) < 5: line1 += random.choice(self.meta_vocab['空灵'])
        while len(line2) < 5: line2 += random.choice(self.meta_vocab['融合'])

        return f"{line1}，{line2}。"
