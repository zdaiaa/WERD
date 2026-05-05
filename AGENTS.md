# WERD Agent Instructions

WERD 是 Portfolio Web Hub / 共享网站承载层，用于承载 WealthX 主页、个人介绍主页，以及未来可能加入的 TravelX、Metro Planner 和其他 App landing page。

## 默认流程

- 默认先审计再修改。
- 修改前先读取 `ProjectContext.md`、`docs/Site Architecture.md`、`docs/Content Map.md` 和相关页面文件。
- 对无法确认的信息写“待确认”，不要编造。
- 不要假设 WERD 是独立业务线。
- 不要把 WERD 当成 WealthX-only marketing 子项目。

## 禁止事项

- 不允许直接 `git push`、`git pull`、`git fetch`。
- 不允许修改 git remote。
- 不允许删除文件。
- 不允许移动或重命名文件，除非用户明确要求。
- 不允许随意修改部署配置、GitHub Actions、Pages、routing、workflow、package 或 build 配置。
- 不允许引入新的技术栈决策，除非用户明确要求并先完成方案说明。

## 页面与内容规则

- 修改主页内容时，必须同步更新 `docs/Content Map.md`。
- 新增 App landing page 前，必须先更新 `docs/Site Architecture.md`。
- 修改页面 URL、导航层级、CTA、SEO、Open Graph、canonical URL 或品牌定位时，必须先说明计划。
- 修改 WealthX 产品事实、隐私政策、App Store 链接或版本号时，必须先回到 WealthX 源文件确认。
- 修改个人介绍页时，涉及个人经历、雇主经历、职业定位或联系信息的内容必须先获得用户确认。

## 部署与自动化规则

- 涉及 GitHub Pages / Vercel / Netlify / Cloudflare Pages 等部署配置时，必须先只读审计并等待确认。
- 涉及 `.github/workflows/` 或 `workflows/` 的改动，必须先说明当前 workflow 的用途、触发条件、写入范围和风险。
- i18n 自动翻译 workflow 可能会提交内容；修改前必须说明影响范围。

## 文档维护

- `ProjectContext.md` 记录项目定位和 Codex 工作边界。
- `docs/Site Architecture.md` 记录站点信息架构。
- `docs/Content Map.md` 记录页面、route、业务线、内容来源和维护状态。
- `docs/Development Notes.md` 记录技术栈观察、风险和待确认项。
- `docs/website-style.md` 是当前视觉和内容风格规则，应继续保留。

## 输出偏好

- WERD 项目管理类文档默认使用中文。
- 对外页面文案按页面现有语言策略执行，不要随意改成单一语言。
- 总结时区分：当前状态、风险、下一步、是否需要用户决策。
