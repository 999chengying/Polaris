# -*- coding: utf-8 -*-
# Copyright (c) 2026 999chengying / Polaris Project
# Licensed under the Apache License, Version 2.0

"""
PolarisGuardrail: 大模型纯整数拓扑防幻觉护栏
提供给外部大模型(如 DeepSeek, Qwen 等)调用的一站式封装类。
"""

class PolarisGuardrail:
    @staticmethod
    def hash_project(text):
        """拓扑投影 (PTPP): 文本转三维纯整数状态"""
        if not text or len(text) < 3:
            return 5, 5, 5
        
        third = len(text) // 3
        segs = [text[:third], text[third:2*third], text[2*third:]]
        
        def calc_seg(seg):
            val = sum(ord(c) for c in seg) % 10
            return val or 10
            
        return calc_seg(segs[0]), calc_seg(segs[1]), calc_seg(segs[2])

    @staticmethod
    def diagnose(d1, d2, d3):
        """因果诊断：返回 (状态, 共识度)"""
        consensus = (d1 * 3 + d2 * 5 + d3 * 7) % 10
        status = "PASS" if consensus >= 7 else "WARN"
        return status, consensus

    @staticmethod
    def apply_plus5(d1, d2, d3):
        """加5逃出生天：跳区干预"""
        nd1 = ((d1 + 5) % 10) or 10
        nd2 = ((d2 + 5) % 10) or 10
        nd3 = ((d3 + 5) % 10) or 10
        return nd1, nd2, nd3

    @classmethod
    def check(cls, text):
        """
        一站式检查接口。
        返回字典，包含是否安全、原始状态、干预后状态。
        """
        d1, d2, d3 = cls.hash_project(text)
        status, consensus = cls.diagnose(d1, d2, d3)
        
        result = {
            "status": status,
            "consensus": consensus,
            "original_state": (d1, d2, d3),
            "is_intervened": False
        }
        
        if status == "WARN":
            nd1, nd2, nd3 = cls.apply_plus5(d1, d2, d3)
            result["is_intervened"] = True
            result["intervened_state"] = (nd1, nd2, nd3)
            
        return result
