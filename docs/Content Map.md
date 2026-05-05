# WERD Content Map

更新时间：2026-05-05

## 页面地图

| 页面名称 | URL / route | 所属业务线 | 页面目的 | 主要文案来源 | 视觉资产来源 | 当前状态 | Codex 自动维护 | 是否同步到 Control Center portfolio dashboard |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| WERD 产品入口页 | `/WERD/` 或 `index.html`，发布路径待确认 | Portfolio Web Hub | 作为 WERD 的产品入口，当前指向 WealthX，并保留 Biography 导航 | `index.html` 内嵌文案；未来应参考 Control Center 的项目列表 | `WealthX logo.png`；共享站点样式 | active | 可以维护结构和已确认文案；导航变化需确认 | 是 |
| WealthX landing page | `/WERD/wealthx.html` | WealthX | 展示 WealthX 产品定位、功能、FAQ、隐私政策和 App Store CTA | `wealthx.html`、`i18n/en-US.json`、`i18n/zh-Hans.json`；产品事实需回到 WealthX 源文件确认 | `WealthX logo.png`、`assets/tips/*.png` | active | 仅限已确认事实、格式、链接检查和 i18n 缺口；SEO/隐私/CTA 需确认 | 是 |
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
- 当前内容：WERD home、WealthX product card、Biography link、privacy link。
- 维护注意：新增产品卡片前，应先更新 `docs/Site Architecture.md`。

### `wealthx.html`

- 状态：active。
- 当前目的：WealthX 主 landing page。
- 当前内容：hero、feature map、product details、FAQ、privacy policy、App Store CTA。
- 维护注意：隐私政策、App Store URL、版本号、SEO 和产品承诺需要确认。

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
