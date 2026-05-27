// ============================================================
// Cinematic UX layer — scroll progress, reveals, sticky section
// marker, custom cursor, hero parallax. All respect
// prefers-reduced-motion and coarse-pointer devices.
// ============================================================

const reduceMotion = window.matchMedia('(prefers-reduced-motion: reduce)').matches;
const finePointer = window.matchMedia('(hover: hover) and (pointer: fine)').matches;

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
const marker = document.querySelector('.section-marker');
const markerNum = marker?.querySelector('.section-marker__num');
const markerTitle = marker?.querySelector('.section-marker__title');

const SECTION_META = {
  home:         { num: '§ 00', title: 'Index' },
  about:        { num: '§ 01', title: 'About' },
  capabilities: { num: '§ 02', title: 'Capabilities' },
  work:         { num: '§ 03', title: 'Selected Work' },
  contact:      { num: '§ 04', title: 'Contact' },
};

const spy = new IntersectionObserver(
  (entries) => {
    entries.forEach((entry) => {
      if (!entry.isIntersecting) return;
      const id = entry.target.id;
      navLinks.forEach((l) => {
        l.classList.toggle('is-active', l.getAttribute('href') === `#${id}`);
      });
      const meta = SECTION_META[id];
      if (meta && marker) {
        markerNum.textContent = meta.num;
        markerTitle.textContent = meta.title;
        marker.classList.toggle('is-visible', id !== 'home');
      }
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
const heroInner = document.querySelector('.hero__inner');
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

// ---------- Custom cursor --------------------------------------------------
if (finePointer && !reduceMotion) {
  const ring = document.querySelector('.cursor-ring');
  const dot = document.querySelector('.cursor-dot');
  if (ring && dot) {
    document.body.classList.add('cursor-ready');
    let x = window.innerWidth / 2, y = window.innerHeight / 2;
    let rx = x, ry = y;
    const speed = 0.18;
    const step = () => {
      rx += (x - rx) * speed;
      ry += (y - ry) * speed;
      ring.style.transform = `translate(${rx}px, ${ry}px) translate(-50%, -50%)`;
      dot.style.transform = `translate(${x}px, ${y}px) translate(-50%, -50%)`;
      requestAnimationFrame(step);
    };
    window.addEventListener('mousemove', (e) => { x = e.clientX; y = e.clientY; });
    window.addEventListener('mouseleave', () => document.body.classList.remove('cursor-ready'));
    window.addEventListener('mouseenter', () => document.body.classList.add('cursor-ready'));

    // Magnet on interactive elements
    const hoverables = 'a, button, .work-item, .capability, .work-item__preview';
    document.addEventListener('mouseover', (e) => {
      if (e.target.closest(hoverables)) document.body.classList.add('cursor-hover');
    });
    document.addEventListener('mouseout', (e) => {
      if (e.target.closest(hoverables)) document.body.classList.remove('cursor-hover');
    });
    step();
  }
}

// ---------- Footer year ----------------------------------------------------
const yearEl = document.getElementById('year');
if (yearEl) yearEl.textContent = String(new Date().getFullYear());
