# WERD Website Style

The WERD website should follow an Apple-style product-page baseline.

## Visual Direction

- Use the system font stack: `-apple-system`, `BlinkMacSystemFont`, `SF Pro Text`, `SF Pro Display`, then common web fallbacks.
- Keep layout quiet, spacious, and product-led. Use large hero type, clear sections, generous vertical rhythm, and restrained navigation.
- Use real product captures or product assets as the main visual signal. Avoid decorative illustrations, gradients, or generic stock-like imagery.
- Keep pages static and framework-free unless the site outgrows the current structure.

## Color Baseline

- Light mode: `#f5f5f7` background, `#ffffff` surfaces, `#1d1d1f` primary text, `#6e6e73` secondary text.
- Dark mode: `#000000` background, `#161617` surfaces, `#f5f5f7` primary text, `#a1a1a6` secondary text.
- Use Apple blue for interactive emphasis: `#0066cc` in light mode and `#2997ff` in dark mode.
- Avoid one-note custom palettes. WealthX may use product captures for visual personality, but the website shell should stay neutral.

## Page Structure

- `index.html` is the product entry page. It currently lists WealthX only and should stay ready for future products.
- `wealthx.html` is the full WealthX product page.
- Future products should get separate detail pages and be added to the product entry page, not mixed into WealthX sections.

## Motion

- Use scroll-triggered motion sparingly, inspired by Apple product pages: small fades, short vertical movement, and clear sequencing.
- Motion should reveal hierarchy and product focus, not decorate the page.
- Feature-map cards may enter in a subtle stagger on scroll. Product captures and text should settle quickly and never block reading.
- Always support `prefers-reduced-motion` by showing content without animation.

## Content Rules

- Keep public claims conservative and feature-backed.
- Do not promise guaranteed savings, investment advice, bank-level security, risk-free privacy, or fully automatic bank sync.
- Keep privacy policy content localized through `i18n/*.json`; preserve `mailto:` links in markup rather than translating them into plain text.
