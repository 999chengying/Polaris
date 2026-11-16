# -*- coding: utf-8 -*-
# Copyright (c) 2026 999chengying / Polaris Project
# Licensed under the Apache License, Version 2.0

"""Polaris 通信总线包：三环 + 历法 + 多中心"""

from .calendar import Calendar, YIN_CHAIN, YANG_CHAIN, MONTH_CYCLE
from .ring1_heartbeat import heartbeat_step, MAP_TIAN, MAP_REN, MAP_DI, BEAT_SEQUENCE
from .ring2_cruise import EndlessCycle, ENDLESS_CYCLE
from .ring3_singularity import SingularityRing
from .multi_center import sphere_shell, defend, yong_to_ti, CENTER, mod10

__all__ = [
    "Calendar", "YIN_CHAIN", "YANG_CHAIN", "MONTH_CYCLE",
    "heartbeat_step", "MAP_TIAN", "MAP_REN", "MAP_DI", "BEAT_SEQUENCE",
    "EndlessCycle", "ENDLESS_CYCLE",
    "SingularityRing",
    "sphere_shell", "defend", "yong_to_ti", "CENTER", "mod10",
]
