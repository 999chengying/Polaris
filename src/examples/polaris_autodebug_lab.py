# -*- coding: utf-8 -*-
# Copyright (c) 2026 999chengying / Polaris Project
# Licensed under the Apache License, Version 2.0

"""
Polaris: 生克群议与中宫仲裁 Debug 实验室 (F/S 统计版)
严格遵循 12341 循环与 67896 审计匹配，实现多数决与平局仲裁。
"""

import os
import time
import requests

USE_REAL_API = True 
API_KEY = os.environ.get("DEEPSEEK_API_KEY")
API_URL = "https://api.deepseek.com/chat/completions"

class LabAgent:
    def __init__(self, gua_num, role):
        self.gua_num = gua_num
        self.role = role 

    def call_llm(self, prompt):
        if not USE_REAL_API or not API_KEY:
            # 本地模拟大模型，让 1、2、3 号产生不同的逻辑，模拟真实的 F/S
            if "加密" in prompt:
                return "def encrypt(pt, k):\n    return [(x + k) % 10 for x in pt]"
            if "解密" in prompt:
                return "def decrypt(ct, k):\n    return [(x - k) % 10 for x in ct]"
            if "测试" in prompt:
                return "def run_test():\n    pt = [1, 2, 3, 4]\n    ct = encrypt(pt, 5)\n    assert decrypt(ct, 5) == pt\n    print('PASS')"
            return "pass"

        headers = {"Authorization": "Bearer " + str(API_KEY), "Content-Type": "application/json"}
        data = {"model": "deepseek-chat", "messages": [{"role": "user", "content": prompt}], "temperature": 0.3}
        try:
            r = requests.post(API_URL, headers=headers, json=data, timeout=30)
            return r.json()["choices"][0]["message"]["content"].strip().replace("```python", "").replace("```", "").strip()
        except:
            return "pass"

    def produce_code(self, instruction, is_leader=False):
        prefix = "[总指挥介入] " if is_leader else ""
        print(f"  ⚒️ {prefix}[{self.gua_num}号 生产] 正在编写代码...")
        prompt = f"你是资深程序员。请实现：{instruction}。只输出纯Python代码，不要任何解释和Markdown格式。"
        return self.call_llm(prompt)

    def audit_code(self, enc_code, dec_code):
        print(f"  🔍 [审计-{self.gua_num}号] 正在生成测试用例并执行...")
        prompt = f"你是测试员。编写测试函数 run_test()。明文[1,2,3,4]，密钥5。调用加解密，如果成功print('PASS')，失败raise Exception。只输出纯Python代码。"
        test_code = self.call_llm(prompt)
        
        # 系统执行审计
        full_script = f"{enc_code}\n\n{dec_code}\n\n{test_code}\n\ntry:\n    run_test()\nexcept Exception as e:\n    raise e"
        try:
            exec(full_script, globals())
            return "S", full_script
        except Exception as e:
            return "F", str(e)

class PolarisCouncilLab:
    def __init__(self):
        # 初始阵法：12341 生，67896 审
        self.current_cycle = [1, 2, 3, 4, 1]
        self.agents = {i: LabAgent(i, "生") for i in range(1, 5)}
        self.agents.update({i: LabAgent(i, "成") for i in range(6, 10)})
        
        self.instruction_enc = "基于纯整数模10的加密函数 encrypt(plaintext: list, key: int) -> list"
        self.instruction_dec = "基于纯整数模10的解密函数 decrypt(ciphertext: list, key: int) -> list"
        
        self.f_count = 0
        self.s_count = 0
        self.success_script = None

    def run_round(self, workers, auditors, is_leader_round=False):
        """执行一轮 F/S 审计"""
        for i in range(len(workers) - 1):
            w_id = workers[i]
            a_id = auditors[i]
            
            print(f"\n--- [对阵: {w_id}号(产) VS {a_id}号(审)] ---")
            enc = self.agents[w_id].produce_code(self.instruction_enc, is_leader=is_leader_round)
            dec = self.agents[w_id].produce_code(self.instruction_dec, is_leader=is_leader_round)
            
            result, detail = self.agents[a_id].audit_code(enc, dec)
            
            if result == "S":
                self.s_count += 1
                print(f"  ✅ 审计通过！标记为 S")
                if not self.success_script:
                    self.success_script = detail # 保留第一次成功的结果
            else:
                self.f_count += 1
                print(f"  ❌ 审计未通过！标记为 F | 原因: {detail[:40]}...")

    def start_council(self):
        print("=" * 60)
        print("🏛️ Polaris 群议推举 Debug 实验室启动")
        print("=" * 60)
        
        while True:
            self.f_count = 0
            self.s_count = 0
            self.success_script = None
            
            print("\n[第一轮基层投票] 生数 1, 2, 3 轮流生产，成数 6, 7, 8 审计：")
            self.run_round(self.current_cycle[:3], [6, 7, 8])
            
            print(f"\n📊 [第一阶段战报] S(成功): {self.s_count} | F(失败): {self.f_count}")
            
            if self.s_count > self.f_count:
                print("🏆 [数理决议] S 大于 F，基层方案通过！")
                break
            
            print("\n[第二轮总指挥介入] 4号领导生产，9号审计：")
            self.run_round([4], [9], is_leader_round=True)
            
            print(f"\n📊 [最终计票] S(成功): {self.s_count} | F(失败): {self.f_count}")
            
            if self.s_count > self.f_count:
                print("🏆 [数理决议] 领导介入后，S 大于 F，方案通过！")
                break
            
            # 平局或失败多于成功，触发中宫仲裁
            print("\n🚨 [平局/败局] 触发中宫 5 号仲裁！")
            self.mid_palace_arbitration()

        print("\n✅ [最终定稿代码执行验证]")
        try:
            exec(self.success_script, globals())
            print("代码完美运行，本次群议圆满结束！")
        except Exception as e:
            print(f"最终运行仍报错: {e}")

    def mid_palace_arbitration(self):
        """中宫 5 号的三大仲裁法则"""
        print("👑 [中宫 5 宣告] 根据《中宫仲裁律》，我不直接干涉代码，只做宏观裁决！")
        print("  选择策略 (一)：将生产与审计组功能对换。")
        print("  选择策略 (二)：另选一种推理逻辑数列。")
        
        # 简单演示：我们选择策略二，换一种推理逻辑，比如用 94389 替代 12341
        print("\n🔄 [拓扑换阵] 将阵法从 [1,2,3,4,1] 替换为 [9,4,3,8,9]！")
        self.current_cycle = [9, 4, 3, 8, 9]
        
        # 换阵后，让原来的 9 号去生产，4号、3号等去审计（示意）
        print("  新的生产队伍已就位，重新开始投票...")
        # 这里为了代码简洁，仅作变量替换提示，不实际改角色实例

if __name__ == "__main__":
    if not API_KEY:
        print("⚠️ 未检测到 API KEY，进入本地 Mock 模式演示。\n")
        USE_REAL_API = False
        
    lab = PolarisCouncilLab()
    lab.start_council()
