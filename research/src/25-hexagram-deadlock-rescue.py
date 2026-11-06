# -*- coding: utf-8 -*-
"""
Polaris 应用研究：甲号用附值——相变死锁、跨轴救援与全量压测
"""

AXIS_DIGITS = {
    "X": {1, 2, 3, 4, 5, 6, 7, 8, 9},
    "Y": {1, 2, 3, 4, 5, 6, 7, 8, 9},
    "Z1": {1, 4, 5, 6, 9},
    "Z5": {1, 2, 3, 4, 5, 7, 8, 9}
}

def try_mutation(axis_name, upper, lower, op_type):
    axis_digits = AXIS_DIGITS[axis_name]
    if op_type == "加5":
        new_upper = (upper + 5) % 10 or 10
        new_lower = (lower + 5) % 10 or 10
    elif op_type == "乘9":
        new_upper = (upper * 9) % 10
        new_lower = (lower * 9) % 10
    
    if new_upper in axis_digits and new_lower in axis_digits:
        return True, new_upper, new_lower
    return False, new_upper, new_lower

def run_full_stress_test():
    print("=" * 60)
    print("☯️ 全量64卦并发变阵与死锁救援压测")
    print("=" * 60)
    
    gua_values = [1, 2, 3, 4, 6, 7, 8, 9]
    total_tests = 0
    z1_deadlocks = 0
    z5_deadlocks = 0
    rescue_success = 0
    
    for upper in gua_values:
        for lower in gua_values:
            total_tests += 1
            success_z1, _, _ = try_mutation("Z1", upper, lower, "加5")
            if not success_z1:
                z1_deadlocks += 1
                rescue_x, _, _ = try_mutation("X", upper, lower, "加5")
                if rescue_x:
                    rescue_success += 1
                    
            success_z5, _, _ = try_mutation("Z5", upper, lower, "加5")
            if not success_z5:
                z5_deadlocks += 1
                
    print(f"\n[压测结果] 共测试合法卦象组合: {total_tests} 个")
    print(f"  🚨 Z=1 (底层轴) 物理坍缩次数: {z1_deadlocks} 次")
    print(f"  🚨 Z=5 (顶层轴) 物理坍缩次数: {z5_deadlocks} 次")
    print(f"  🆘 触发 X轴 成功救援次数: {rescue_success} 次")
    print(f"  ✅ Z=1 轴自身承载成功率: {((total_tests - z1_deadlocks)/total_tests)*100:.1f}%")
    print(f"  ✅ Z=5 轴自身承载成功率: {((total_tests - z5_deadlocks)/total_tests)*100:.1f}%")
    print("\n【结论】X/Y 轴 1~9 完备，跨轴救援成功率为 100%！")

if __name__ == "__main__":
    run_full_stress_test()
