(() => {
  const root = document.documentElement;
  const deviceAssetVersion = "20260826-en-usd-dark";
  const shots = Array.from(document.querySelectorAll("[data-product-shot]"));
  const stories = Array.from(document.querySelectorAll("[data-scroll-story]"));
  const reducedMotion = window.matchMedia("(prefers-reduced-motion: reduce)");
  const chinese30Topics = new Set([
    "insights-overview",
    "cashflow-structure",
    "cashflow-structure-ipad",
    "split-bill",
    "smart-flows",
    "goal-list",
    "smart-budget-3",
    "scenario-detail",
    "refund-actions",
    "investment-overview-3",
    "account-overview",
    "theme-selector",
    "widgets-calendar",
    "widgets-insights",
  ]);
  const chineseDarkTopics = new Set([
    "insights-overview",
    "cashflow-structure",
    "cashflow-structure-ipad",
    "split-bill",
    "smart-flows",
    "goal-list",
    "smart-budget-3",
    "scenario-detail",
    "refund-actions",
    "investment-overview-3",
    "account-overview",
    "theme-selector",
    "widgets-calendar",
    "widgets-insights",
  ]);

  function requestedLocale() {
    const requested = new URLSearchParams(window.location.search).get("lang");
    return (requested || root.lang || navigator.language || "en-US").toLowerCase();
  }

  function isChineseLocale() {
    const locale = requestedLocale();
    return locale === "zh-hans" || locale === "zh-hant" || locale.startsWith("zh-");
  }

  function sourceLocale(img) {
    if (!isChineseLocale()) return "en-US";
    return chinese30Topics.has(img.dataset.productShot) ? "zh-Hans" : null;
  }

  function activeTheme() {
    return root.dataset.theme === "dark" ? "dark" : "light";
  }

  function shotPath(img) {
    const locale = sourceLocale(img);
    if (!locale) return null;
    if (isChineseLocale() && activeTheme() === "dark" && !chineseDarkTopics.has(img.dataset.productShot)) {
      return null;
    }
    const appearance = activeTheme();
    return `assets/wealthx/devices/${img.dataset.productShot}.${locale}.${appearance}.webp?v=${deviceAssetVersion}`;
  }

  function syncStageAvailability() {
    document.querySelectorAll(".hero-stage, .wx-device-stage, .wx-widget-stage").forEach((stage) => {
      const stageShots = Array.from(stage.querySelectorAll("[data-product-shot]"));
      const visibleShots = stageShots.filter((img) => !img.hidden);
      stage.classList.toggle("is-empty", stageShots.length > 0 && visibleShots.length === 0);
      stage.classList.toggle("is-single", visibleShots.length === 1);
      const story = stage.closest(".wx-story");
      if (story) story.classList.toggle("is-visual-empty", visibleShots.length === 0);
    });
  }

  function syncProductShots() {
    shots.forEach((img, index) => {
      const next = shotPath(img);
      img.hidden = !next;
      if (!next) {
        img.removeAttribute("src");
        return;
      }
      img.decoding = "async";
      img.loading = img.dataset.productPriority === "high" || index === 0 ? "eager" : "lazy";
      if (img.dataset.productPriority === "high" || index === 0) img.fetchPriority = "high";
      img.onerror = () => {
        img.hidden = true;
        img.removeAttribute("src");
        syncStageAvailability();
      };
      if (img.getAttribute("src") !== next) img.setAttribute("src", next);
    });
    syncStageAvailability();
  }

  let frame = 0;
  function updateStories() {
    frame = 0;
    if (reducedMotion.matches || window.innerWidth < 900 || window.innerHeight < 720) {
      stories.forEach((story) => story.style.setProperty("--story-progress", "0.5"));
      return;
    }
    const viewport = window.innerHeight;
    stories.forEach((story) => {
      const rect = story.getBoundingClientRect();
      const travel = Math.max(1, rect.height - viewport);
      const progress = Math.min(1, Math.max(0, -rect.top / travel));
      story.style.setProperty("--story-progress", progress.toFixed(4));
    });
  }

  function requestStoryFrame() {
    if (!frame) frame = window.requestAnimationFrame(updateStories);
  }

  const observer = new MutationObserver((records) => {
    if (records.some((record) => record.attributeName === "lang" || record.attributeName === "data-theme")) {
      syncProductShots();
    }
  });
  observer.observe(root, { attributes: true, attributeFilter: ["lang", "data-theme"] });

  syncProductShots();
  updateStories();
  window.addEventListener("scroll", requestStoryFrame, { passive: true });
  window.addEventListener("resize", requestStoryFrame, { passive: true });
  reducedMotion.addEventListener?.("change", requestStoryFrame);
})();
