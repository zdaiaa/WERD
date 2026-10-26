# WERD Site Architecture

## 历史发布结构 — 2026-10-04

已核实 GitHub Pages 从 `main` 分支根目录发布，站点前缀为 `/WERD/`。现行静态 route 使用仓库根目录文件名和相对资源路径；WealthX 继续使用 `wealthx.html?lang=<locale>#privacy` 作为本地化隐私地址。

本次内容来自 Sites 已发布版本 15 的 `public/` 静态目录，只适配托管 URL，不迁入应用服务器、Sites 凭据或框架配置。现有 Pages 设置、workflow、路由名称与 `.nojekyll` 保留。整站公开内容在 GitHub 上独立提供，访问者无需转跳到原 Sites 域名。

更新时间：2026-10-26

## 当前页面发布结构 — 2026-10-26

- `/WERD/` 的产品卡片同级展示 WealthX、SightReader、TravelX；现有 WealthX hero、2026-10-15 截图与 `hub.js` 语言/图标映射保持不变。
- `/WERD/sightreader.html` 与 `/WERD/sightreader-zh-Hans.html`：SightReader 英文与简体中文产品预览。每页保留四个截图位；UI 验收后再补入真实 App 界面。正式隐私政策待提供，当前页面明确声明预览不是生效政策并保留支持邮箱。
- `/WERD/travelx.html` 与 `/WERD/travelx-zh-Hans.html`：TravelX 英文与简体中文产品预览，使用 `assets/travelx.css`、`assets/travelx.js` 和 `i18n/travelx/`。网站托管说明仅指向 GitHub 官方隐私声明，不声明未核实的请求日志或留存事实。
- `/WERD/daxhboard.html`：保留旧链接的归档说明页，设为 `noindex`；旧版产品介绍与隐私文本保存在 Git 历史中，不再出现在主页、sitemap 或当前营销页。
- 三个 App 的 light/dark 图标来自各自当前项目 AppIcon PNG。产品图标随页面主题切换，网站标签页继续使用 WERD `favicon.ico`。
- 共享相对路由基于 GitHub Pages `/WERD/` 子目录；不要使用从域名根部开始的 `/assets/...` 绝对资源路径。

## 定位

WERD 是 Portfolio Web Hub / 共享网站承载层。它把产品、个人介绍和未来项目 landing page 组织成一个可发布的网站。

WERD 不负责 portfolio 层决策；portfolio 层决策由总项目 `Control Center` 管理。WERD 负责把确认后的项目内容对外呈现。

## 当前站点层级

```text
/
├── index.html        # WERD 产品入口页
├── wealthx.html      # WealthX landing page
├── sightreader*.html # SightReader 英文 / 简体中文预览页
├── travelx*.html     # TravelX 英文 / 简体中文预览页
├── daxhboard.html    # 旧链接的归档说明页
├── bio.html          # Personal homepage / biography
├── assets/           # 产品截图、AppIcon 和共享资产
├── i18n/             # 多语言文案
└── docs/             # 项目文档；Pages 从仓库根目录发布
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

## Daxhboard Archive Route

当前页面：

- `daxhboard.html`

职责：

- 为访问旧链接的用户说明 Daxhboard 页面已归档。
- 不再展示产品营销、功能或隐私声明；页面设置为 `noindex,follow`。
- 旧产品页面和文案保存在 Git 历史中。

维护规则：

- 旧版产品事实仍在历史版本；不得从归档说明推断当前产品状态。

## Future Apps Landing Pages

未来可承载：

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
- `assets/wealthx/20261015/`：WealthX 当前图标与页面截图。
- `assets/sightreader/`、`assets/travelx/`：对应 App 当前 light/dark AppIcon PNG。
- `assets/app-icon-provenance.json`：记录六个 AppIcon 文件的来源、用途、尺寸和 SHA-256。
- `assets/tips/*.png`：WealthX 旧页面资源；保留现状。

规则：

- WealthX 截图属于 WealthX marketing asset。
- favicon 和站点基础图标属于 WERD shared web platform。
- SightReader 与 TravelX 页面中的四个截图位均为预留状态，UI 验收通过后才能替换为真实截图。
- Metro Planner 资产待确认后再纳入。

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

- `/WERD/` 或 `/WERD/index.html`：产品入口页，GitHub Pages 从 `main` 根目录提供。
- `/WERD/wealthx.html`：WealthX landing page。
- `/WERD/daxhboard.html`：旧链接的归档说明页，不再是当前产品/隐私页。
- `/WERD/bio.html`：个人介绍页。

未来 route：

- Metro Planner：待确认。

当前已发布 route：

- `/WERD/sightreader.html`、`/WERD/sightreader-zh-Hans.html`。
- `/WERD/travelx.html`、`/WERD/travelx-zh-Hans.html`。
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
| SightReader、TravelX 产品事实与支持/隐私内容 | 各 App 项目 | 只呈现已提供的当前信息；未确认政策保留准备状态与支持方式 |
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
