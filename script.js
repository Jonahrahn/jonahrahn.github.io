const navToggle = document.querySelector('.nav__toggle');
const navLinks = document.querySelector('.nav__links');
const navLinkItems = document.querySelectorAll('.nav__links a');
const scrollCue = document.querySelector('.scroll-cue');

navToggle.addEventListener('click', () => {
  const expanded = navToggle.getAttribute('aria-expanded') === 'true';
  navToggle.setAttribute('aria-expanded', !expanded);
  navLinks.classList.toggle('open');
});

navLinkItems.forEach((link) => {
  link.addEventListener('click', () => {
    navLinks.classList.remove('open');
    navToggle.setAttribute('aria-expanded', 'false');
  });
});

if (scrollCue) {
  scrollCue.addEventListener('click', () => {
    const target = scrollCue.dataset.scrollTarget;
    document.querySelector(target)?.scrollIntoView({ behavior: 'smooth' });
  });
}

const observer = new IntersectionObserver(
  (entries) => {
    entries.forEach((entry) => {
      if (entry.isIntersecting) {
        entry.target.classList.add('visible');
        observer.unobserve(entry.target);
      }
    });
  },
  {
    threshold: 0.15,
  }
);

document.querySelectorAll('.reveal').forEach((el) => observer.observe(el));
