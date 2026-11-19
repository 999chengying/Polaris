# -*- coding: utf-8 -*-
# Copyright (c) 2026 999chengying / Polaris Project
# Licensed under the Apache License, Version 2.0

"""
Polaris Brain v5.1: 联想记忆版硅基大脑
引入“拓扑近邻唤醒”机制，解决字面差异导致匹配不上的问题。
"""

import itertools

def mod10(x):
    return x % 10 or 10

class MemoryWarehouse:
    def __init__(self):
        self.pool = {}
        self.managers = {}
    def _slot_index(self, data):
        buckets = {1: [], 2: [], 3: [], 4: []}
        temp = []
        for v in data:
            r = v % 4 or 4
            if not buckets[r]: buckets[r].append(v)
            else: temp.append(v)
        for r in [1, 2, 3, 4]:
            if not buckets[r] and temp: buckets[r].append(temp.pop(0))
        return [buckets[r][0] if buckets[r] else 0 for r in [1, 2, 3, 4]]
    def write(self, x, y, data_16):
        vals = self._slot_index(data_16)
        self.managers[(x, y)] = mod10(sum(vals))
        for i, v in enumerate(vals):
            if v != 0: self.pool[(x, y, i)] = v
    def read(self, x, y):
        return [self.pool.get((x, y, i), 0) for i in range(4)]
    def search_nearby(self, target_x, target_y, radius=3):
        best_path, min_dist = None, 999
        for (px, py) in set((px, py) for (px, py, _) in self.pool.keys()):
            dist = abs(px - target_x) + abs(py - target_y)
            if dist <= radius and dist < min_dist:
                min_dist, best_path = dist, (px, py)
        if best_path: return best_path, self.read(best_path[0], best_path[1]), min_dist
        return None, [], 999

class PolarisBrainV5:
    def __init__(self):
        self.coords = list(itertools.product([1, 3, 5], repeat=3))
        self.neurons = {c: 5 for c in self.coords}
        self.warehouse = MemoryWarehouse()
        self.energy_pool = 40
        self.perception_consensus = 5

    def receive_stimulus(self, text):
        third = max(1, len(text) // 3)
        segs = [text[:third], text[third:2*third], text[2*third:]]
        d1 = sum(ord(c) for c in segs[0]) % 10 or 10
        d2 = sum(ord(c) for c in segs[1]) % 10 or 10
        d3 = sum(ord(c) for c in segs[2]) % 10 or 10
        self.perception_consensus = (d1 * 3 + d2 * 5 + d3 * 7) % 10
        self.neurons[(1, 3, 3)] = mod10(self.neurons[(1, 3, 3)] + d1)
        self.neurons[(3, 1, 3)] = mod10(self.neurons[(3, 1, 3)] + d2)
        self.neurons[(3, 3, 1)] = mod10(self.neurons[(3, 3, 1)] + d3)
        self.energy_pool += 10

    def step(self):
        self.energy_pool = max(0, self.energy_pool - 1)
        for coord, state in self.neurons.items():
            if coord != (3, 3, 3):
                self.neurons[coord] = mod10(state + 3) 
        for (x, y, z), state in list(self.neurons.items()):
            if (x, y, z) == (3, 3, 3): continue
            if x != 3:
                self.neurons[(x, y, z)] = mod10(state + self.neurons[(6 - x, y, z)])
            elif y != 3:
                self.neurons[(x, y, z)] = mod10(state * 3 + self.neurons[(x, 6 - y, z)])
        internal = sum(self.neurons[c] for c in self.coords if c != (3, 3, 3))
        self.neurons[(3, 3, 3)] = mod10(internal + self.perception_consensus * 3)

    def memorize_experience(self):
        core = self.neurons[(3, 3, 3)]
        div = len(set(self.neurons.values()))
        path_x = mod10(core * 3) - 1
        path_y = mod10(div * 7) - 1
        memory_vector = [self.neurons[c] for c in self.coords if c != (3,3,3)][:16]
        self.warehouse.write(path_x, path_y, memory_vector)
        print("  [记忆固化] 核心态 {} | 多样性 {} -> 已存入仓库路径 ({}, {})".format(core, div, path_x, path_y))

    def recall_experience(self):
        core = self.neurons[(3, 3, 3)]
        div = len(set(self.neurons.values()))
        path_x = mod10(core * 3) - 1
        path_y = mod10(div * 7) - 1
        memory = self.warehouse.read(path_x, path_y)
        if sum(memory) > 0:
            print("  [精确唤醒] 命中路径 ({}, {})，残片: {}".format(path_x, path_y, memory))
        else:
            best_path, memory, dist = self.warehouse.search_nearby(path_x, path_y, radius=4)
            if best_path:
                print("  [联想唤醒] 目标 ({}, {}) 未命中，但发现临近记忆 ({}, {}) [距离={}]".format(path_x, path_y, best_path[0], best_path[1], dist))
        if sum(memory) > 0:
            for i, val in enumerate(memory):
                coord = self.coords[i]
                self.neurons[coord] = mod10(self.neurons[coord] + val)
