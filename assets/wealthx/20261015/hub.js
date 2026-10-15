(() => {
  const root = document.documentElement;
  function sync() {
    const locale = root.lang || 'en-US';
    const source = locale.startsWith('zh-') ? 'zh-Hans' : locale === 'ja' ? 'ja' : 'en-US';
    const theme = root.dataset.theme === 'dark' ? 'dark' : 'light';
    document.querySelectorAll('[data-product-shot]').forEach(img => {
      const path = `assets/wealthx/20261015/devices/overview.${source}.${theme}.png`;
      if(img.getAttribute('src') !== path) img.src = path;
    });
    document.querySelectorAll('[data-wealthx-icon]').forEach(img => {img.src = `assets/wealthx/20261015/icon-${theme}.png`;});
    const sharing = document.querySelector('#wealthx-sharing-link');
    if(sharing) sharing.href = `wealthx.html?lang=${encodeURIComponent(locale)}&theme=${theme}#sharing`;
    const hero = document.querySelector('#wealthx-hero-link');
    if(hero) hero.href = `wealthx.html?lang=${encodeURIComponent(locale)}&theme=${theme}#sharing`;
    const main = document.querySelector('#wealthx-link');
    if(main) main.href = `wealthx.html?lang=${encodeURIComponent(locale)}&theme=${theme}`;
  }
  new MutationObserver(sync).observe(root,{attributes:true,attributeFilter:['lang','data-theme']});
  sync();
})();
