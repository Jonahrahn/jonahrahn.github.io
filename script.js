// ============================================================
// Cinematic UX layer: scroll progress, reveals, sticky section
// marker, custom cursor, hero parallax. All respect
// prefers-reduced-motion and coarse-pointer devices.
// ============================================================

const reduceMotion = window.matchMedia('(prefers-reduced-motion: reduce)').matches;

// ---------- Nav: mobile toggle + scroll-spy --------------------------------
const nav = document.querySelector('.nav');
const toggle = document.querySelector('.nav__toggle');

if (toggle) {
  toggle.addEventListener('click', () => {
    const open = nav.classList.toggle('is-open');
    toggle.setAttribute('aria-expanded', String(open));
    toggle.textContent = open ? 'Close' : 'Menu';
  });
}
document.querySelectorAll('.nav__links a').forEach((link) => {
  link.addEventListener('click', () => {
    if (nav.classList.contains('is-open')) {
      nav.classList.remove('is-open');
      toggle.setAttribute('aria-expanded', 'false');
      toggle.textContent = 'Menu';
    }
  });
});

const sections = Array.from(document.querySelectorAll('section[id]'));
const navLinks = document.querySelectorAll('.nav__links a');

const spy = new IntersectionObserver(
  (entries) => {
    entries.forEach((entry) => {
      if (!entry.isIntersecting) return;
      const id = entry.target.id;
      navLinks.forEach((l) => {
        l.classList.toggle('is-active', l.getAttribute('href') === `#${id}`);
      });
    });
  },
  { rootMargin: '-45% 0px -50% 0px' }
);
sections.forEach((s) => spy.observe(s));

// ---------- Scroll progress bar --------------------------------------------
const progress = document.querySelector('.scroll-progress');
if (progress) {
  const update = () => {
    const max = document.documentElement.scrollHeight - window.innerHeight;
    const t = max > 0 ? window.scrollY / max : 0;
    progress.style.transform = `scaleX(${Math.min(1, Math.max(0, t))})`;
  };
  window.addEventListener('scroll', update, { passive: true });
  window.addEventListener('resize', update);
  update();
}

// ---------- Reveal on scroll -----------------------------------------------
const revealEls = document.querySelectorAll('[data-reveal]');
revealEls.forEach((el) => {
  const d = el.dataset.revealDelay;
  if (d) el.style.setProperty('--reveal-delay', `${d}ms`);
});

if (reduceMotion) {
  revealEls.forEach((el) => el.classList.add('is-revealed'));
} else {
  const revealObs = new IntersectionObserver(
    (entries) => {
      entries.forEach((entry) => {
        if (entry.isIntersecting) {
          entry.target.classList.add('is-revealed');
          revealObs.unobserve(entry.target);
        }
      });
    },
    { rootMargin: '0px 0px -8% 0px', threshold: 0.08 }
  );
  revealEls.forEach((el) => revealObs.observe(el));
  // Reveal anything above-the-fold immediately so the hero doesn't pop.
  requestAnimationFrame(() => {
    revealEls.forEach((el) => {
      const r = el.getBoundingClientRect();
      if (r.top < window.innerHeight * 0.95) el.classList.add('is-revealed');
    });
  });
}

// ---------- Hero parallax --------------------------------------------------
const heroInner = document.querySelector('.hero__grid');
if (heroInner && !reduceMotion) {
  let ticking = false;
  const onScroll = () => {
    if (ticking) return;
    ticking = true;
    requestAnimationFrame(() => {
      const y = window.scrollY;
      const hero = document.querySelector('.hero');
      if (hero && y < hero.offsetHeight) {
        const shift = y * 0.18;
        const fade = 1 - Math.min(0.65, y / hero.offsetHeight);
        heroInner.style.transform = `translate3d(0, ${-shift}px, 0)`;
        heroInner.style.opacity = String(fade);
      }
      ticking = false;
    });
  };
  window.addEventListener('scroll', onScroll, { passive: true });
}

// ---------- Work-item preview parallax -------------------------------------
const previews = document.querySelectorAll('.work-item__preview img');
if (previews.length && !reduceMotion) {
  let ticking = false;
  const onScroll = () => {
    if (ticking) return;
    ticking = true;
    requestAnimationFrame(() => {
      const viewH = window.innerHeight;
      previews.forEach((img) => {
        const rect = img.getBoundingClientRect();
        if (rect.bottom < 0 || rect.top > viewH) return;
        // Map scroll position to a -6%..+6% translate
        const center = rect.top + rect.height / 2;
        const t = (center - viewH / 2) / (viewH / 2); // -1..+1
        const shift = -t * 6; // px-ish percentage
        img.style.transform = `translate3d(0, ${shift}%, 0) scale(1.06)`;
      });
      ticking = false;
    });
  };
  window.addEventListener('scroll', onScroll, { passive: true });
  onScroll();
}

// ---------- View Transitions: smooth crossfade between same-origin links ---
if (document.startViewTransition && !reduceMotion) {
  document.addEventListener('click', (e) => {
    const a = e.target.closest('a');
    if (!a) return;
    if (a.target === '_blank') return;
    if (a.hasAttribute('download')) return;
    const href = a.getAttribute('href');
    if (!href) return;
    if (href.startsWith('#')) return;          // anchors stay native
    if (href.startsWith('http')) {
      const url = new URL(href);
      if (url.origin !== location.origin) return;
    }
    e.preventDefault();
    document.startViewTransition(() => {
      window.location.href = a.href;
    });
  });
}

// ---------- Subtle cursor accent: tiny lagging dot (no replacement) -------
if (!reduceMotion && window.matchMedia('(hover: hover) and (pointer: fine)').matches) {
  const dot = document.createElement('div');
  dot.className = 'cursor-accent';
  dot.setAttribute('aria-hidden', 'true');
  document.body.appendChild(dot);
  let x = -100, y = -100, cx = x, cy = y;
  window.addEventListener('mousemove', (e) => { x = e.clientX; y = e.clientY; });
  document.addEventListener('mouseover', (e) => {
    if (e.target.closest('a, button, .work-item, .capability')) dot.classList.add('is-hover');
  });
  document.addEventListener('mouseout', (e) => {
    if (e.target.closest('a, button, .work-item, .capability')) dot.classList.remove('is-hover');
  });
  const step = () => {
    cx += (x - cx) * 0.22;
    cy += (y - cy) * 0.22;
    dot.style.transform = `translate(${cx}px, ${cy}px) translate(-50%, -50%)`;
    requestAnimationFrame(step);
  };
  step();
}

// ---------- Footer year ----------------------------------------------------
const yearEl = document.getElementById('year');
if (yearEl) yearEl.textContent = String(new Date().getFullYear());
