# WERD

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
| WERD 产品入口页 | `index.html` | active | 当前展示 WealthX 与 Daxhboard，并保留个人介绍入口 |
| WealthX landing page | `wealthx.html` | active | 展示 WealthX 产品定位、功能、FAQ、隐私政策和 App Store CTA |
| Daxhboard 介绍/隐私页 | `daxhboard.html` | active | 展示 Daxhboard 产品范围、数据边界和隐私声明 |
| Personal biography | `bio.html` | active | 展示 Eric Dai 的个人介绍、经历信号和工作方式 |

## 未来可承载页面

WERD 未来可以继续承载：

- TravelX landing page
- Metro Planner landing page
- 其他 App / 项目的 landing page
- 更多个人品牌或 portfolio 展示页面

新增页面前，应先更新 `docs/Site Architecture.md` 和 `docs/Content Map.md`，确认页面 route、内容来源、视觉资产、CTA 和是否允许对外展示。

## 与其他项目的关系

- `Control Center`：管理 portfolio 层状态、策略、同步和审计；WERD 应被 `Control Center/Portfolio` 引用。
- `WealthX`：产品事实、版本号、隐私政策、App Store 链接和截图来源应回到 WealthX 源文件确认；WERD 负责页面呈现。
- `Daxhboard`：产品范围、平台、数据与隐私边界应回到 Daxhboard 源文件确认；WERD 负责页面呈现。
- `TravelX`：未来可加入独立 landing page，route、文案、截图和 CTA 待确认。
- `Metro Planner`：未来可加入独立 landing page，route、文案、视觉资产和公开范围待确认。
- Personal branding：`bio.html` 承载个人介绍内容，涉及经历、定位和联系信息时需要用户确认。

## 当前技术形态

基于当前目录观察，WERD 是静态网站项目：

- HTML：`index.html`、`wealthx.html`、`daxhboard.html`、`bio.html`
- 样式与交互：页面内 CSS + vanilla JavaScript
- 多语言：`i18n/*.json` 和页面内文案对象并存
- 视觉资产：`assets/tips/*.png`、`WealthX logo.png`、`Daxhboard logo.svg`、`favicon.ico`
- 网站规则：`docs/website-style.md`

目前未发现 `package.json`、Vite、Next.js、Astro、Vercel、Netlify 或 Cloudflare Pages 配置。

## 本地运行

待确认。

初步判断可以用静态 HTTP server 预览，因为 `wealthx.html` 会 fetch `i18n/*.json`，直接用 `file://` 打开可能受浏览器限制。

```sh
python3 -m http.server 8000
```

然后访问：

```text
http://127.0.0.1:8000/
http://127.0.0.1:8000/wealthx.html
http://127.0.0.1:8000/daxhboard.html
http://127.0.0.1:8000/bio.html
```

## 构建方式

待确认。

当前没有发现前端构建配置。初步判断 WERD 可能不需要本地 build，直接发布静态文件。

## 部署方式

待确认。

当前证据：

- 页面 canonical / Open Graph URL 指向 `https://zdaiaa.github.io/WERD/...`
- `.nojekyll` 存在，常见于 GitHub Pages 静态发布。
- `.github/workflows/i18n_autotranslate.yml` 存在，会自动翻译并提交 locale 文件。

仍需确认：

- GitHub Pages source 是 repo root、`docs/`、GitHub Actions artifact，还是其他设置。
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
- `docs/Development Notes.md`：技术栈观察、运行/构建/部署待确认项、风险和下一步。
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
