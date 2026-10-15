(() => {
  const root = document.documentElement;
  const cache = new Map();
  const selection = document.querySelector('#language-select');
  const toggle = document.querySelector('#theme-toggle');
  const query = new URLSearchParams(location.search);
  const imageRoot = 'assets/wealthx/20261015';
  let config, messages, fallback, activeLocale, requestNumber = 0;
  let theme = query.get('theme');
  if (!['light', 'dark'].includes(theme)) {
    try { theme = localStorage.getItem('werd-theme'); } catch { /* Storage is optional. */ }
  }
  if (!['light', 'dark'].includes(theme)) theme = matchMedia('(prefers-color-scheme: dark)').matches ? 'dark' : 'light';
  root.dataset.theme = theme;

  function readJson(path) {
    if (!cache.has(path)) cache.set(path, fetch(`${path}?v=20261015`, {cache:'no-cache'}).then(response => {
      if (!response.ok) throw new Error(`Unable to load ${path}`);
      return response.json();
    }).catch(error => { cache.delete(path); throw error; }));
    return cache.get(path);
  }
  function t(key) { return messages[key] ?? fallback[key] ?? key; }
  function sourceLocale() { return activeLocale.startsWith('zh-') ? 'zh-Hans' : activeLocale === 'ja' ? 'ja' : 'en-US'; }
  function applyImages() {
    const source = sourceLocale(); root.dataset.screenshotLocale = source;
    document.querySelectorAll('[data-product-shot]').forEach(img => {
      const path = `${imageRoot}/devices/${img.dataset.productShot}.${source}.${theme}.png`;
      if (img.getAttribute('src') !== path) img.src = path;
    });
    document.querySelectorAll('[data-icon]').forEach(img => { img.src = `${imageRoot}/icon-${theme}.png`; });
    toggle.setAttribute('aria-pressed', String(theme === 'dark'));
    toggle.setAttribute('aria-label', t(theme === 'dark' ? 'wx_switch_light' : 'wx_switch_dark'));
  }
  function updateLinks() {
    const suffix = `?lang=${encodeURIComponent(activeLocale)}&theme=${theme}`;
    document.querySelectorAll('[data-home-link]').forEach(link => { link.href = `index.html${suffix}`; });
    const url = new URL(location.href); url.searchParams.set('lang', activeLocale); url.searchParams.set('theme', theme);
    history.replaceState(null, '', url);
  }
  function applySchema() {
    const url = `https://zdaiaa.github.io/WERD/wealthx.html?lang=${encodeURIComponent(activeLocale)}`;
    const graph = {
      '@context': 'https://schema.org', '@graph': [
        {'@type':'SoftwareApplication', name:'WealthX', operatingSystem:'iOS, iPadOS', applicationCategory:'FinanceApplication', url,
          downloadUrl:'https://apps.apple.com/app/id6749512735', description:t('meta_description'), inLanguage:activeLocale,
          featureList:[t('wx_sharing_title'),t('feature_budget_title'),t('feature_flows_title'),t('wx_reconcile_title'),t('feature_insights_title'),t('feature_goals_title'),t('feature_widgets_title')]},
        {'@type':'FAQPage', inLanguage:activeLocale, mainEntity:[...document.querySelectorAll('#faq-list details')].map(item => ({
          '@type':'Question', name:item.querySelector('summary').textContent, acceptedAnswer:{'@type':'Answer',text:item.querySelector('p').textContent}
        }))}
      ]
    };
    document.querySelector('#schema-json').textContent = JSON.stringify(graph);
    document.querySelector('link[rel=canonical]').href = url;
    document.querySelector('meta[property="og:url"]').content = url;
  }
  function setTitleLines(selector, lines) {
    const node = document.querySelector(selector); node.replaceChildren();
    lines.forEach((line,index) => { if(index) node.append(document.createElement('br')); node.append(document.createTextNode(line)); });
  }
  function applyCopy() {
    root.lang = activeLocale;
    root.dir = config.locales.find(locale => locale.code === activeLocale)?.dir || 'ltr';
    selection.value = activeLocale;
    document.querySelectorAll('[data-i18n]').forEach(node => { node.textContent = t(node.dataset.i18n); });
    document.querySelectorAll('[data-i18n-attr]').forEach(node => {
      node.dataset.i18nAttr.split(',').forEach(item => {
        const [attribute,key] = item.split(':').map(value => value.trim());
        if(attribute && key) node.setAttribute(attribute,t(key));
      });
    });
    if(activeLocale === 'zh-Hans') {
      setTitleLines('#hero-title',['看清每一笔，','安排每一步。']);
      setTitleLines('#sharing-title',['一起花的钱，','每个人的份额都清楚。']);
    } else if(activeLocale === 'ja') {
      setTitleLines('#hero-title',['お金の流れを知り、','次の一歩を整える。']);
      setTitleLines('#sharing-title',['共同支出の負担を、','ひとりずつ明確に。']);
    }
    applyImages(); updateLinks(); applySchema();
  }
  async function changeLocale(locale) {
    const currentRequest = ++requestNumber;
    selection.setAttribute('aria-busy','true');
    try {
      const copy = await readJson(`i18n/${locale}.json`);
      if(currentRequest !== requestNumber) return;
      messages = copy; activeLocale = locale; applyCopy();
    } catch(error) {
      selection.value = activeLocale;
      console.error(error);
    } finally {
      if(currentRequest === requestNumber) selection.removeAttribute('aria-busy');
    }
  }
  function restoreHash() {
    let hash;
    try { hash = decodeURIComponent(location.hash.slice(1)); } catch { return; }
    if(hash === 'privacy') document.querySelector('#privacy-policy').open = true;
    const target = document.getElementById(hash);
    if(target) requestAnimationFrame(() => target.scrollIntoView({behavior:'instant',block:'start'}));
  }
  Promise.all([readJson('i18n/locales.json'),readJson('i18n/en-US.json')]).then(async values => {
    [config,fallback] = values;
    const normalize = value => config.aliases[value] || value;
    const requested = normalize(query.get('lang') || navigator.language || 'en-US');
    activeLocale = config.locales.some(locale => locale.code === requested) ? requested : config.locales.find(locale => locale.code.split('-')[0] === requested.split('-')[0])?.code || 'en-US';
    messages = activeLocale === 'en-US' ? fallback : await readJson(`i18n/${activeLocale}.json`);
    selection.replaceChildren();
    for(const locale of config.locales) { const option = document.createElement('option'); option.value = locale.code; option.textContent = locale.label; selection.append(option); }
    applyCopy(); restoreHash();
    selection.addEventListener('change',()=>changeLocale(selection.value));
    toggle.addEventListener('click',()=>{
      theme = theme === 'dark' ? 'light' : 'dark'; root.dataset.theme = theme; applyImages(); updateLinks();
      try { localStorage.setItem('werd-theme',theme); } catch { /* No persistence is required. */ }
    });
    window.addEventListener('hashchange',restoreHash);
  }).catch(error => {
    root.lang = 'en-US'; root.dataset.theme = 'light';
    document.querySelectorAll('[data-product-shot]').forEach(img => { img.src = `${imageRoot}/devices/${img.dataset.productShot}.en-US.light.png`; });
    selection.disabled = true; toggle.disabled = true;
    console.error(error);
  });
})();
