# WERD Project Context

更新时间：2026-07-13

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
- `Daxhboard`：当前已有独立介绍/隐私页，页面事实应回到 Daxhboard 项目源文件确认。
- `TravelX`：未来可新增 landing page，当前页面状态待确认。
- `Metro Planner`：未来可新增 landing page，当前页面状态待确认。

WERD 应被 `Control Center/Portfolio` 引用，但 WERD 自身作为独立 repo 维护。

## 当前承载内容

- `index.html`：WERD 产品入口页，当前承载 WealthX 与 Daxhboard，并保留个人介绍入口。
- `wealthx.html`：WealthX landing page，包含产品介绍、功能区、FAQ、隐私政策、App Store 链接和多语言加载逻辑。
- `daxhboard.html`：Daxhboard 产品介绍与隐私说明页。
- `bio.html`：Eric Dai 个人介绍页，承载 personal branding。
- `docs/website-style.md`：现有网站视觉和内容规则。
- `i18n/*.json`：WealthX 页面多语言文案源。
- `assets/tips/*.png`：WealthX 页面产品截图资产。

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
- Daxhboard 产品定位、平台范围、隐私声明和对外链接。
- 未来 TravelX landing page 的产品定位、功能范围、截图、路线规划能力和发布状态。
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
10. `daxhboard.html`
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

- GitHub Pages 当前发布源是否为 repo root、`docs/`、GitHub Actions artifact，或其他方式。
- `workflows/eod.yml` 是否仍属于 WERD 当前职责。
- `scripts/parse_hist_all.py` 与 `docs/latest.json` 数据工作流是否仍有效。
- Daxhboard 的产品源文件与 WERD 之间的长期同步责任尚待明确。
