# WERD Development Notes

更新时间：2026-07-13

## 当前技术栈初步判断

基于只读观察，WERD 当前是静态网站项目：

- 根目录包含 `index.html`、`wealthx.html`、`daxhboard.html`、`bio.html`。
- 页面使用 HTML + inline CSS + vanilla JavaScript。
- 未发现 `package.json`、Vite、Next.js、Astro、Vercel、Netlify 或 Cloudflare Pages 配置。
- `wealthx.html` 使用 `fetch("i18n/locales.json")` 和 `fetch("i18n/<locale>.json")` 加载多语言 JSON。
- `bio.html` 和 `index.html` 主要使用页面内文案对象进行中英文切换。
- `.github/workflows/i18n_autotranslate.yml` 会在 i18n 源文件或脚本变化时运行自动翻译并提交 locale 文件。
- `workflows/eod.yml` 看起来与 Pages artifact 和 EOD 数据生成有关，是否仍属于 WERD 当前职责待确认。

## 当前目录结构观察

```text
.
├── README.md
├── index.html
├── wealthx.html
├── daxhboard.html
├── bio.html
├── WealthX logo.png
├── Daxhboard logo.svg
├── favicon.ico
├── assets/
│   └── tips/
├── i18n/
├── scripts/
├── docs/
├── .github/workflows/
└── workflows/
```

## 运行方式

待确认。

初步判断：

- 由于 `wealthx.html` 会 fetch 本地 JSON，直接用 `file://` 打开可能受浏览器限制。
- 本地预览更适合使用静态 HTTP server，例如：

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

以上只是基于当前静态文件结构的推断，不代表正式运行流程。

## 构建方式

待确认。

当前没有发现前端构建配置。初步判断 WERD 可能不需要本地 build，直接发布静态文件。

## 部署方式

待确认。

当前证据：

- HTML 中的 canonical / Open Graph URL 指向 `https://zdaiaa.github.io/WERD/wealthx.html` 和 `https://zdaiaa.github.io/WERD/bio.html`。
- `.nojekyll` 存在，常见于 GitHub Pages 静态发布。
- `.github/workflows/i18n_autotranslate.yml` 会自动提交 i18n 翻译。
- `workflows/eod.yml` 使用 GitHub Pages artifact，但该 workflow 位于 `workflows/` 而不是 `.github/workflows/`，是否实际生效待确认。

不能确认：

- GitHub Pages source 是 repo root、`docs/`、GitHub Actions artifact，还是其他设置。
- 是否还有 Vercel / Netlify / Cloudflare Pages 外部配置。
- `workflows/eod.yml` 是否是历史遗留。

## 代码风险

- `README.md` 已更新为 WERD Portfolio Web Hub 入口，并需随新增产品页持续校正页面清单。
- `docs/` 目录为小写；用户目标路径写作 `Docs/`。当前不做大小写重命名，避免移动现有文件。
- `wealthx.html` 是大型单文件页面，结构、样式、脚本和内容耦合较高。
- `bio.html` 与 `index.html` 使用页面内翻译对象，而 `wealthx.html` 使用外部 i18n JSON，国际化机制不完全一致。
- `.github/workflows/i18n_autotranslate.yml` 有写入权限并会 push 翻译提交；修改 i18n 源文件前要明确影响范围。
- `scripts/__pycache__` 存在，是否需要清理待确认。本轮不删除。
- `workflows/eod.yml` 的业务归属不清，可能是历史数据工作流或其他项目遗留。不要在未确认前删除或修改。

## 文档缺口

本轮新增文档用于补齐：

- `ProjectContext.md`：Codex / agent 项目定位。
- `AGENTS.md`：WERD 内部 agent 规则。
- `docs/Site Architecture.md`：站点信息架构。
- `docs/Content Map.md`：页面内容地图。
- `docs/Development Notes.md`：技术观察、风险和待确认项。

仍缺：

- 部署审计记录：需要确认 GitHub Pages source 和实际发布流程。
- Landing page 新增流程模板：新增 TravelX / Metro Planner 页面前需要创建。
- i18n 维护规则：需要明确哪些页面使用外部 JSON，哪些页面仍是内嵌对象。

## 下一步建议

1. 只读审计 GitHub Pages 当前 source 与实际部署入口。
2. 决定 `workflows/eod.yml` 是否仍属于 WERD。
3. 为 TravelX / Metro Planner landing page 建立创建前检查清单。
4. 建立轻量脚本或检查流程，验证 route、asset、i18n key 和 Content Map 一致性。
