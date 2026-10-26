# WERD Content Map

更新时间：2026-10-26

> 当前迁移（2026-10-04）：用户确认将 Sites 已发布版本 15 的公开内容迁回 GitHub Pages。`/WERD/`、`wealthx.html`、`daxhboard.html` 和 `bio.html` 直接提供页面；WealthX 支持/隐私地址保持已填写的 GitHub 地址，保留 `?lang=` 和 `#privacy`。页面、图片、脚本、28 语言 JSON、社交预览及 sitemap 统一使用 GitHub Pages 托管地址。

> 本次更新（2026-10-15）：保留 GitHub Pages 路由与部署配置，更新 WealthX 产品页与总首页入口。截图来自最新中、英、日 Tips Raw，经 LaunchCanvas 原生设备渲染；其他语言使用英文截图，中文语言组使用中文截图。场景统一称为「场景」，不引入私人/共享场景区分。

> 文案复审（2026-10-15）：对照 WealthX 当前 App 的本地化入口名称，重点打磨英文与日文，核对 28 种语言的场景、分摊、拆分账单、智能流、计划流、预算、目标与对账用词。仅调整既有功能的表达与截图说明；场景不增加私人/共享分类。按用户补充，简繁体将功能名「交易流」统一为「流」，包含正文、关键词、旧文案键与隐私数据清单中的功能称谓；「现金流」及「导入导出流程」保持原义。本轮是源码对照与 AI 编辑审校，尚未经过独立母语者审校。

> 历史说明（2026-07-19）：当时 Sites 为主站，GitHub Pages 首页作为兼容入口。该发布方向已由上述用户决定替代。


> 本次更新（2026-10-26）：主页同级展示 WealthX、SightReader 与 TravelX，保留 WealthX 2026-10-15 页面、截图和 `hub.js` 映射。新增 SightReader、TravelX 中英双语预览页，各保留四个截图位，UI 验收后使用真实 App 界面补图。使用三款 App 当前真实 light/dark AppIcon PNG，WERD favicon 不变。Daxhboard 当前网站营销与隐私内容归档；旧页面内容仍在 Git 历史。SightReader 正式隐私政策待发布；TravelX 网站托管说明使用 GitHub 官方隐私声明，不推断日志或留存。

> 手机与深色模式复审（2026-10-15）：日文产品页主标题与分摊标题按手机宽度调整字号，避免 320px 下出现短尾孤行；总首页日文标题同步适配。主页导航、主题切换及页脚链接补足 44px 点击区域。总首页切换主题同步既有 theme 参数，刷新后保留选择；首次访问且没有主题偏好时使用系统外观。保留已确认的中英日截图及明暗版本，其他语言仍使用英文截图。样式文件引用增加版本参数，使浏览器加载本次修订；路由、文案、截图原件与部署配置不变。

## 页面地图

| 页面名称 | URL / route | 所属业务线 | 页面目的 | 主要文案来源 | 视觉资产来源 | 当前状态 | Codex 自动维护 | 是否同步到 Control Center portfolio dashboard |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| WERD 产品入口页 | `/WERD/` 或 `index.html` | Portfolio Web Hub | 同级展示 WealthX、SightReader、TravelX，并保留 Biography 导航 | `index.html` 内嵌中英文文案 | 三款 App light/dark AppIcon（来源记录见 `assets/app-icon-provenance.json`）；WealthX 2026-10-15 hero 图 | active | 可以维护结构和已确认文案；导航变化需确认 | 是 |
| WealthX landing page | `/WERD/wealthx.html` | WealthX | 展示 WealthX 产品定位、功能、FAQ、隐私政策和 App Store CTA | `wealthx.html`、`i18n/en-US.json`、`i18n/zh-Hans.json`；产品事实需回到 WealthX 源文件确认 | `assets/wealthx/20261015/` 中的图标、设备图、社交预览和 `device-assets.json` | active | 仅限已确认事实、格式、链接检查和 i18n 缺口；SEO/隐私/CTA 需确认 | 是 |
| SightReader 英文页 | `/WERD/sightreader.html` | SightReader | 英文产品预览与支持信息；正式隐私政策待提供 | 页面内文案；当前产品事实来自交接材料 | `assets/sightreader/` AppIcon；四个预留截图位 | preview | 只呈现已确认事实；补图待 UI 验收，隐私政策不得当作已生效 | 是 |
| SightReader 简体中文页 | `/WERD/sightreader-zh-Hans.html` | SightReader | 简体中文产品预览与支持信息；正式隐私政策待提供 | 页面内文案；当前产品事实来自交接材料 | 同上 | preview | 同上 | 是 |
| TravelX 英文页 | `/WERD/travelx.html` | TravelX | 英文产品预览、支持与当前隐私信息 | `travelx.html`、`assets/travelx.js`、`i18n/travelx/en-US.json` | `assets/travelx/` AppIcon；四个预留截图位 | preview / noindex | 页面语言与主题可切换；网站托管仅引用 GitHub 官方说明 | 是 |
| TravelX 简体中文页 | `/WERD/travelx-zh-Hans.html` | TravelX | 简体中文产品预览、支持与当前隐私信息 | `travelx-zh-Hans.html`、`assets/travelx.js`、`i18n/travelx/zh-Hans.json` | 同上 | preview / noindex | 同上 | 是 |
| Daxhboard 归档说明 | `/WERD/daxhboard.html` | Daxhboard | 为旧链接说明页面已归档，不再展示营销或隐私内容 | `daxhboard.html` | WERD favicon | archived / noindex | 仅维护归档说明；旧版内容保存在 Git 历史 | 否 |
| Personal biography | `/WERD/bio.html` | Personal Branding | 展示 Eric Dai 的个人介绍、经历信号和工作方式 | `bio.html` 内嵌文案；个人事实需用户确认 | 页面当前主要为文本和样式；其他视觉资产待确认 | active | 可维护排版、结构和已确认措辞；个人经历和定位需确认 | 是，作为个人品牌入口 |

| Metro Planner landing page | 待确认 | Metro Planner | 未来展示 Metro Planner 产品定位、平台状态和 CTA | 待确认，应来自 metro-planner 文档或用户确认 | 待确认 | planned | 不可自动创建；需先确认定位、route、资产和 CTA | 是，创建后同步 |
| Other App landing pages | 待确认 | 待确认 | 未来承载其他 App 或项目主页 | 待确认 | 待确认 | planned | 不可自动创建；需先确认项目是否适合公开展示 | 视项目状态决定 |

## 内容来源规则

- WERD 不直接决定项目优先级；项目优先级来自 `Control Center/Portfolio`。
- WERD 不直接发明 App 功能；App 功能来自对应项目源文件或用户确认。
- WERD 可以维护页面结构、可访问性、静态资源引用和已确认内容的一致性。
- WERD 的 personal branding 内容必须以用户确认为准。

## 当前页面状态

### `index.html`

- 状态：active；2026-10-15 更新 WealthX 入口。
- 当前目的：WERD 产品入口页，同级展示 WealthX、SightReader、TravelX，并保留 Biography 与 WealthX 隐私链接。
- WealthX 入口：首屏使用 WealthX 当前产品介绍，移除维护者视角的未来入口说明；最新总览完整设备图、当前图标、分摊介绍与直达 `wealthx.html?lang=…#sharing` 的链接。
- 图片契约：`data-product-shot="overview"`，由 `assets/wealthx/20261015/hub.js` 按语言与主题选择图片；中文组 → zh-Hans，日文 → ja，其余 → en-US。

### `wealthx.html`

- 状态：active；2026-10-15 完整页面更新。
- 结构：总览 Hero → 分摊（三步说明与 Pro 范围）→ 六个功能区（预算、流水、对账、洞察、目标、小组件）→ 六项 FAQ → 隐私政策 → App Store CTA。
- 文案：场景是场景，不增加私人或共享类型。分摊用于场景中的项目预算；实际付款由用户在应用外完成。分摊与拆分账单（英文 Split Bill、日文「取引分割」）的用途在 FAQ 中区分。
- 视觉：完整设备图、正常文档流、原生 details FAQ、浅色/深色主题；支持小屏、键盘操作和 reduced-motion。
- 图片：`assets/wealthx/20261015/devices/{topic}.{source-locale}.{theme}.png`；8 个主题 × 中/英/日 × 浅/深 = 48 张。图片来自已制作的真实应用素材，使用 LaunchCanvas 原生渲染；目标配图明确为创建目标界面。
- 语言：28 种文案；中文组使用 zh-Hans 图片，日文使用 ja，其余使用 en-US。每页只请求当前语言/主题图片，首屏优先、其余延迟加载。
- 样式/脚本：`assets/wealthx/20261015/page.css` 和 `page.js`，不改变其他产品的共享脚本。
- SEO：使用无版本号标题和最新 1200×630 社交图，保留 canonical、28 个 hreflang、App Store 地址；SoftwareApplication 和 FAQ 结构化数据与页面一致。
- 隐私：政策事实与各语言内容保留；简繁体数据清单仅同步「流／場景」功能称谓，`#privacy` 仍可直达并展开。政策事实后续可另行对照当前产品核验，本轮未作法律内容改写。
- i18n：新增文案与修改值的 source_hashes 同步记录；未改自动翻译 workflow。新译文尚未经过母语者审校。

### `sightreader.html` 与 `sightreader-zh-Hans.html`

- 状态：双语产品预览；正式隐私政策待提供，页面明确说明当前内容不是生效政策。
- 当前目的：说明读谱、批注、曲谱选择、支持方式与尚未发布的功能状态。
- 截图：每页四个 `data-screenshot-status="reserved"` 截图位；UI 验收前不替换为真实截图。
- 语言切换保留主题偏好；主题默认跟随系统，也可手动选择。

### `travelx.html` 与 `travelx-zh-Hans.html`

- 状态：双语产品预览，保留 `noindex,nofollow`。
- 当前目的：说明地点、每日行程、住宿与当前版本的限制和支持方式。
- 文案：`i18n/travelx/` 的英中 JSON；切换语言不改变主题。
- 托管说明：GitHub Pages 使用 GitHub 官方隐私声明链接；不声明未确认的请求日志或保留期限。
- 截图：每页四个截图位待 UI 验收后补充；旅行计划示意图明确注明并非 App 截图。

### `daxhboard.html`

- 状态：archived / noindex。
- 当前目的：为旧链接说明产品页面已归档，不再展示营销内容或隐私政策。
- 历史：此前页面内容通过 Git 历史保留，不永久删除。

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
