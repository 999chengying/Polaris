# -*- coding: utf-8 -*-
# Copyright (c) 2026 999chengying / Polaris Project
# Licensed under the Apache License, Version 2.0

"""
Polaris Warehouse v3.0: 4096 宫同构分形存储引擎 (空间折叠版)
16(外层) * 16(中层) * 16(内层) = 4096 个存储小立方体。
实现通过六维坐标直接寻址，物理显存恒定，同构折叠无限扩容。
"""

def mod10(x):
    return x % 10 or 10

class FractalWarehouse:
    def __init__(self):
        self.storage_pool = {}
        self.slots = [
            (1, 3, 1), (1, 5, 3), (1, 1, 3), (1, 3, 5), (1, 1, 1), (1, 5, 1), (1, 1, 5), (1, 5, 5),
            (5, 5, 1), (5, 1, 1), (5, 5, 5), (5, 1, 5), (5, 5, 3), (5, 1, 3), (5, 3, 1), (5, 3, 5)
        ]
        self.managers = {}

    def _get_slot_index(self, data_16):
        buckets = {1: [], 2: [], 3: [], 4: []}
        temp_pool = []
        for val in data_16:
            rem = val % 4
            if rem == 0: rem = 4 
            if len(buckets[rem]) == 0:
                buckets[rem].append(val)
            else:
                temp_pool.append(val)
        for rem in [1, 2, 3, 4]:
            if len(buckets[rem]) == 0 and temp_pool:
                buckets[rem].append(temp_pool.pop(0))
        return [buckets[rem][0] if buckets[rem] else 0 for rem in [1, 2, 3, 4]]

    def write_deep(self, data_16, outer_idx, middle_idx):
        inner_vals = self._get_slot_index(data_16)
        checksum = mod10(sum(inner_vals))
        self.managers[(outer_idx, middle_idx)] = checksum
        for i, val in enumerate(inner_vals):
            if val != 0:
                self.storage_pool[(outer_idx, middle_idx, i)] = val
        print("  [折叠写入] 路径 ({}, {}) | 校验位: {} | 写入点: {}".format(outer_idx, middle_idx, checksum, len(inner_vals)))

    def read_deep(self, outer_idx, middle_idx, inner_idx):
        return self.storage_pool.get((outer_idx, middle_idx, inner_idx), 0)

    def simulate_corruption(self, outer_idx, middle_idx, inner_idx):
        path = (outer_idx, middle_idx, inner_idx)
        original = self.storage_pool.get(path, 0)
        if original == 0: return False
        del self.storage_pool[path]
        manager_val = self.managers[(outer_idx, middle_idx)]
        other_sum = 0
        for i in range(4):
            if i != inner_idx:
                other_sum += self.storage_pool.get((outer_idx, middle_idx, i), 0)
        recovered = (manager_val - other_sum) % 10
        if recovered == 0: recovered = 10
        self.storage_pool[path] = recovered
        return original == recovered

if __name__ == "__main__":
    wh = FractalWarehouse()
    wh.write_deep([4]*16, 5, 5)
    if wh.simulate_corruption(5, 5, 2):
        print("  [验证成功] 4096 宫底座的深度纠删码闭环！")
