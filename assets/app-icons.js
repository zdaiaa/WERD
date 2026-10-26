// Use the genuine exported AppIcon rendition, never a recolored substitute.
(() => {
  const root = document.documentElement;
  const system = matchMedia('(prefers-color-scheme: dark)');
  function syncIcons() {
    const dark = root.dataset.theme ? root.dataset.theme === 'dark' : system.matches;
    document.querySelectorAll('[data-app-icon]').forEach(element => {
      const path = dark ? element.dataset.iconDark : element.dataset.iconLight;
      const attribute = element.tagName === 'LINK' ? 'href' : 'src';
      if (element.getAttribute(attribute) !== path) element.setAttribute(attribute, path);
    });
  }
  new MutationObserver(syncIcons).observe(root, {attributes: true, attributeFilter: ['data-theme']});
  system.addEventListener('change', syncIcons);
  syncIcons();
})();
