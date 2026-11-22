# -*- coding: utf-8 -*-
# Copyright (c) 2026 999chengying / Polaris Project
# Licensed under the Apache License, Version 2.0

"""
Polaris Causal Steering Gateway (V2.0 时空全息版)
引入朱熹“本卦、互卦、之卦”体系，实现 18位（18-bit）三维拓扑干涉。
"""

import os
import requests
import re
import itertools

class PolarisCausalSteering:
    def __init__(self, api_key=None, model="deepseek-chat"):
        self.api_key = api_key or os.environ.get("DEEPSEEK_API_KEY")
        self.api_url = "https://api.deepseek.com/chat/completions"
        self.model = model
        
        # 27宫物理坐标映射
        self.gua_to_vertex = {
            (1,1,1): 9, (5,5,1): 1, (1,5,5): 8, (5,1,5): 2,
            (1,1,5): 7, (5,5,5): 3, (1,5,1): 6, (5,1,1): 4
        }
        self.weights = [3, 5, 7, 11, 13, 17]

    def _mod10(self, x):
        return x % 10 or 10

    def _call_llm(self, prompt, system_msg="你是AI助手", temp=0.7):
        headers = {"Authorization": "Bearer " + str(self.api_key), "Content-Type": "application/json"}
        messages = [{"role": "system", "content": system_msg}, {"role": "user", "content": prompt}]
        data = {"model": self.model, "messages": messages, "temperature": temp}
        try:
            r = requests.post(self.api_url, headers=headers, json=data, timeout=30)
            return r.json()["choices"][0]["message"]["content"].strip()
        except Exception as e:
            return "[API Error] " + str(e)

    def _get_trinity_hexagrams(self, text):
        """大模型三卦齐发：提取本卦、互卦、之卦"""
        prompt = (
            "你是一个精通易经的太极裁判。请将以下文本中的关键汉字，根据其语境意象，"
            "同时给出它的 本卦(当前表象)、互卦(内在结构)、之卦(未来发展) 的 6 位二进制编码。\n"
            "格式要求：字:本卦二进制,互卦二进制,之卦二进制\n"
            "例如：天:111111,101010,111000\n"
            "文本：" + text
        )
        return self._call_llm(prompt, "你是太极裁判。", temp=0.0)

    def diagnose(self, text):
        """核心诊断：18位三维全息干涉，返回中核状态（1-10）"""
        hex_str = self._get_trinity_hexagrams(text)
        # 解析正则
        pattern = r'([\u4e00-\u9fa5])\s*[:：]\s*([01]{6}),([01]{6}),([01]{6})'
        matches = re.findall(pattern, hex_str)
        
        if not matches:
            return 5, "无法提取有效全息卦象"

        cube = {c: 0 for c in itertools.product([1,3,5], repeat=3)}
        cube[(3, 3, 3)] = 5
        
        for char, ben_bits, hu_bits, zhi_bits in matches:
            # 1. 计算三维能量
            val_ben = sum(self.weights[i] for i in range(6) if ben_bits[i] == '1')
            val_hu = sum(self.weights[i] for i in range(6) if hu_bits[i] == '1')
            val_zhi = sum(self.weights[i] for i in range(6) if zhi_bits[i] == '1')
            
            # 2. 定位三维坐标 (X本, Y互, Z之)
            x_idx = sum(int(b) for b in ben_bits[:2]) % 3
            y_idx = sum(int(b) for b in hu_bits[:2]) % 3
            z_idx = sum(int(b) for b in zhi_bits[:2]) % 3
            
            coords_xyz = [1, 3, 5]
            coord = (coords_xyz[x_idx], coords_xyz[y_idx], coords_xyz[z_idx])
            
            # 3. 能量注入
            energy = self._mod10(val_ben + val_hu + val_zhi)
            cube[coord] = self._mod10(cube[coord] + energy)
            
        # 4. 空间大干涉
        for coord, state in list(cube.items()):
            if coord != (3, 3, 3) and state != 0:
                cube[(3, 3, 3)] = self._mod10(cube[(3, 3, 3)] + self._mod10(state * 3))
                
        final_core = cube[(3, 3, 3)]
        return final_core, "全息干涉完成"

    def generate_with_steering(self, topic, style="平衡"):
        print("[Polaris] 请求原始生成...")
        ans1 = self._call_llm("请围绕以下主题写一段 100 字左右的文字：" + topic, "你是一个作家。")
        
        core, msg = self.diagnose(ans1)
        print("[Polaris] 18位时空全息诊断中核: {}".format(core))
        
        is_even = core in [2, 4, 6, 8]
        need_rewrite = False
        steer_msg = ""
        
        if style == "发散" and not is_even:
            need_rewrite = True
            steer_msg = "【拓扑干预】刚才生成过于死板。请释放想象力，使用充满情感、比喻和宏大意象的语言重新表述。"
        elif style == "收敛" and is_even:
            need_rewrite = True
            steer_msg = "【拓扑干预】刚才生成过于发散。请立刻收敛情绪，使用更加务实、逻辑严密、条理清晰的语言重新表述。"

        if need_rewrite:
            print("[Polaris] 触发因果干预，强制重写...")
            ans2 = self._call_llm("主题：" + topic + "\n原版：" + ans1 + "\n" + steer_msg, "你是一个听取指令修改的作家。")
            new_core, _ = self.diagnose(ans2)
            print("[Polaris] 重写完毕。新中核: {}".format(new_core))
            return ans2
        else:
            print("[Polaris] 当前极性符合要求，安全放行。")
            return ans1
