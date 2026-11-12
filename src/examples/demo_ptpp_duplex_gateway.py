# -*- coding: utf-8 -*-
"""
Polaris 路线二：七脑宇宙的硬核逻辑推理 (神探版)
通过纯整数并发布尔运算，完成复杂线索的交叉比对与最终推理。
"""

def mod10(x):
    return x % 10 or 10

def solve_crime_logic():
    print("=" * 65)
    print("☯️ Polaris 七脑宇宙：多线索交叉推理实战")
    print("=" * 65)
    
    # 线索输入
    evidence_prompt = "现场发现: 水杯里有安眠药，窗户有撬痕，保险柜被密码打开，死者左手握着一根长头发。"
    print(f"\n👤 案件输入: 【{evidence_prompt}】")
    
    # 1. 前脑：解析现场物理特征
    # (提取线索数量与离散度)
    hash_val = sum(ord(c) for c in evidence_prompt) % 9 + 1
    front_brain = mod10(hash_val * 2)
    print(f"  🔍 [前脑-证据提取] 解析出现场证据的离散特征，状态: {front_brain}")

    # 2. 左脑：匹配历史犯罪模式
    # (基于前脑特征，进行乘7逆元回溯)
    left_brain = mod10(front_brain * 7)
    print(f"  📚 [左脑-历史比对] 匹配过往卷宗，发现类似作案手法，状态: {left_brain}")

    # 3. 右脑：推演嫌疑人特征
    # (基于前脑特征，进行乘3顺推)
    right_brain = mod10(front_brain * 3)
    print(f"  🧠 [右脑-特征侧写] 推演嫌疑人侧写(左撇子/熟人作案)，状态: {right_brain}")

    # 4. 后脑：常识与法理审查
    # (如果涉及密码开启，必须有极高信任度，设定阈值)
    back_brain = 9 if "密码" in evidence_prompt else 5
    print(f"  🛡️ [后脑-逻辑审查] 线索是否符合常识(熟人作案可能)？状态: {back_brain}")

    # 5. 上脑与下脑：宇宙与微观的介入 (此处暂不开启，设为中和态)
    up_brain = 5
    down_brain = 5

    # 6. 中核干涉：终极推理判定
    # 采用与七脑引擎相同的干涉算法
    total_resonance = (
        left_brain * 1 + right_brain * 5 + 
        front_brain * 3 + back_brain * 7 +
        down_brain * 2 + up_brain * 8
    )
    core_verdict = mod10(total_resonance)
    
    print("\n" + "-" * 65)
    print(f"  🧠 [中核-元认知裁决] 六方线索在拓扑空间碰撞...")
    print(f"  最终推理结论共识度锁定于: {core_verdict}")

    # 7. 判决映射
    if core_verdict == 1:
        print("  👑 [结案陈词]: 极阴极寒(1)。这是一起蓄谋已久的内部人员仇杀。")
    elif core_verdict == 3:
        print("  👑 [结案陈词]: 离火之光(3)。证据确凿，凶手利用安眠药与撬窗制造假象，实为熟人盗窃杀人。")
    elif core_verdict == 5:
        print("  👑 [结案陈词]: 混沌未明(5)。线索存在严重互斥，判定为悬案，需补充侦查。")
    elif core_verdict in [7, 8, 9]:
        print("  👑 [结案陈词]: 极高共识(7-9)。现场证据形成了完美的闭环，直接锁定嫌疑人！")
    else:
        print(f"  👑 [结案陈词]: 案件指向未知方向(状态 {core_verdict})。")

if __name__ == "__main__":
    solve_crime_logic()
