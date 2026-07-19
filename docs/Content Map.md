# WERD Content Map

更新时间：2026-07-19

> 迁移说明（2026-07-19）：Sites 已成为 WERD 主站：`https://werd-portfolio.eric-dai.chatgpt.site/`。GitHub Pages 首页保留为兼容入口，原有 WealthX、Daxhboard 与 Biography 深层页面继续可用。

## 页面地图

| 页面名称 | URL / route | 所属业务线 | 页面目的 | 主要文案来源 | 视觉资产来源 | 当前状态 | Codex 自动维护 | 是否同步到 Control Center portfolio dashboard |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| WERD 产品入口页 | `/WERD/` 或 `index.html`，发布路径待确认 | Portfolio Web Hub | 作为 WERD 的产品入口，当前展示 WealthX 与 Daxhboard，并保留 Biography 导航 | `index.html` 内嵌文案；项目列表应参考 Control Center | `WealthX logo.png`、`Daxhboard logo.svg`、`assets/wealthx/devices/*.webp`；共享视觉层 | active | 可以维护结构和已确认文案；导航变化需确认 | 是 |
| WealthX landing page | `/WERD/wealthx.html` | WealthX | 展示 WealthX 产品定位、功能、FAQ、隐私政策和 App Store CTA | `wealthx.html`、`i18n/en-US.json`、`i18n/zh-Hans.json`；产品事实需回到 WealthX 源文件确认 | `WealthX logo.png`、`assets/wealthx/devices/*.webp`、`assets/wealthx/device-assets.json` | active | 仅限已确认事实、格式、链接检查和 i18n 缺口；SEO/隐私/CTA 需确认 | 是 |
| Daxhboard 介绍/隐私页 | `/WERD/daxhboard.html` | Daxhboard | 展示 Daxhboard 产品范围、数据边界与隐私声明 | `daxhboard.html`；产品事实需回到 Daxhboard 源文件确认 | `Daxhboard logo.svg`、页内样式 | active | 可维护排版和已确认事实；平台/数据/隐私表述需确认 | 是 |
| Personal biography | `/WERD/bio.html` | Personal Branding | 展示 Eric Dai 的个人介绍、经历信号和工作方式 | `bio.html` 内嵌文案；个人事实需用户确认 | 页面当前主要为文本和样式；其他视觉资产待确认 | active | 可维护排版、结构和已确认措辞；个人经历和定位需确认 | 是，作为个人品牌入口 |
| TravelX landing page | 待确认 | TravelX | 未来展示 TravelX 产品定位、核心能力和 CTA | 待确认，应来自 TravelX `ProjectContext.md`、roadmap 或用户确认 | 待确认 | planned | 不可自动创建；需先确认定位、route、资产和 CTA | 是，创建后同步 |
| Metro Planner landing page | 待确认 | Metro Planner | 未来展示 Metro Planner 产品定位、平台状态和 CTA | 待确认，应来自 metro-planner 文档或用户确认 | 待确认 | planned | 不可自动创建；需先确认定位、route、资产和 CTA | 是，创建后同步 |
| Other App landing pages | 待确认 | 待确认 | 未来承载其他 App 或项目主页 | 待确认 | 待确认 | planned | 不可自动创建；需先确认项目是否适合公开展示 | 视项目状态决定 |

## 内容来源规则

- WERD 不直接决定项目优先级；项目优先级来自 `Control Center/Portfolio`。
- WERD 不直接发明 App 功能；App 功能来自对应项目源文件或用户确认。
- WERD 可以维护页面结构、可访问性、静态资源引用和已确认内容的一致性。
- WERD 的 personal branding 内容必须以用户确认为准。

## 当前页面状态

### `index.html`

- 状态：active。
- 当前目的：产品入口页。
- 当前内容：WERD home、WealthX 主产品舞台、WealthX 与 Daxhboard product card、Biography link、privacy link。
- 图片契约：使用 `data-product-shot="charts-overview"`，由共享脚本按 locale/theme 选择透明设备资产。
- 维护注意：新增产品卡片前，应先更新 `docs/Site Architecture.md`。

### `wealthx.html`

- 状态：active。
- 当前目的：WealthX 主 landing page。
- 当前内容：hero、feature map、五个桌面 sticky 产品场景（Budget + Scenario、Flow、Goals + Investments、Charts + Cashflow Map、Widgets）、FAQ、privacy policy、App Store CTA。导入、导出与隐私承诺保留在功能卡、FAQ 与隐私政策中。
- 响应式：桌面使用滚动进度叙事；移动端、短 viewport 与 reduced-motion 使用正常文档流。
- 图片契约：`data-product-shot` + `{topic}.{source-locale}.{theme}.webp`；所有当前页面产品图均位于 `assets/wealthx/devices/`。Widgets 使用成对完整设备图 `widgets-pair`，在两台 iPhone 内分别展示主屏与 Today View。中文 locale 使用 `zh-Hans` 图片组，其余使用 `en-US` 图片组。
- 隐私政策：2026-07-14 已统一为 iOS 与 macOS 共用政策，明确 iOS 可选 iCloud、Mac Pro 强制 CloudKit、财务记录不进入 WealthX backend、账户/Apple/Stripe entitlement 元数据处理、服务提供方、锁定与账户删除边界。`en-US` 与 `zh-Hans` 是 source locale；其余 locale 已由现有 i18n workflow 自动同步并通过 fallback 与 JSON 质量 gate，页面随本次 PR 合并到 `main` 后发布。
- 维护注意：隐私政策、App Store URL、版本号、SEO 和产品承诺需要确认。

### `daxhboard.html`

- 状态：active。
- 当前目的：Daxhboard 产品介绍与隐私页。
- 当前内容：平台范围、只读定位、iCloud 快照与数据边界。
- 维护注意：产品范围、平台、数据与隐私表述需回到 Daxhboard 源文件确认。

### `bio.html`

- 状态：active。
- 当前目的：个人介绍主页。
- 当前内容：profile、experience signals、operating style、与 WealthX / WERD 的连接。
- 维护注意：个人经历和 public positioning 需要用户确认。

## 自动化维护建议

适合自动化：

- 扫描页面 route 和 title。
- 检查 `data-i18n` key 是否在 locale 文件中存在。
- 检查截图路径是否存在。
- 检查 `docs/Content Map.md` 与实际页面是否一致。

不适合自动化：

- 自动改 SEO 主标题。
- 自动新增产品页。
- 自动发布个人履历变更。
- 自动改隐私政策。
- 自动变更部署配置。
