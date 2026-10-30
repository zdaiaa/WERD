# WERD

## 当前网站与维护方式 — 2026-10-26

GitHub Pages 直接承载当前公开网站：

- 产品入口：`https://zdaiaa.github.io/WERD/`
- WealthX 支持/产品页：`https://zdaiaa.github.io/WERD/wealthx.html`
- WealthX 隐私政策：`https://zdaiaa.github.io/WERD/wealthx.html?lang=en-US#privacy`
- SightReader（英文 / 简体中文）：`sightreader.html`、`sightreader-zh-Hans.html`
- SightReader 英文隐私政策：`https://zdaiaa.github.io/WERD/sightreader.html#privacy`
- SightReader 简体中文隐私政策：`https://zdaiaa.github.io/WERD/sightreader-zh-Hans.html#privacy`
- TravelX（英文 / 简体中文）：`travelx.html`、`travelx-zh-Hans.html`

主页同级展示 WealthX、SightReader 与 TravelX。SightReader 英文与简体中文页现已展示完整隐私政策及四张既有产品海报；TravelX 的四个截图位仍待 UI 验收后补充。Daxhboard 入口和营销/隐私展示已从当前站点移除；`daxhboard.html` 保留为归档说明，旧版页面仍可从 Git 历史恢复。WealthX 2026-10-15 页面、截图、图标路由和 28 语言资源保持现有版本。

2026-10-04 的首次迁移以 Sites 版本 15 为基线；其后 GitHub `main` 已于 2026-10-15 更新 WealthX 页面和截图，并在 2026-10-26 加入 SightReader、TravelX 预览页。以 GitHub 当前主站为准，不用旧 Sites 版本覆盖。以后在本仓库修改静态页面，经本地检查后按用户授权发布到 `main`。Pages 发布源为分支根目录，无需迁入 Sites 的应用框架、服务器、凭据或配置。

根级语言源文件及工作流列出的脚本变更会触发现有自动翻译流程。2026-10-04 迁移时按当时流程保留了完整 28 语言成品；本轮新增的 `i18n/travelx/` 文件不在该工作流的触发清单中，因此不会重生成这 28 种现有翻译。Pages 仍从 `main` 根目录发布，本轮不改部署或翻译配置。

WERD 是 Portfolio Web Hub / 共享网站承载层。

它用于承载跨项目主页、App landing page 和个人介绍页，把已经确认的项目内容以网页方式对外展示。WERD 不是独立业务线，也不是 WealthX-only marketing 子项目。

## 为什么存在

总项目的 `Control Center` 负责 portfolio 层管理、项目总览、策略、同步和审计。WERD 负责把这些项目对外展示出来，是项目主页和个人品牌展示的 Web 承载层。

WERD 保持独立 GitHub repo 管理：

```text
git@github.com:zdaiaa/WERD.git
```

## 当前承载页面

| 页面 | 文件 | 当前状态 | 用途 |
| --- | --- | --- | --- |
| WERD 产品入口页 | `index.html` | active | 同级展示 WealthX、SightReader、TravelX，并保留个人介绍入口 |
| WealthX landing page | `wealthx.html` | active | 展示 WealthX 产品定位、功能、FAQ、隐私政策和 App Store CTA |
| SightReader landing page | `sightreader.html`、`sightreader-zh-Hans.html` | preview | 中英双语展示当前读谱能力、完整隐私政策与四张产品海报；隐私政策自 2026-10-30 生效 |
| TravelX landing page | `travelx.html`、`travelx-zh-Hans.html` | preview | 中英双语展示地图、每日行程、住宿规划与当前版本信息；保留产品页 noindex |
| Daxhboard archive notice | `daxhboard.html` | archived | 保留旧链接并说明页面已归档；不再展示产品营销或隐私内容 |
| Personal biography | `bio.html` | active | 展示 Eric Dai 的个人介绍、经历信号和工作方式 |

## 未来可承载页面

WERD 未来可以继续承载：

- Metro Planner landing page
- 其他 App / 项目的 landing page
- 更多个人品牌或 portfolio 展示页面

新增页面前，应先更新 `docs/Site Architecture.md` 和 `docs/Content Map.md`，确认页面 route、内容来源、视觉资产、CTA 和是否允许对外展示。

## 与其他项目的关系

- `Control Center`：管理 portfolio 层状态、策略、同步和审计；WERD 应被 `Control Center/Portfolio` 引用。
- `WealthX`：产品事实、版本号、隐私政策、App Store 链接和截图来源应回到 WealthX 源文件确认；WERD 负责页面呈现。
- `Daxhboard`：WERD 当前仅保留归档说明，不再展示其产品营销或隐私内容。
- `TravelX`：WERD 已承载英文与简体中文产品预览页；产品事实仍以 TravelX 当前项目资料为准，界面截图待 UI 验收后补充。
- `Metro Planner`：未来可加入独立 landing page，route、文案、视觉资产和公开范围待确认。
- Personal branding：`bio.html` 承载个人介绍内容，涉及经历、定位和联系信息时需要用户确认。

## 当前技术形态

基于当前目录观察，WERD 是静态网站项目：

- HTML：`index.html`、`wealthx.html`、`sightreader*.html`、`travelx*.html`、归档页 `daxhboard.html`、`bio.html`
- 样式与交互：页面内 CSS + vanilla JavaScript
- 多语言：`i18n/*.json` 和页面内文案对象并存
- 视觉资产：`assets/wealthx/20261015/`、`assets/sightreader/`、`assets/travelx/`、`assets/tips/*.png`、图标来源记录 `assets/app-icon-provenance.json`、WERD `favicon.ico`
- 网站规则：`docs/website-style.md`

目前未发现 `package.json`、Vite、Next.js、Astro、Vercel、Netlify 或 Cloudflare Pages 配置。

## 本地运行

从仓库的上级目录启动静态 HTTP server，保留 `/WERD/` 子目录路由。`wealthx.html` 与 TravelX 使用 `fetch`，请用 HTTP 预览而不是 `file://`。

```sh
cd ..
python3 -m http.server 8000
```

然后访问：

```text
http://127.0.0.1:8000/WERD/
http://127.0.0.1:8000/WERD/wealthx.html
http://127.0.0.1:8000/WERD/sightreader.html
http://127.0.0.1:8000/WERD/sightreader-zh-Hans.html
http://127.0.0.1:8000/WERD/travelx.html
http://127.0.0.1:8000/WERD/travelx-zh-Hans.html
http://127.0.0.1:8000/WERD/daxhboard.html
http://127.0.0.1:8000/WERD/bio.html
```

## 构建方式

当前没有发现前端构建配置或 `package.json`。页面作为静态 HTML、CSS、JavaScript、JSON 和 PNG 直接发布；使用 HTTP 预览和链接/资源检查验证。

## 部署方式

GitHub Pages 从 `main` 分支根目录发布，公开前缀为 `/WERD/`。本轮不修改 Pages、Actions 或部署配置。

当前证据：

- 页面 canonical / Open Graph URL 指向 `https://zdaiaa.github.io/WERD/...`
- `.nojekyll` 存在，常见于 GitHub Pages 静态发布。
- `.github/workflows/i18n_autotranslate.yml` 存在，会自动翻译并提交 locale 文件。

仍需确认：

- `workflows/eod.yml` 是否仍属于 WERD 当前职责。
- 是否存在外部 Vercel / Netlify / Cloudflare Pages 配置。

## 日常维护流程

建议按以下顺序维护：

1. 先读取 `ProjectContext.md`、`AGENTS.md`、`docs/Site Architecture.md`、`docs/Content Map.md`。
2. 判断改动属于 shared web platform、App marketing 还是 personal branding。
3. 如果改页面内容，先更新或确认 `docs/Content Map.md`。
4. 如果新增 App landing page，先更新 `docs/Site Architecture.md`。
5. 修改页面后检查 route、链接、截图路径、i18n key、SEO metadata 和 canonical URL。
6. 涉及产品事实时，回到对应项目源文件确认。
7. 涉及 SEO、品牌定位、导航结构、隐私政策、App Store CTA 或部署配置时，先给计划并等待确认。

## 文档索引

- `ProjectContext.md`：WERD 的项目定位、边界和 Codex 优先读取顺序。
- `AGENTS.md`：WERD 内部 agent 工作规则。
- `docs/Site Architecture.md`：站点信息架构、内容 owner、routing、自动化边界。
- `docs/Content Map.md`：当前和未来页面的内容地图。
- `docs/Development Notes.md`：技术栈观察、运行/构建/部署方式、风险和下一步。
- `docs/website-style.md`：现有网站视觉和内容风格规则。

## 修改边界

默认不要直接修改：

- Git remote
- GitHub Actions / Pages / deploy / routing 配置
- App Store 链接
- 隐私政策和法律条款
- SEO 主标题、Open Graph、canonical URL
- 批量 i18n 自动翻译逻辑

默认不要执行：

- `git push`
- `git pull`
- `git fetch`
- 删除、移动、重命名文件

上述操作需要用户明确确认。
