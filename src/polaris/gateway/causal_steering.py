# -*- coding: utf-8 -*-
# Copyright (c) 2026 999chengying / Polaris Project
# Licensed under the Apache License, Version 2.0

"""
Polaris Causal Steering Gateway
纯整数拓扑大模型因果干预网关。
拦截大模型发散生成，实施拓扑极性诊断与因果重写。
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
        
        # 空间拓扑坐标映射
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

    def _get_hexagrams(self, text):
        """大模型判卦"""
        prompt = (
            "请将以下文本中的汉字转化为 6 位的二进制卦象编码（1为阳，0为阴）。\n"
            "严格只输出 '字:二进制' 的格式，用逗号分隔。\n"
            "文本：" + text
        )
        return self._call_llm(prompt, "你是精通易经的太极裁判。", temp=0.0)

    def diagnose(self, text):
        """核心诊断：返回中核状态（1-10）"""
        hex_str = self._get_hexagrams(text)
        pattern = r'([\u4e00-\u9fa5])\s*[:：]\s*([01]{6})'
        matches = re.findall(pattern, hex_str)
        
        if not matches:
            return 5 # 无法诊断时默认太极态

        cube = {c: 0 for c in itertools.product([1,3,5], repeat=3)}
        cube[(3, 3, 3)] = 5
        
        for char, bits in matches:
            val = 0
            for i in range(6):
                if bits[i] == '1': val += self.weights[i]
            val = self._mod10(val)
            
            index = sum(int(b) for b in bits[:3]) % 8
            coord = list(self.gua_to_vertex.keys())[index]
            cube[coord] = self._mod10(cube[coord] + val)
            
        # 拓扑干涉
        for coord, state in list(cube.items()):
            if coord != (3, 3, 3) and state != 0:
                cube[(3, 3, 3)] = self._mod10(cube[(3, 3, 3)] + self._mod10(state * 3))
                
        return cube[(3, 3, 3)]

    def generate_with_steering(self, topic, style="平衡"):
        """
        拦截式生成：
        1. 先自由生成。
        2. 测算拓扑极性。
        3. 若极性不符合预期，立刻施加因果干预，强制重写。
        """
        print("[Polaris] 正在请求原始生成...")
        ans1 = self._call_llm("请围绕以下主题写一段 100 字左右的文字：" + topic, "你是一个作家。")
        
        core = self.diagnose(ans1)
        print("[Polaris] 拓扑诊断中核状态: {}".format(core))
        
        # 判定极性 (偶数=感性发散, 奇数=理性收敛)
        is_even = core in [2, 4, 6, 8]
        
        need_rewrite = False
        steer_msg = ""
        
        if style == "发散" and not is_even:
            need_rewrite = True
            steer_msg = "【拓扑干预】刚才的生成逻辑过于死板。请释放想象力，使用充满情感、比喻和宏大意象的语言重新表述。"
        elif style == "收敛" and is_even:
            need_rewrite = True
            steer_msg = "【拓扑干预】刚才的生成逻辑过于发散。请立刻收敛情绪，使用更加务实、逻辑严密、条理清晰的语言重新表述。不要讲废话。"

        if need_rewrite:
            print("[Polaris] 触发因果干预，强制重写...")
            ans2 = self._call_llm("主题：" + topic + "\n原版：" + ans1 + "\n" + steer_msg, "你是一个听取指令修改的作家。")
            new_core = self.diagnose(ans2)
            print("[Polaris] 重写完毕。新中核状态: {}".format(new_core))
            return ans2
        else:
            print("[Polaris] 当前极性符合要求，安全放行。")
            return ans1
