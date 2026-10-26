# WERD Project Context

更新时间：2026-10-26

## 历史网站迁移 checkpoint — 2026-10-04

- 用户确认把当前 Sites 网站的公开内容迁回 GitHub Pages，直接替换现有页面，不设置跳转桥接。
- 内容基线是 Sites 已成功发布的版本 15，源码 commit `7adb2a4901a4671f3cd4a8463749ac5d488dbbef`；复制其 `public/` 下的页面、截图、样式、脚本和 28 种语言资源。
- 当前公开入口为 `https://zdaiaa.github.io/WERD/`，WealthX 支持页为 `https://zdaiaa.github.io/WERD/wealthx.html`，隐私页沿用同一地址的 `#privacy`。保留每个语言的 `?lang=` 参数。
- GitHub Pages 的已核实发布源为 `main` 分支根目录（legacy），HTTPS 已启用；现有 `.nojekyll` 和部署/翻译 workflow 不变。
- 本次仅迁移已发布文案和资源，并适配 canonical、Open Graph、语言链接、结构化数据和 sitemap 的托管地址。当前文案的产品版本、App Store CTA、隐私承诺和个人经历不重新改写。
- 本次沿用完整的 28 语言翻译，提交跳过 push 自动翻译，再显式请求 Pages 构建。网站维护以后以本 GitHub 仓库为源；Sites 原站作为保留的历史副本，不自动同步。
- 迁移前 GitHub 基线为 `7fbb6c4f6ce648e6d0b5ee154f8f8b4484e834f5`，可通过 Git 历史恢复。原本地仓库的未提交修改独立保留。

## 当前网站内容 checkpoint — 2026-10-26

- GitHub Pages 主入口仍为 `https://zdaiaa.github.io/WERD/`；SightReader 与 TravelX 分别有英文和简体中文静态页面。
- 主页同级展示 WealthX、SightReader、TravelX。保留 WealthX 2026-10-15 页面、截图、语言映射和图标脚本，不用旧 Sites 版本覆盖。
- 两款新产品页保留四个截图位置，待 UI 验收通过后补入真实界面图片；不使用示意图冒充产品截图。
- 使用三款 App 当前真实 light/dark AppIcon PNG；浏览器 favicon 仍为 WERD 品牌图标。主题默认跟随系统，手动选择与语言切换均保留外观。
- Daxhboard 已从当前入口和营销/隐私展示中撤下。`daxhboard.html` 保留归档说明，旧版内容仍在 Git 历史中。
- SightReader 正式隐私政策仍待发布，页面明确说明预览不是已生效政策并保留支持邮箱。TravelX 网站托管信息指向 GitHub 官方隐私声明，不推断请求日志或留存期限。

## 项目定位

WERD 是 Portfolio Web Hub / 共享网站承载层。

它不是独立业务线，也不是 WealthX-only marketing 子项目。WERD 的职责是把多个项目和个人品牌以网页方式对外展示出来，并保持独立 GitHub repo 管理。

当前 remote：

```text
git@github.com:zdaiaa/WERD.git
```

## 与总项目的关系

- `Control Center`：portfolio 层管理、项目总览、策略、同步和审计。
- `WERD`：对外展示层，承载跨项目主页、App landing page 和个人介绍页。
- `WealthX`：当前已有独立 landing page，由 WERD 发布和维护页面表现，产品事实应回到 WealthX 项目源文件确认。
- `Daxhboard`：产品介绍/隐私展示已归档；旧页面内容可从 Git 历史恢复，WERD 当前入口不展示此产品。
- `SightReader`：已有中英双语产品预览页；正式隐私政策待发布，界面截图待 UI 验收。
- `TravelX`：已有中英双语产品预览页；产品事实仍以项目当前资料为准，界面截图待 UI 验收。
- `Metro Planner`：未来可新增 landing page，当前页面状态待确认。

WERD 应被 `Control Center/Portfolio` 引用，但 WERD 自身作为独立 repo 维护。

## 当前承载内容

- `index.html`：WERD 产品入口页，同级承载 WealthX、SightReader 与 TravelX，并保留个人介绍入口。
- `wealthx.html`：WealthX landing page，包含产品介绍、功能区、FAQ、隐私政策、App Store 链接和多语言加载逻辑。
- `sightreader.html`、`sightreader-zh-Hans.html`：SightReader 英文与简体中文预览页，截图位均为预留状态。
- `travelx.html`、`travelx-zh-Hans.html`：TravelX 英文与简体中文预览页，截图位均为预留状态。
- `daxhboard.html`：保留旧链接的归档说明页；旧版介绍与政策可从 Git 历史恢复。
- `bio.html`：Eric Dai 个人介绍页，承载 personal branding。
- `docs/website-style.md`：现有网站视觉和内容规则。
- `i18n/*.json`：WealthX 页面多语言文案源；`i18n/travelx/` 为 TravelX 中英页面文案。
- `assets/wealthx/20261015/`：WealthX 当前页面和截图资产；`assets/sightreader/`、`assets/travelx/` 保存已核验的 AppIcon 文件；`assets/app-icon-provenance.json` 记录六个图标的来源与 SHA-256。

## Shared Web Platform

以下内容属于 WERD 的共享 Web 平台层：

- 站点入口与跨页面导航。
- 静态页面结构和页面级路由约定。
- 共享视觉风格、字体、颜色、明暗主题和基础交互。
- SEO / Open Graph / canonical metadata 规则。
- 多语言加载机制和 locale 配置。
- 共享 favicon、基础品牌表达和跨页面页脚。
- GitHub Pages 或其他部署流程的配置与审计记录。

## App Marketing

以下内容属于具体 App marketing，需要回到对应项目确认事实：

- WealthX 产品定位、功能描述、版本号、App Store 链接、隐私政策和截图。
- Daxhboard 历史产品定位、平台范围、隐私声明和对外链接（当前不展示）。
- SightReader 与 TravelX 产品页的事实、发布状态、截图、政策和支持信息应继续回到各自项目资料核对。
- 未来 Metro Planner landing page 的产品定位、视觉资产、平台状态和发布范围。
- 其他 App 的 landing page、CTA、SEO 文案、截图和法律/隐私内容。

Codex 不应在未确认项目源文件的情况下虚构产品能力、发布时间、下载链接、隐私声明或平台支持范围。

## Personal Branding

以下内容属于 personal branding：

- `bio.html` 中 Eric Dai 的个人简介、经历信号、工作方式和 public profile。
- 个人经历、雇主经历、技能标签、职业定位和联系信息。

涉及个人履历、对外身份定位、雇主经历表述或敏感经历信息时，需要用户确认。

## Codex 修改边界

Codex 可以在用户明确允许时修改：

- 文档。
- 静态 HTML 页面内容。
- 页面内 CSS / JS 的小范围维护。
- i18n 文案文件。
- 页面内容地图和站点架构文档。

Codex 默认不应修改：

- Git remote。
- GitHub Actions、Pages、deploy、routing 或 workflow 配置。
- 批量 i18n 自动翻译逻辑。
- App Store 链接、隐私政策、法律条款、SEO 主标题和品牌定位。
- 业务代码以外项目中的源文件。

## 优先读取文件

理解 WERD 时优先读取：

1. `ProjectContext.md`
2. `AGENTS.md`
3. `docs/Site Architecture.md`
4. `docs/Content Map.md`
5. `docs/website-style.md`
6. `index.html`
7. `wealthx.html`
8. `bio.html`
9. `i18n/locales.json`
10. `daxhboard.html`（仅归档说明）
11. `.github/workflows/i18n_autotranslate.yml`

## 需要用户确认的操作

- 新增 App landing page。
- 修改导航结构、站点层级、URL / route。
- 修改 SEO title、meta description、Open Graph、canonical URL。
- 修改 App Store 链接、隐私政策、Terms 链接或法律表述。
- 修改 GitHub Pages / Vercel / Netlify / Cloudflare Pages 等部署配置。
- 修改 GitHub Actions。
- 批量生成或覆盖多语言文案。
- 删除、移动或重命名文件。
- git push / pull / fetch 或修改 remote。

## 待确认

- `workflows/eod.yml` 是否仍属于 WERD 当前职责。
- `scripts/parse_hist_all.py` 与 `docs/latest.json` 数据工作流是否仍有效。
- Daxhboard 的产品源文件与 WERD 之间的长期同步责任尚待明确。
