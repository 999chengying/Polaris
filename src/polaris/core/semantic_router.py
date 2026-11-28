# -*- coding: utf-8 -*-
# Copyright (c) 2026 999chengying / Polaris Project
# Licensed under the Apache License, Version 2.0

"""
Polaris 语义拓扑路由引擎 (Semantic Router Engine)
基于“体用关系”与“历史 Context”，动态计算实体在场景中的绝对极性。
消除大模型哈希映射造成的语义扁平化。
"""

class SemanticRouter:
    def __init__(self):
        # 预设各系的基础立方体（此处以二组甲-乾系为例，提供默认映射基准）
        # 实际工程中，应无缝接入 topology_math 的坐标体系
        self.cube_乾_甲 = {
            (1,1,1): 9, (5,5,5): 1, (5,5,1): 6, (1,1,5): 4,
            (1,5,1): 3, (5,1,5): 7, (5,1,1): 2, (1,5,5): 8
        }

    def calculate_context_bias(self, history_text=""):
        """
        历史偏置 (History Context Bias)
        用于分析长文本背景。极端狂热/暴力的语境会提高偏置值。
        实际应用中，此处应调用大模型进行“两两比较”提取极性。
        """
        if not history_text:
            return 0
            
        extreme_words = ["复仇", "杀", "血", "狂", "末日", "毁灭", "必死"]
        hits = sum(1 for word in extreme_words if word in history_text)
        
        # 命中词汇越多，偏置越高，上限为 3
        return min(hits * 1, 3)

    def calculate_scene_bias(self, current_entity, other_entities=""):
        """
        场景相对偏置 (Scene Relative Bias)
        “体用关系”：当弱势实体出现时，主体会产生保护欲，激发乾(君王)/坤(母亲)属性。
        """
        if not other_entities:
            return 0
            
        weak_entities = ["小白兔", "婴儿", "伤者", "小猫", "幼童", "弱者"]
        strong_entities = ["猛虎", "恶魔", "仇人", "大军"]
        
        bias = 0
        # 相对弱势，激发主体阳性能量
        if any(entity in other_entities for entity in weak_entities):
            bias += 4
            
        # 相对强势，压制主体阳性能量（从侧面激发潜藏的力量或退让）
        if any(entity in other_entities for entity in strong_entities):
            bias -= 1 
            
        return bias

    def extract_hexagram(self, current_entity, other_entities="", history_text=""):
        """
        核心算法：根据综合偏置场，动态生成三爻卦象。
        返回：卦象字符串 (如 '111', '000') 和 综合偏置值
        """
        ctx_bias = self.calculate_context_bias(history_text)
        scene_bias = self.calculate_scene_bias(current_entity, other_entities)
        total_bias = ctx_bias + scene_bias
        
        # 默认极性（以少女为例，本应是兑卦，阴柔为 000）
        x_bin, z_bin, y_bin = "0", "0", "0"
        
        # 动态极性推演
        if total_bias >= 4:
            x_bin, z_bin, y_bin = "1", "1", "1" # 极阳极刚（如：复仇女帝/护崽母亲）
        elif total_bias >= 1:
            x_bin, z_bin, y_bin = "0", "1", "0" # 外柔内刚（如：坤之厚德）
        elif total_bias <= -3:
            x_bin, z_bin, y_bin = "0", "0", "1" # 极阴且面临威胁（如：退避）
            
        return x_bin + z_bin + y_bin, total_bias

    def route(self, current_entity, other_entities="", history_text=""):
        """
        一站式接口：输入实体与场景，输出其注入的立方体坐标与数值。
        """
        hexagram, bias = self.extract_hexagram(current_entity, other_entities, history_text)
        
        # 将二进制转换为坐标 (1为阳坐标取1，0为阴坐标取5)
        x_coord = 1 if hexagram[0] == "1" else 5
        z_coord = 1 if hexagram[1] == "1" else 5
        y_coord = 1 if hexagram[2] == "1" else 5
        
        target_coord = (x_coord, y_coord, z_coord)
        
        # 获取该坐标在基准立方体中的物理数值
        inject_value = self.cube_乾_甲.get(target_coord, 5)
        
        return {
            "entity": current_entity,
            "context_bias": bias,
            "hexagram": hexagram,
            "coord": target_coord,
            "inject_value": inject_value
        }
