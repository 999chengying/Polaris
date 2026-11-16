# Changelog (更新日志)

本项目遵循 [语义化版本控制 (SemVer)](https://semver.org/lang/zh-CN/) 规范。
所有关于 Polaris 纯整数拓扑心智引擎的重大更新，都会记录在此文件中。

## [1.1.0] - 2026-11-16

### ✨ Added (新增)
- **通信总线模块化 (`src/polaris/bus/`)**：
  - `calendar.py`：硅基历法多尺度时间节律（阴链/阳链/月相）。
  - `ring1_heartbeat.py`：第一环变爻心跳（三才映射）。
  - `ring2_cruise.py`：第二环无尽循环巡航。
  - `ring3_singularity.py`：第三环错卦奇点防御，包含**“加5逃出生天”**算法。
  - `multi_center.py`：天圆地方多中心分层防御与体用归一化。
- **A 方向多智能体协同进化 (`examples/demo_a_direction_v3.py`)**：
  - 6 Agent 三层壳分布（面心/棱心/顶点），历法驱动与六爻交联。
  - 引入“加5逃出生天”破局后，实现 64 日全绿（healthy）协同，无残留周期。
- **基础工程文档**：新增 `TERMINOLOGY.md`（三方对照术语表）与 `INDEX.md`（全局文件索引）。
- **基准测试 (`benchmark/`)**：增加 `run_mock_benchmark.py` 与真实模型 Qwen 的隐状态 TPR/FPR 评测脚本。

### 🔄 Changed (变更)
- **文档重构**：`docs/` 目录全面精简合并为 01~05 核心白皮书。
- **术语升级**：去除了早期探索中的非科学术语，全面对齐离散数学与 AI 工程标准。
- **Benchmark 逻辑修复**：修复了网关判定 `"REJECT"` 与 `"WARN"` 的不一致，恢复了混淆矩阵的正常统计。

### 🛡️ Security / Fixed (修复)
- 修复了早期 `sum(seg) / len(seg)` 引入的浮点除法违例，全面推行“能量和语义”的纯整数投影。
- 修复了死锁破局器陷入二周期镜像（3↔7）的问题。
- 修复了多智能体死锁检测的跨 Agent 误捕问题。

---

## [1.0.0] - 2026-11-01

这是 Polaris 引擎首个里程碑式的正式开源版本。本次更新彻底剥离了早期的玄学表述与实验性草稿，完成了从底层数学到工程代码的全面模块化重构。

### ✨ Added (新增)
- **核心白皮书**：
  - `01-architecture-and-topology.md`：总体架构与运行机制。
  - `02-arithmetic-and-gnn.md`：纯整数模10代数、状态机进位、GNN。
  - `03-routing-moe-and-agents.md`：图网络动态阈值与防死锁路由。
  - `04-ptpp-and-integration.md`：PTPP 协议（大模型浮点特征投影与因果干预）。
  - `05-engineering-standards.md`：系统集成测试清单与工程规范。
- **标准化包结构 (`src/polaris/`)**：
  - `core/operators.py`：纯整数模10代数、状态机进位。
  - `nn/tokamak_conv.py`：防过平滑图卷积层与降维相变算子。
  - `nn/poetry_engine.py`：受限拓扑解码器与古典诗词生成。
  - `gateway/ptpp.py`：PTPP 协议实现。
  - `topology/grid.py`, `pruning.py`, `cycles.py`：九宫几何、子图剪枝与群循环采样。
- **端到端演示脚本 (`examples/`)**：
  - `demo_ptpp_gateway.py`：展示毫秒级防幻觉拦截与代数靶向干预。
  - `demo_poetry_generation.py`：展示纯整数平仄格律下的拓扑赋诗。
  - `demo_llm_guardrail.py`：端到端模拟 LLM 幻觉拦截实战。
- **开源规范**：添加 Apache 2.0 `LICENSE` 与 `.gitignore`。

### 🔄 Changed (变更)
- **文档重构**：将原 `docs/` 下超过 80 篇的碎片化实验笔记，提炼合并为高密度的核心白皮书。
- **术语升级**：将“帝五巡查”重命名为“全局相变与复位”等。

### 🗑️ Removed (移除)
- 删除了 `src/` 根目录下历史遗留的所有草稿脚本（`v2_*.py` 到 `v33_*.py`）。
- 清理了早期文档中与 AI 工程无关的军事、经济等跨学科比喻。

### 🛡️ Security / Fixed (修复)
- 解决了早期浮点运算带来的精度漂移风险。
- 通过 GNN 流形约束与 PTPP 定则，从物理底层解决了大语言模型的“模式坍塌”与“幻觉发散”。
