/* ────────────────────────────────────────────────────────────────────────────
   sirtechify.com — channel home base scripts
   - Mobile nav toggle
   - Episode grid hydration from /static/data/episodes.json
     (only PUBLISHED episodes render; the public JSON only contains episodes
      already uploaded to YouTube — see episodes.json comment + PASS1-NOTES.md)
   ──────────────────────────────────────────────────────────────────────────── */

(function () {
  'use strict';

  // ─── Mobile nav toggle ────────────────────────────────────────────────────
  const menuBtn = document.querySelector('.menu-btn');
  const navLinks = document.querySelector('.nav-links');
  if (menuBtn && navLinks) {
    menuBtn.addEventListener('click', () => navLinks.classList.toggle('active'));
    navLinks.querySelectorAll('a').forEach(a => {
      a.addEventListener('click', () => navLinks.classList.remove('active'));
    });
  }

  // ─── Episode grid hydration ───────────────────────────────────────────────
  const grid = document.getElementById('episodes-grid');
  if (!grid) return;

  const epUrl = grid.dataset.src || '/static/data/episodes.json';

  fetch(epUrl, { cache: 'no-store' })
    .then(r => {
      if (!r.ok) throw new Error('episodes.json HTTP ' + r.status);
      return r.json();
    })
    .then(data => renderEpisodes(grid, data))
    .catch(err => {
      console.error('Episode load failed:', err);
      renderPlaceholder(grid, '// signal lost. retrying soon.');
    });

  function renderEpisodes(container, data) {
    const eps = (data && Array.isArray(data.episodes)) ? data.episodes : [];

    // Defense in depth: even though only published episodes should ever ship in
    // the public JSON, filter again here so a stray non-published row never renders.
    const visible = eps.filter(ep => (ep.status || '').toLowerCase() === 'published');

    if (visible.length === 0) {
      renderPlaceholder(container, '// standing by. awaiting first signal.');
      return;
    }

    const frag = document.createDocumentFragment();
    visible.forEach(ep => frag.appendChild(buildCard(ep)));
    container.innerHTML = '';
    container.appendChild(frag);
  }

  function renderPlaceholder(container, message) {
    container.innerHTML = '';
    const card = document.createElement('div');
    card.className = 'episodes-placeholder';
    card.innerHTML = `
      <p class="placeholder-line">${message}</p>
      <p class="placeholder-sub">First episode drops on YouTube. <a href="https://www.youtube.com/@sirtechify" target="_blank" rel="noopener noreferrer">@SirTechify</a></p>
    `;
    container.appendChild(card);
  }

  function buildCard(ep) {
    const card = document.createElement('article');
    card.className = 'episode-card';
    if (ep.highlight) card.classList.add('highlight');

    const num = document.createElement('div');
    num.className = 'episode-num';
    num.textContent = `EP ${String(ep.ep).padStart(2, '0')}`;
    card.appendChild(num);

    const status = document.createElement('div');
    status.className = 'status-pill';
    status.dataset.status = 'published';
    status.innerHTML = `<span class="dot"></span>PUBLISHED`;
    card.appendChild(status);

    const title = document.createElement('h3');
    title.className = 'episode-title';
    title.textContent = ep.title;
    card.appendChild(title);

    const device = document.createElement('div');
    device.className = 'episode-device';
    device.textContent = ep.subtitle || ep.device || '';
    card.appendChild(device);

    const links = document.createElement('div');
    links.className = 'episode-links';
    links.appendChild(makeLink('YouTube', ep.youtube_url));
    links.appendChild(makeLink('Source', ep.github_url));
    card.appendChild(links);

    return card;
  }

  function makeLink(label, href) {
    const a = document.createElement('a');
    a.textContent = label;
    if (href) {
      a.href = href;
      a.target = '_blank';
      a.rel = 'noopener noreferrer';
    } else {
      a.classList.add('disabled');
      a.title = 'Not linked yet';
    }
    return a;
  }
})();
