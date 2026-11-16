# -*- coding: utf-8 -*-
# Copyright (c) 2026 999chengying / Polaris Project
# Licensed under the Apache License, Version 2.0

"""
Polaris 第一环：变爻心跳总线
八步莫比乌斯驻波：上→中→下→中→上→中→下→中
三才映射：MAP_TIAN / MAP_REN / MAP_DI
"""

MAP_TIAN = {1:(6,7,8),2:(7,6,8),3:(8,7,6),4:(6,8,7),6:(4,2,3),7:(2,3,4),8:(3,4,2),9:(4,3,2)}
MAP_REN  = {1:(7,8,6),2:(6,8,7),3:(7,6,8),4:(8,7,6),6:(2,3,4),7:(3,4,2),8:(4,2,3),9:(3,2,4)}
MAP_DI   = {1:(8,6,7),2:(8,7,6),3:(6,8,7),4:(7,6,8),6:(3,4,2),7:(4,2,3),8:(2,3,4),9:(2,4,3)}

BEAT_SEQUENCE = [MAP_TIAN, MAP_REN, MAP_DI, MAP_REN, MAP_TIAN, MAP_REN, MAP_DI, MAP_REN]


def heartbeat_step(seq, mode_map):
    """执行一步变爻心跳"""
    next_seq = []
    prev = 5
    for val in seq:
        mixed = (val + prev) % 10
        if mixed == 0:
            mixed = (mixed + 7) % 10
        elif mixed == 5:
            mixed = (mixed + 6) % 10
        if mixed == 0:
            mixed = 9
        transformed = mode_map.get(mixed, (5, 5, 5))
        next_seq.extend(transformed)
        prev = transformed[0]
    return next_seq
