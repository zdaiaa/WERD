# WERD Site Architecture

更新时间：2026-07-13

## 定位

WERD 是 Portfolio Web Hub / 共享网站承载层。它把产品、个人介绍和未来项目 landing page 组织成一个可发布的网站。

WERD 不负责 portfolio 层决策；portfolio 层决策由总项目 `Control Center` 管理。WERD 负责把确认后的项目内容对外呈现。

## 当前站点层级

```text
/
├── index.html        # WERD 产品入口页
├── wealthx.html      # WealthX landing page
├── daxhboard.html    # Daxhboard 介绍/隐私页
├── bio.html          # Personal homepage / biography
├── assets/           # 产品截图和共享资产
├── i18n/             # 多语言文案
└── docs/             # 文档和可能的 Pages artifact 输出目录，具体部署关系待确认
```

## Personal Homepage

当前页面：

- `bio.html`

职责：

- 承载 Eric Dai 的个人介绍、经历信号、工作方式和 public profile。
- 为 WERD 与产品页提供个人品牌背景。

维护规则：

- 个人经历、雇主经历、职业定位和联系信息需要用户确认。
- 可以做排版、可读性、可访问性和小范围文案优化，但不能虚构经历。
- 适合被 `Control Center/Portfolio` 引用为 personal branding 展示层。

## WealthX Landing Page

当前页面：

- `wealthx.html`

职责：

- 承载 WealthX 产品定位、核心功能、FAQ、隐私政策和 App Store CTA。
- 使用 `assets/tips/*.png` 作为产品截图资产。
- 使用 `i18n/*.json` 和页面内 i18n 加载逻辑维护多语言内容。

维护规则：

- 产品事实、版本号、隐私政策、App Store 链接必须从 WealthX 源文件或用户确认中获取。
- 不得承诺投资收益、保证省钱、银行级安全或完全自动银行同步。
- 修改页面内容时同步更新 `docs/Content Map.md`。

## Daxhboard Page

当前页面：

- `daxhboard.html`

职责：

- 承载 Daxhboard 产品介绍、平台范围、数据边界和隐私声明。
- 使用 `Daxhboard logo.svg` 作为产品识别资产。

维护规则：

- 产品事实、支持平台、iCloud 同步与隐私表述必须从 Daxhboard 源文件或用户确认中获取。
- 修改页面内容时同步更新 `docs/Content Map.md`。

## Future Apps Landing Pages

未来可承载：

- TravelX landing page：planned，route 待确认。
- Metro Planner landing page：planned，route 待确认。
- 其他 App / 项目的 landing page：planned，route 待确认。

新增规则：

- 先更新本文档，明确页面职责、route、内容来源和资产来源。
- 再更新 `docs/Content Map.md`。
- 然后才创建页面或修改 `index.html` 导航。
- 新增页面前必须确认该项目的定位、状态、主要 CTA、视觉资产和是否已经允许对外展示。

## Shared Components

当前项目没有抽离组件框架，页面以静态 HTML + inline CSS / JS 维护。

可视为共享组件的模式：

- 顶部导航。
- 主题切换按钮。
- 语言选择器。
- 页面 footer。
- CTA button 样式。
- Apple-style 视觉基线。
- WealthX 产品截图的 light/dark 切换逻辑。

是否需要抽离为共享文件：待确认。当前不应在未确认前引入构建工具或组件框架。

## Shared Assets

当前资产：

- `favicon.ico`
- `WealthX logo.png`
- `Daxhboard logo.svg`
- `assets/tips/*.png`

规则：

- WealthX 截图属于 WealthX marketing asset。
- favicon 和站点基础图标属于 WERD shared web platform。
- 未来 TravelX / Metro Planner 资产应放入清晰子目录，命名规则待确认。

## SEO / Metadata

当前观察：

- `wealthx.html` 有 meta description、keywords、Open Graph、canonical URL。
- `bio.html` 有 meta description、Open Graph、canonical URL。
- `index.html` 有基础 description 和 title。

维护规则：

- SEO title、description、Open Graph、canonical URL 属于高影响内容，修改前需要说明计划。
- App landing page 的 SEO 内容必须与对应项目的真实定位一致。
- 不应为了搜索流量夸大产品能力。

## Routing

当前 route 形式：

- `/WERD/` 或 `/WERD/index.html`：产品入口页，实际发布路径待确认。
- `/WERD/wealthx.html`：WealthX landing page。
- `/WERD/daxhboard.html`：Daxhboard 介绍/隐私页。
- `/WERD/bio.html`：个人介绍页。

未来 route：

- TravelX：待确认。
- Metro Planner：待确认。
- 其他项目：待确认。

修改 route 或导航前必须先确认部署方式和外部链接影响。

## Brand System

当前品牌层次：

- WERD：共享网站承载层。
- WealthX：具体 App 品牌。
- Eric Dai biography：personal branding。
- 未来 App：独立品牌或项目品牌，待确认。

视觉规则参考：

- `docs/website-style.md`

## Content Ownership

| 内容类型 | Owner | 维护方式 |
| --- | --- | --- |
| Portfolio 总览与业务线状态 | Control Center | WERD 只引用确认后的对外内容 |
| WERD 站点结构 | WERD | 修改前更新站点架构和内容地图 |
| WealthX 产品事实 | WealthX | WERD 不直接发明产品能力 |
| Personal biography | 用户确认 | 涉及经历和定位必须确认 |
| SEO / navigation / CTA | WERD + 用户确认 | 修改前先给计划 |
| 部署配置 | WERD + 用户确认 | 先只读审计，再改 |

## 自动化更新边界

适合 Codex 自动维护：

- 文档索引和内容地图。
- 页面状态表。
- 已确认产品事实的格式整理。
- 轻量文案一致性检查。
- i18n 缺口扫描。

必须人工确认：

- 新增 landing page。
- 修改主导航。
- 修改 SEO 主标题、canonical URL、Open Graph。
- 修改 App Store CTA。
- 修改隐私政策、Terms、法律声明。
- 修改部署 workflow。
- 发布前对外品牌定位。
