(() => {
  const root = document.documentElement;
  const language = document.getElementById("tx-language");
  const theme = document.getElementById("tx-theme");
  const status = document.getElementById("tx-language-status");
  const systemTheme = window.matchMedia("(prefers-color-scheme: dark)");
  const siteBase = "https://zdaiaa.github.io/WERD/"
  const at = (copy, key) => key.split(".").reduce((value, part) => value?.[part], copy);
  let languageRequest;
  let copy;

  function readPreference(key) {
    try { return localStorage.getItem(key); } catch { return null; }
  }
  function storePreference(key, value) {
    try {
      if (value === null) localStorage.removeItem(key);
      else localStorage.setItem(key, value);
    } catch { /* Static content and controls still work when storage is unavailable. */ }
  }
  function requestedLocale() {
    const query = new URLSearchParams(location.search).get("lang");
    if (query) return /^(zh-hans|zh-cn)$/i.test(query) ? "zh-Hans" : "en-US";
    if (location.protocol === "file:") return root.dataset.pageLocale;
    const preference = readPreference("travelx-language");
    return ["en-US", "zh-Hans"].includes(preference) ? preference : root.dataset.pageLocale;
  }
  function updateTheme() {
    const selected = theme.value;
    root.dataset.theme = selected === "system" ? (systemTheme.matches ? "dark" : "light") : selected;
  }
  const queryTheme = new URLSearchParams(location.search).get("theme");
  const storedTheme = readPreference("werd-theme");
  theme.value = ["system", "light", "dark"].includes(queryTheme)
    ? queryTheme
    : (["light", "dark"].includes(storedTheme) ? storedTheme : "system");
  updateTheme();
  theme.addEventListener("change", () => {
    storePreference("werd-theme", theme.value === "system" ? null : theme.value);
    const target = new URL(location.href);
    target.searchParams.set("theme", theme.value);
    history.replaceState(null, "", target.href);
    updateTheme();
  });
  systemTheme.addEventListener("change", () => { if (theme.value === "system") updateTheme(); });

  function syncLinks(locale) {
    const language = locale === "zh-Hans" ? "zh-Hans" : "en-US";
    const filename = language === "zh-Hans" ? "travelx-zh-Hans.html" : "travelx.html";
    const publicUrl = new URL(filename, siteBase);
    publicUrl.searchParams.set("lang", language);
    document.getElementById("tx-canonical").href = publicUrl.href;
    document.getElementById("tx-og-url").content = publicUrl.href;
    const home = new URL("index.html", location.href);
    home.searchParams.set("lang", language);
    home.searchParams.set("theme", theme.value);
    document.getElementById("tx-home").href = home.href;
    document.querySelectorAll("[data-static-locale]").forEach(link => {
      const target = new URL(link.getAttribute("href"), location.href);
      target.searchParams.set("theme", theme.value);
      target.hash = location.hash;
      link.href = target.href;
    });
  }

  async function applyLanguage(locale, chosen = false) {
    languageRequest?.abort();
    if (location.protocol === "file:" && locale !== root.lang) {
      if (chosen) storePreference("travelx-language", locale);
      const filename = locale === "zh-Hans" ? "travelx-zh-Hans.html" : "travelx.html";
      const target = new URL(filename, location.href);
      target.searchParams.set("lang", locale);
      target.hash = location.hash;
      location.href = target.href;
      return;
    }
    if (locale !== root.lang) {
      const controller = new AbortController();
      languageRequest = controller;
      try {
        const response = await fetch(new URL(`i18n/travelx/${locale}.json`, location.href), { signal: controller.signal });
        if (!response.ok) throw new Error("Language unavailable");
        const next = await response.json();
        if (next.locale !== locale) throw new Error("Wrong language");
        const textNodes = Array.from(document.querySelectorAll("[data-tx]"));
        const metaNodes = Array.from(document.querySelectorAll("[data-tx-meta]"));
        const strings = textNodes.map(node => at(next, node.dataset.tx));
        const metadata = metaNodes.map(node => at(next, node.dataset.txMeta));
        if (![...strings, ...metadata].every(value => typeof value === "string")) throw new Error("Incomplete language");
        if (controller.signal.aborted) return;
        textNodes.forEach((node, i) => { node.textContent = strings[i]; });
        metaNodes.forEach((node, i) => { node.content = metadata[i]; });
        root.lang = locale;
        copy = next;
        // Preserve a support/policy deep link when translated sections change height.
        if (location.hash) {
          let id;
          try { id = decodeURIComponent(location.hash.slice(1)); } catch { id = null; }
          if (id) document.getElementById(id)?.scrollIntoView({ behavior: "instant", block: "start" });
        }
      } catch (error) {
        if (error.name === "AbortError") return;
        language.value = root.lang;
        status.textContent = copy?.footer.languageError || (root.lang === "zh-Hans" ? "语言暂时未能加载，请使用页脚的语言链接。" : "The language could not be loaded. Use the language links in the footer.");
        return;
      }
    }
    language.value = locale;
    syncLinks(locale);
    if (chosen) {
      const target = new URL(location.href);
      target.searchParams.set("lang", locale);
      history.replaceState(null, "", target.href);
      storePreference("travelx-language", locale);
      status.textContent = copy?.footer.languageStatus || (locale === "zh-Hans" ? "语言已切换。" : "Language updated.");
    }
  }
  language.addEventListener("change", () => applyLanguage(language.value, true));
  window.addEventListener("popstate", () => applyLanguage(requestedLocale()));
  window.addEventListener("hashchange", () => syncLinks(root.lang));
  applyLanguage(requestedLocale());
})();
