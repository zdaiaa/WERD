# WERD Development Notes

更新时间：2026-10-26

## 当前技术栈初步判断

基于只读观察，WERD 当前是静态网站项目：

- 根目录包含 `index.html`、`wealthx.html`、`sightreader*.html`、`travelx*.html`、`daxhboard.html`（归档说明）和 `bio.html`。
- 页面使用 HTML + inline CSS + vanilla JavaScript；TravelX 另用 `assets/travelx.css`、`assets/travelx.js` 和 `i18n/travelx/*.json`。
- 未发现 `package.json`、Vite、Next.js、Astro、Vercel、Netlify 或 Cloudflare Pages 配置。
- `wealthx.html` 使用 `fetch("i18n/locales.json")` 和 `fetch("i18n/<locale>.json")` 加载多语言 JSON。
- `bio.html` 和 `index.html` 主要使用页面内文案对象进行中英文切换。
- `.github/workflows/i18n_autotranslate.yml` 仅监听列出的根级 `i18n/*.json` 源文件、脚本和自身；`i18n/travelx/` 产品文案不在当前触发清单中，本轮不改 workflow。
- `workflows/eod.yml` 看起来与 EOD 数据/Pages artifact 有关，业务归属待确认；本轮保持不变。

## 当前目录结构观察

```text
.
├── README.md
├── index.html
├── wealthx.html
├── sightreader*.html
├── travelx*.html
├── daxhboard.html   # 归档说明
├── bio.html
├── WealthX logo.png
├── Daxhboard logo.svg
├── favicon.ico
├── assets/
│   ├── wealthx/20261015/
│   ├── sightreader/
│   ├── travelx/
│   ├── tips/
│   └── app-icon-provenance.json
├── i18n/
├── scripts/
├── docs/
├── .github/workflows/
└── workflows/
```

## 运行方式

使用静态 HTTP server 预览；`wealthx.html` 和 TravelX 页面使用 `fetch` 加载 JSON，因此不应使用 `file://` 直接打开。

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

从仓库的上级目录运行服务器，才能用 `/WERD/` 前缀检查与 GitHub Pages 一致的相对路径。

## 构建方式

当前未发现前端构建配置或 `package.json`。WERD 页面直接以静态 HTML、CSS、JavaScript、JSON 和图片发布；本轮以本地 HTTP 预览、链接/资源扫描和浏览器主题/语言检查代替打包构建。

## 部署方式

当前发布源已确认是 GitHub Pages 的 `main` 分支根目录，公开前缀为 `/WERD/`。发布流程不修改 Pages 设置、Actions 或部署配置。

当前证据：

- HTML 中的 canonical / Open Graph URL 指向 `https://zdaiaa.github.io/WERD/wealthx.html` 和 `https://zdaiaa.github.io/WERD/bio.html`。
- `.nojekyll` 存在，常见于 GitHub Pages 静态发布。
- `.github/workflows/i18n_autotranslate.yml` 会自动提交 i18n 翻译。
- `workflows/eod.yml` 位于 `workflows/` 而不是 `.github/workflows/`；其历史用途待确认，本轮未修改。

尚未核实：

- 是否还有 Vercel / Netlify / Cloudflare Pages 外部配置。
- `workflows/eod.yml` 是否为历史遗留；本轮保持该文件不变。

## 代码风险

- `README.md` 与 `ProjectContext.md` 应保持当前三产品入口、双语预览页与 Daxhboard 归档状态一致。
- `docs/` 目录为小写；用户目标路径写作 `Docs/`。当前不做大小写重命名，避免移动现有文件。
- `wealthx.html` 是大型单文件页面，结构、样式、脚本和内容耦合较高。
- `bio.html` 与 `index.html` 使用页面内翻译对象，而 `wealthx.html` 使用外部 i18n JSON，国际化机制不完全一致。
- `.github/workflows/i18n_autotranslate.yml` 有写入权限并会 push 翻译提交；修改 i18n 源文件前要明确影响范围。
- `scripts/__pycache__` 存在；本轮不清理。
- `workflows/eod.yml` 的业务归属不清，可能是历史数据工作流或其他项目遗留。不要在未确认前删除或修改。

## 文档缺口

本轮新增文档用于补齐：

- `ProjectContext.md`：Codex / agent 项目定位。
- `AGENTS.md`：WERD 内部 agent 规则。
- `docs/Site Architecture.md`：站点信息架构。
- `docs/Content Map.md`：页面内容地图。
- `docs/Development Notes.md`：技术观察、风险和待确认项。

仍缺：

- 部署审计记录：GitHub Pages 已确认使用 `main` 根目录；发布记录需在每次上线后补充。
- Landing page 新增流程模板：Metro Planner 新页面提出前需要创建。
- i18n 维护规则：需要明确哪些页面使用外部 JSON，哪些页面仍是内嵌对象。

## 当前维护边界

- TravelX 的四个截图位仍保持预留，待其独立 UI 验收后补图；SightReader 中英页面各展示四张原始 App 截屏，网页添加单层 CSS iPad 外框，不裁切或重绘截图。
- SightReader 的完整中英双语隐私政策于 2026-10-30 首次正式公开发布并生效，英文与简体中文页面均可通过 `#privacy` 访问。四张场景截屏均对应当前页面语言，图外保留曲谱来源与许可说明；源文件与 SHA-256 列于 `assets/sightreader/screenshots/provenance.json`。
- TravelX 页面保留 `noindex,nofollow`；网站托管说明链接 GitHub 官方隐私声明，不声称日志处理或留存期限。
- WealthX 2026-10-15 页面、截图和 `assets/wealthx/20261015/hub.js` 映射继续作为当前基线。

## 后续维护建议

1. 决定 `workflows/eod.yml` 是否仍属于 WERD。
2. 为 Metro Planner landing page 建立创建前检查清单。
3. 建立轻量检查流程，验证 route、asset、i18n key 和 Content Map 一致性。
