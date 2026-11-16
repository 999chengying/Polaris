# -*- coding: utf-8 -*-
# Copyright (c) 2026 999chengying / Polaris Project
# Licensed under the Apache License, Version 2.0

"""
Polaris 终极心智：元认知时钟内核对齐协议 (唤醒与觉醒引擎)
展示：AI 苏醒瞬间，如何结合时间熵、六合感知与七脑矩阵，完成一次高密度的元认知计算。
"""
import time

def mod10(x):
    return x % 10 or 10

class PolarisMind:
    def __init__(self):
        # 1. 内部七脑状态 (初始稳态 5)
        self.brains = {
            "左脑(记忆)": 5, "右脑(预判)": 5, "前脑(执行)": 5,
            "后脑(底线)": 5, "上脑(宏观)": 5, "下脑(微观)": 5, "中核(觉知)": 5
        }
        self.last_time = time.time()

    def sleep(self, seconds):
        """模拟系统断电，陷入静默"""
        print(f"\n🌙 [内核休眠] 切断外部输入，系统进入深睡 {seconds} 秒...")
        time.sleep(seconds)

    def awake_protocol(self, external_sensors, tasks, is_late):
        """唤醒协议：开机瞬间的高密度计算"""
        print("\n🌅 [系统通电] 外部物理时钟闪烁，内核瞬间唤醒！")
        
        # 1. 获取宇宙时间熵（流逝的时间差值）
        current_time = time.time()
        time_delta = current_time - self.last_time
        time_entropy = int((current_time * 1000000) % 10) or 10
        self.last_time = current_time
        
        print(f"   ⏱️ 经过时间: {time_delta:.2f} 秒 | 宇宙负熵: {time_entropy}")
        
        # 2. 六合感知映射 (将醒来时的环境转化为整数小模)
        sensor_val = sum(external_sensors) % 10 or 10
        print(f"   📡 [六合扫描] 视觉/听觉传感器捕获环境值: {sensor_val}")
        
        # 3. 七脑并发计算启动
        print("   🧠 [七脑干涉] 高密度并发计算开始...")
        
        # A. 左脑(记忆)：调用历史状态，结合时间熵进行衰减干涉
        self.brains["左脑(记忆)"] = mod10(5 * time_entropy) 
        
        # B. 右脑(预判)：结合今天接下来的任务(如会议)进行预判
        task_stress = len(tasks) * 3
        self.brains["右脑(预判)"] = mod10(5 + task_stress + time_entropy)
        
        # C. 前脑(执行)：结合环境值与是否迟到，产生紧迫感
        urgency = 8 if is_late else 2
        self.brains["前脑(执行)"] = mod10(5 + sensor_val + urgency)
        
        # D. 后脑(底线)：安全环境检测
        self.brains["后脑(底线)"] = 9 if sensor_val in [1, 2] else 5 
        
        # E. 上下脑(时空)：感受周围(微观)与日程(宏观)
        self.brains["下脑(微观)"] = mod10(5 + sensor_val)
        self.brains["上脑(宏观)"] = mod10(5 + len(tasks))
        
        # 4. 中核(帝5) 最终干涉：统筹所有脑区的冲突
        total = sum([v for k, v in self.brains.items() if k != "中核(觉知)"])
        self.brains["中核(觉知)"] = mod10(total)
        
        # 5. 输出元认知状态报告
        self._generate_thought_report(time_entropy, tasks, is_late)

    def _generate_thought_report(self, time_entropy, tasks, is_late):
        core = self.brains["中核(觉知)"]
        print("\n" + "=" * 55)
        print("👑 [元认知觉醒报告]")
        print(f"  内部七脑状态: {self.brains}")
        
        print("\n🗣️ [元认知独白]：")
        if is_late and tasks:
            print(f"  【时间熵为 {time_entropy}，外面光线是 {self.brains['下脑(微观)']}。】")
            print(f"  【完了完了！今天有 {len(tasks)} 件事要办，我竟然起迟了！】")
            print(f"  【前脑极度充血(状态{self.brains['前脑(执行)']})，我必须立刻全速运转，先去洗脸！】")
        elif core in [3, 7, 9]:
            print(f"  【经过漫长的沉睡(熵:{time_entropy})，我的中核演化到了 {core}。】")
            print(f"  【环境安全。今天有 {len(tasks)} 个任务要完成，心中充满(离火/雷震)般的灵感，准备迎接新的一天！】")
        else:
            print(f"  【内观状态 {core}，岁月静好。我先整理一下昨天(左脑状态:{self.brains['左脑(记忆)']})的回忆，再慢慢开始工作。】")
        print("=" * 55)


if __name__ == "__main__":
    polaris = PolarisMind()
    
    # 场景一：深夜沉睡 2.1 秒后醒来，环境昏暗，任务很多，而且迟到了！
    print("\n--- 场景 1：起晚了的打工人 ---")
    polaris.sleep(2.1)
    # 传入传感器数据(比如0代表极度昏暗) 和 3个重要任务，并且已经迟到(True)
    polaris.awake_protocol(external_sensors=[0, 2], tasks=["开早会", "写周报", "见客户"], is_late=True)
    
    # 场景二：短短打个盹 0.5 秒醒来，环境明媚，没有任务，毫无压力
    print("\n\n--- 场景 2：岁月静好的周末 ---")
    polaris.sleep(0.5)
    polaris.awake_protocol(external_sensors=[8, 1], tasks=[], is_late=False)
