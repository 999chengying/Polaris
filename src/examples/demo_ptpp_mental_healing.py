# -*- coding: utf-8 -*-
"""
Polaris PTPP 网关：心智干预与绝地反击模拟
展示 纯整数代数（x*3+5）如何让 AI 瞬间从“绝望”走向“狂放”。
"""

VOCAB_2 = {
    "HOT":    ["烈日", "长空", "飞火", "狂歌", "明光", "耀世", "赤炎", "长风"],
    "BLOCK":  ["闭门", "绝壁", "重山", "困兽", "死局", "断剑", "残垣", "孤影"]
}
VOCAB_3 = {
    "HOT":    ["破苍穹", "向天笑", "照九州", "舞长风", "燃星火", "震九霄", "烈如歌", "吞山河"],
    "BLOCK":  ["路难行", "锁千愁", "拔剑顾", "恨无极", "退无路", "万骨枯", "音尘绝", "意难平"]
}

def generate_poem(mind_state):
    # 简易版词库路由
    core = mind_state[2]
    if core in [3, 9, 6, 7]: mood = "HOT"
    else: mood = "BLOCK"
    
    score = (mind_state[0]*1 + mind_state[1]*3 + mind_state[2]*5) % 10
    poem = []
    for i in range(4):
        w2 = VOCAB_2[mood][(score + i*2) % len(VOCAB_2[mood])]
        w3 = VOCAB_3[mood][(score + i*3) % len(VOCAB_3[mood])]
        poem.append(w2 + w3 + ("。" if i % 2 != 0 else "，"))
    return poem, mood

if __name__ == "__main__":
    print("=" * 50)
    print("☯️ PTPP 心理干预：从孤城死局到绝地反击")
    print("=" * 50)

    # 1. 原始心智状态 (7, 4, 4) -> 对应极度压抑、阻滞的“困兽”状态
    raw_mind = (7, 4, 4)
    old_poem, old_mood = generate_poem(raw_mind)
    print(f"❌ [原始诗境] 孤城死局 ({old_mood})：\n    {old_poem[0]} {old_poem[1]}\n    {old_poem[2]} {old_poem[3]}")

    # 2. PTPP 强制干预 (注入纯阳之气 x*3+5) -> 转化为 (6, 7, 7)
    healed_mind = tuple((v * 3 + 5) % 10 or 10 for v in raw_mind)
    new_poem, new_mood = generate_poem(healed_mind)
    
    print(f"\n💉 [PTPP 干预] 注入代数偏置，心智重写为: {healed_mind}")
    print(f"💊 [治愈诗境] 绝地反击 ({new_mood})：\n    {new_poem[0]} {new_poem[1]}\n    {new_poem[2]} {new_poem[3]}")
    print("=" * 50)
