# -*- coding: utf-8 -*-
# Copyright (c) 2026 999chengying / Polaris Project
# Licensed under the Apache License, Version 2.0

"""
Polaris 多中心路由：天圆地方三层防御 + 体用归一化
R²=4 面心归5 / R²=8 棱心×3 / R²=12 顶点+5
"""

CENTER = (3, 3, 3)


def mod10(x):
    return x % 10 or 10


def sphere_shell(coord):
    """返回 R²：0 中宫 / 4 面心 / 8 棱心 / 12 顶点"""
    return sum((coord[i] - CENTER[i]) ** 2 for i in range(3))


def defend(state, r2):
    """天圆地方三层防御"""
    if r2 == 0:
        return state, "中宫"
    if state not in [2, 4, 6, 8]:
        return state, "安全"
    if r2 == 12:
        return mod10(state + 5), "顶点+5"
    if r2 == 8:
        return mod10(state * 3), "棱心×3"
    if r2 == 4:
        return 5, "面心归5"
    return state, "未知"


def yong_to_ti(coord, val):
    """体用归一化：Y=5/Z=5 ×7；Y=5/Z=1 ×3；Z=1/Y=3 ×3"""
    x, y, z = coord
    if val == 5:
        return 5
    if y == 5:
        if z == 5:
            return (val * 7) % 10 or 10
        elif z == 1:
            return (val * 3) % 10 or 10
    if z == 1 and y == 3:
        return (val * 3) % 10 or 10
    return val
