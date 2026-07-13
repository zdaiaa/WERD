(() => {
  const root = document.documentElement;
  const shots = Array.from(document.querySelectorAll("[data-product-shot]"));
  const stories = Array.from(document.querySelectorAll("[data-scroll-story]"));
  const reducedMotion = window.matchMedia("(prefers-reduced-motion: reduce)");

  function sourceLocale() {
    const requested = new URLSearchParams(window.location.search).get("lang");
    const locale = (requested || root.lang || navigator.language || "en-US").toLowerCase();
    return locale === "zh-hans" || locale === "zh-hant" || locale.startsWith("zh-")
      ? "zh-Hans"
      : "en-US";
  }

  function activeTheme() {
    return root.dataset.theme === "dark" ? "dark" : "light";
  }

  function shotPath(img) {
    const assetGroup = img.dataset.productShotType === "widget" ? "widgets" : "devices";
    return `assets/wealthx/${assetGroup}/${img.dataset.productShot}.${sourceLocale()}.${activeTheme()}.webp`;
  }

  function syncProductShots() {
    shots.forEach((img, index) => {
      const next = shotPath(img);
      img.decoding = "async";
      img.loading = img.dataset.productPriority === "high" || index === 0 ? "eager" : "lazy";
      if (img.dataset.productPriority === "high" || index === 0) img.fetchPriority = "high";
      if (img.getAttribute("src") !== next) img.setAttribute("src", next);
    });
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
