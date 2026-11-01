# Changelog (更新日志)

本项目遵循 [语义化版本控制 (SemVer)](https://semver.org/lang/zh-CN/) 规范。
所有关于 Polaris 纯整数拓扑心智引擎的重大更新，都会记录在此文件中。

## [1.0.0] - 2026-11-01

这是 Polaris 引擎首个里程碑式的正式开源版本。本次更新彻底剥离了早期的玄学表述与实验性草稿，完成了从底层数学到工程代码的全面模块化重构。

### ✨ Added (新增)
- **四大核心白皮书**：
  - `00-system-architecture-whitepaper.md`：总体架构与运行机制。
  - `01-routing-and-deadlock-prevention.md`：图网络动态阈值与防死锁路由。
  - `02-multi-agent-phase-transition.md`：多智能体拓扑相变与全局锁定。
  - `03-continuous-feature-and-gnn.md`：分形嵌套连续小模与 GNN 防幻觉。
  - `04-autonomous-intent-engine.md`：基于能量池与受控概率的自主意图引擎。
- **标准化包结构 (`src/polaris/`)**：
  - `core/operators.py`：纯整数模10代数、状态机进位、拓扑偏移定则。
  - `nn/tokamak_conv.py`：防过平滑图卷积层与降维相变算子。
  - `nn/poetry_engine.py`：受限拓扑解码器与古典诗词生成。
  - `gateway/ptpp.py`：PTPP 协议（大模型浮点特征投影与因果干预）。
  - `topology/grid.py`, `pruning.py`, `cycles.py`：九宫几何、子图剪枝与群循环采样。
- **端到端演示脚本 (`examples/`)**：
  - `demo_ptpp_gateway.py`：展示毫秒级防幻觉拦截与代数靶向干预。
  - `demo_poetry_generation.py`：展示纯整数平仄格律下的拓扑赋诗。
  - `demo_llm_guardrail.py`：端到端模拟 LLM 幻觉拦截实战。
- **开源规范**：添加 Apache 2.0 `LICENSE` 与 `.gitignore`。

### 🔄 Changed (变更)
- **文档重构**：将原 `docs/` 下超过 80 篇的碎片化实验笔记，提炼合并为高密度的核心白皮书，大幅提升了可读性与学术严谨性。
- **术语升级**：去除了早期探索中的非科学术语（如将“帝五巡查”重命名为“全局相变与复位”），全面对齐现代计算机科学与 AI 工程标准。
- **README 重构**：引入核心架构图、快速开始命令与项目愿景。

### 🗑️ Removed (移除)
- 删除了 `src/` 根目录下历史遗留的所有草稿脚本（`v2_*.py` 到 `v33_*.py`）。
- 清理了早期文档中与 AI 工程无关的军事、经济等跨学科比喻。

### 🛡️ Security / Fixed (修复)
- 解决了早期浮点运算带来的精度漂移风险。
- 通过 GNN 流形约束与 PTPP 定则，从物理底层解决了大语言模型的“模式坍塌”与“幻觉发散”。
