# WealthX Apple-inspired 官网刷新线框

更新时间：2026-07-13

状态：等待用户确认，尚未修改 `index.html` 或 `wealthx.html`。

## 核心承诺

- English source: `A clearer structure for personal finance.`
- 中文源文案：`让复杂的个人财务保持结构清楚`
- 支持证明：`manual-first, review-first` 和 `different money jobs, one review rhythm`。
- 不使用：省钱、收益、完全自动、绝对隐私、投资建议或银行级安全承诺。

## `index.html`：WERD 产品入口

### 1. 安静的 WERD 顶部导航

- 左侧：WERD 标识。
- 右侧：Biography、locale、theme。
- 保持 WERD portfolio hub 定位，不把页面修改成 WealthX-only 站点。

### 2. Portfolio Hero

- 小标签：WERD / Products for real life。
- 主标题：介绍一组帮助用户看清状态、保持掌控的产品。
- 不在此阶段确定最终文案；PR3 单独审查。

### 3. WealthX Featured Product

- 大比例 WealthX 产品区，使用 `charts-overview` 透明设备图。
- 图片随 source locale 与 theme 切换。
- 保留进入 `wealthx.html` 的唯一主 CTA。

### 4. Daxhboard Product Entry

- 保留当前 Daxhboard 产品卡、路由和已确认事实。
- 视觉层级低于 Featured WealthX，但不隐藏或弱化为辅助链接。

### 5. Footer

- 保留 Biography、WealthX Privacy 和 Daxhboard Privacy 链接。

## `wealthx.html`：沉浸式产品叙事

### Scene 1 — Hero / 复杂财务，清楚组织

- 首屏左侧是承诺、支持文案与 App Store CTA。
- 右侧是 `charts-overview` 透明设备图，仅当前 locale/theme 预加载。
- 顶部导航保留 Features、FAQ、Privacy、locale 和 theme。

### Scene 2 — Budget + Scenario / 不同用途，清楚边界

- 文案主张：日常、旅行、家庭、副业和长期目标不必全部挤进一个月度视图。
- 粘性产品舞台在 `smart-budget` 与 `scenario-switch` 之间进行受控转场。
- 不声称 Scenario 直接绑定 Account。

### Scene 3 — Flow / 重复模式，真实确认

- 使用 `flow-use`。
- 强调可复用收入、支出、转账和退款模式，但不承诺全自动执行或金额永远正确。

### Scene 4 — Goals + Investments / 日常与长期

- 双设备组合：`goal-detail` + `investment-overview`。
- 表达长期目标和投资记录在同一个组织系统里可见。
- 投资区块只表述记录、上下文和视图，不表述建议、预测或收益。

### Scene 5 — Insights + Cashflow Map / 多个视角

- 使用 `cashflow-map`。
- 用地图与图表证明“同一套记录可以回答不同问题”。
- 地理位置表述保持权限与真实功能边界。

### Scene 6 — Widgets / 随手可见的状态

- 使用 `widgets-pair` 一张确定性透明背景的完整双设备构图，在两台 iPhone 内呈现主屏与 Today View。
- 用主屏与 Today View 证明：预算信号、交易流、收支日历和目标状态可以在不打开 App 的情况下被看见。
- 导入/导出的可迁移性与保守隐私表述保留在功能卡、FAQ、Privacy、Terms、联系方式和 App Store URL 中，不再与组件主视觉混用。

### Supporting content

- 保留 FAQ、Privacy 和必要的功能覆盖；Widgets 为独立主场景，Search 等次要能力继续收敛到辅助网格，不与核心叙事争夺层级。

## Motion 规格

### Desktop

- 建议启用条件：`min-width: 900px` 且视口高度可容纳产品舞台。
- 产品图保持 sticky，文案场景按 DOM 顺序滚动。
- 每个场景只使用 opacity、短距离 translate 和克制 scale。
- `IntersectionObserver` 识别当前场景，单一 `requestAnimationFrame` 循环更新 CSS custom property。

### Mobile / short viewport

- 取消长时间 sticky，按“文案 → 设备图”顺序正常排列。
- 只保留短淡入，不做视差或大幅缩放。

### Reduced motion

- 关闭滚动驱动的位移、缩放、深度、视差和交叉淡化。
- 所有文案和图片直接处于最终可见状态。

## 资产路由

- DOM 接口：`data-product-shot="{topic}"`。
- `zh-Hans` 与 `zh-Hant` 路由到 `zh-Hans` 图片。
- 其他 locale 路由到 `en-US` 图片。
- 文件格式：`assets/wealthx/devices/{topic}.{source-locale}.{theme}.webp`。
- 只 eager-load 当前 Hero；其他场景 lazy-load。

## 确认门

用户确认以下内容后才修改页面代码：

1. 六个 WealthX 场景的顺序和主承诺。
2. 32 张透明设备图的扣图质量。
3. Index 继续同时展示 WealthX 与 Daxhboard。
4. Desktop 沉浸式、mobile/reduced-motion 正常文档流的动效边界。
