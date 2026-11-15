# 九宫八卦结构可视化图集 (Visual Atlas)

## 序言

本图集是体系的视觉索引。通过8张核心图表，直观展示27宫立方体的几何骨架、赋值转换、路径动力学、寻址半径、跨球连接、连续球面以及动态决策机制。

所有图表均使用 SVG 代码生成，可无损缩放。读者可将代码复制至任意 SVG 渲染器查看，或直接阅读本图集。

---

## 第一章：基础骨架

### 图1：十三射线全向信道

```svg
<svg xmlns="http://www.w3.org/2000/svg" width="300" height="300" viewBox="0 0 300 300">
<circle cx="150" cy="150" r="120" fill="none" stroke="#333"/>
<line x1="210.0" y1="150.0" x2="90.0" y2="150.0" stroke="red" stroke-width="2"/>
<line x1="150.0" y1="210.0" x2="150.0" y2="90.0" stroke="red" stroke-width="2"/>
<line x1="270.0" y1="150.0" x2="30.0" y2="150.0" stroke="red" stroke-width="2"/>
<line x1="270.0" y1="150.0" x2="30.0" y2="150.0" stroke="orange" stroke-width="1.5"/>
<line x1="270.0" y1="150.0" x2="30.0" y2="150.0" stroke="orange" stroke-width="1.5"/>
<line x1="270.0" y1="150.0" x2="30.0" y2="150.0" stroke="orange" stroke-width="1.5"/>
<line x1="270.0" y1="150.0" x2="30.0" y2="150.0" stroke="orange" stroke-width="1.5"/>
<line x1="270.0" y1="150.0" x2="30.0" y2="150.0" stroke="orange" stroke-width="1.5"/>
<line x1="270.0" y1="150.0" x2="30.0" y2="150.0" stroke="orange" stroke-width="1.5"/>
<line x1="270.0" y1="150.0" x2="30.0" y2="150.0" stroke="blue" stroke-width="1.5"/>
<line x1="270.0" y1="150.0" x2="30.0" y2="150.0" stroke="blue" stroke-width="1.5"/>
<line x1="270.0" y1="150.0" x2="30.0" y2="150.0" stroke="blue" stroke-width="1.5"/>
<line x1="270.0" y1="150.0" x2="30.0" y2="150.0" stroke="blue" stroke-width="1.5"/>
<circle cx="150" cy="150" r="4" fill="black"/>
<text x="5" y="20" font-size="11">红=3轴 橙=6面对角 蓝=4体对角</text>
</svg>
