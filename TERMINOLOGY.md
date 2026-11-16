# Polaris 术语表 v6.1

> 三方对照：对话语言 / 文档正式术语 / 代码标识符
> 铁律：核心代码禁 float，模10/模24 代数，Type Hint + Docstring
> 更新日期：2026-11-16

---

## 一、核心术语三方对照

### 1.1 时间与节律

| 对话语言 | 文档正式术语 | 代码标识符 | 出处 |
|---|---|---|---|
| 变爻心跳 | 第一环：微观节拍 | ring1_heartbeat / heartbeat_step | demo_heartbeat_seven_brains |
| 后天巡航 | 第二环：无尽循环 | ring2_cruise / ENDLESS_CYCLE | demo_houtian_avoid5_bus |
| 错卦奇点 | 第三环：宏观破局 | ring3_singularity / break_deadlock | demo_singularity_bus |
| 三才映射 | 天/人/地三张表 | MAP_TIAN / MAP_REN / MAP_DI | demo_heartbeat_seven_brains |
| 历法日推进 | 下卦先后天置换 | forward_map / next_post_to_pre | demo_multi_scale_calendar |
| 历法阴链 | 阴链 [1,2,4,7] | YIN_CHAIN | demo_temporal_driven_agent |
| 历法阳链 | 阳链 [8,3,9,6] | YANG_CHAIN | demo_temporal_driven_agent |
| 无尽循环 | 外围环形路由 | ENDLESS_CYCLE | 06 研究 / 07 验证 |

### 1.2 空间与拓扑

| 对话语言 | 文档正式术语 | 代码标识符 | 出处 |
|---|---|---|---|
| 太极中宫/帝5 | 中心锚点 | CENTER = (3, 3, 3) | grid.py / bus/multi_center |
| 球壳分层 | R平方梯度 | sphere_shell(coord) -> int | 11/12/13/16/17 |
| 四角柱 | 四根 Z 轴竖棱 | pillar_values | 14/15 |
| 甲号用附值 | 三轴并发 | JiaHaoHexagramBlock | jiahao_hexagram_block.py |
| 截面活跃子集 | 不同截面不同活跃集 | SENSORY_CUBE / AXIS_DIGITS | demo_sensory_node / 25 |

### 1.3 代数与算子

| 对话语言 | 文档正式术语 | 代码标识符 | 出处 |
|---|---|---|---|
| 错卦=合十 | 乘9 等同于 10减x | cuogua(x) = (x*9)%10 | demo_3d_light_switch |
| 帝5巡查/加5逃出生天 | 生克翻转（加5） | break_deadlock / x+5 | demo_singularity_bus / v3.7 |
| 体用归一化 | 乘3/乘7 逆元 | yong_to_ti | operators.py / 09 |
| 炼丹算子 | 1/7/9 | _alchemy | 19/20 |

### 1.4 通信与多智能体

| 对话语言 | 文档正式术语 | 代码标识符 | 出处 |
|---|---|---|---|
| 双环通道 | 1-4/2-5/3-6 三通道 | DualRingNetworkNode | 18/19 |
| 六爻交联 | 内外卦应位 | _six_yao_coupling | 17/18/23 / v3.7 |
| 拓扑溢出 | 曼哈顿溢出 | route_with_overflow | 20/21 |

---

## 二、固定常数表（全部整数）

### 2.1 干涉权重

| 体系 | 权重 | 验证次数 |
|---|---|---|
| 七脑 | 左1 右5 前3 后7 下2 上8 | 3 次 |
| 六合三轴 | 前后乘2 左右乘3 上下乘4 | 1 次 |

### 2.2 球壳防御阈值

| R平方 | 壳层 | 防御算子 | 注意力半径 |
|---|---|---|---|
| 0 | 中宫 | 无需干预 | 1 |
| 4 | 面心 | 强制归 5 | 3 |
| 8 | 棱心 | 乘3 逆元 | 5 |
| 12 | 顶点 | 加5 生克翻转 | 9 |

### 2.3 时间序列

| 名称 | 序列 |
|---|---|
| 无尽循环 | [2,3,1,4,9,7,8,6,5] |
| 历法阴链 | [1,2,4,7] |
| 历法阳链 | [8,3,9,6] |
| 历法月相 | [8,3,9,6,1,2,4,7] |
| 先后天置换 | {1:2, 2:4, 4:7, 7:1, 8:3, 3:9, 9:6, 6:8} |

---

## 三、四套距离度量

| 度量 | 公式 | 用途 | A 方向是否使用 |
|---|---|---|---|
| 欧氏距离平方 R平方 | 坐标差的平方和 | 球壳分层 | 是 |
| 曼哈顿距离 | 坐标差的绝对值之和 | 建边 / 拓扑溢出 | 是 |
| 切比雪夫距离 | 各维度差的最大绝对值 | 2D-RoPE | 否 |
| 环形距离 | min(abs(d), 10-abs(d)) | 螺旋注意力衰减 | 可选 |

---

## 四、核心层 float 违例清单（待修复）

| 文件 | 违例行 | 性质 |
|---|---|---|
| nn/tokamak_conv.py | over_smooth_threshold: float = 0.5 等 | 核心 |
| nn/sparse_transformer.py | sum/len ; float('inf') | 核心 |
| gateway/ptpp.py | abs_mean * 10 | 网关 |
| nn/polaris_block.py | int(abs(sum(seg) / len(seg))) | 核心 |
| 21-topological-overflow-moe.py | sum/len + variance + float('inf') | 验证 |

统一修法：`sum(seg) / len(seg)` 改为 `sum(seg) % 10`（能量和语义）。
