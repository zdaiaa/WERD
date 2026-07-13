# WERD Website Style

> 本文件记录 WERD 静态官网的共享视觉契约。通用方法来自正式 skill
> `$design-apple-inspired-websites`；WERD / WealthX 特有规则以本文件为准。

The WERD website should follow an Apple-style product-page baseline.

## Visual Direction

- Use the system font stack: `-apple-system`, `BlinkMacSystemFont`, `SF Pro Text`, `SF Pro Display`, then common web fallbacks.
- Keep layout quiet, spacious, and product-led. Use large hero type, clear sections, generous vertical rhythm, and restrained navigation.
- Use real product captures or product assets as the main visual signal. Avoid decorative illustrations or generic stock-like imagery. Restrained radial light may be used behind a device stage to separate the product from the neutral shell.
- Keep pages static and framework-free unless the site outgrows the current structure.

## Color Baseline

- Light mode: `#f5f5f7` background, `#ffffff` surfaces, `#1d1d1f` primary text, `#6e6e73` secondary text.
- Dark mode: `#000000` background, `#161617` surfaces, `#f5f5f7` primary text, `#a1a1a6` secondary text.
- Use Apple blue for interactive emphasis: `#0066cc` in light mode and `#2997ff` in dark mode.
- Avoid one-note custom palettes. WealthX may use product captures for visual personality, but the website shell should stay neutral.

## Page Structure

- `index.html` is the portfolio product entry page. It currently lists WealthX and Daxhboard; WealthX may receive the dominant visual stage without turning the page into a WealthX-only site.
- `wealthx.html` is the full WealthX product page.
- Future products should get separate detail pages and be added to the product entry page, not mixed into WealthX sections.

## Product image contract

- Website-derived device images live in `assets/wealthx/devices/`; Craftshot exports remain read-only source material outside this directory.
- Stable filename: `{topic}.{source-locale}.{theme}.webp`, where `source-locale` is `en-US` or `zh-Hans` and `theme` is `light` or `dark`.
- Mark product images with `data-product-shot="{topic}"`. Shared JavaScript selects only the active locale/theme file.
- Widget scene crops live in `assets/wealthx/widgets/` and add `data-product-shot-type="widget"`; they are deterministic website-only crops from approved simulator captures, not generated UI or replacements for source captures.
- `zh-Hans` and `zh-Hant` use the Chinese source group; all other locales use the English source group.
- Only the first/hero device image is eager and high priority. Remaining images use native lazy loading.
- Source mapping, dimensions, alpha status, intended use, and QA state are recorded in `assets/wealthx/device-assets.json`.

## Motion

- Desktop product stories may use native sticky sections, CSS transforms, and one `requestAnimationFrame` scroll loop. Motion must remain proportional to scroll progress and must not trap scrolling.
- Motion should reveal hierarchy and product focus, not decorate the page.
- Under `900px` width or short viewports, stories return to normal document flow with lightweight reveal only.
- Always support `prefers-reduced-motion`: disable scroll-driven translation, scaling, depth, and cross-fade; every image and text block must remain visible and understandable.
- Content order and meaning must never depend on JavaScript or animation.

## Content Rules

- Keep public claims conservative and feature-backed.
- Do not promise guaranteed savings, investment advice, bank-level security, risk-free privacy, or fully automatic bank sync.
- Keep privacy policy content localized through `i18n/*.json`; preserve `mailto:` links in markup rather than translating them into plain text.
