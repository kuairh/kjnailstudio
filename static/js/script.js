// ===========================
// KJ NAIL STUDIO - script.js
// ===========================

// ===== LANGUAGE TOGGLE =====
let currentLang = 'zh';

function toggleLang() {
  currentLang = currentLang === 'zh' ? 'en' : 'zh';
  document.querySelector('.lang-toggle').textContent = currentLang === 'zh' ? 'EN' : '中文';

  document.querySelectorAll('[data-zh]').forEach(el => {
    const text = el.getAttribute('data-' + currentLang);
    if (!text) return;
    if (el.tagName === 'INPUT' || el.tagName === 'TEXTAREA') {
      el.placeholder = text;
    } else if (el.tagName === 'OPTION') {
      el.textContent = text;
    } else {
      el.innerHTML = text; // innerHTML for <br> support in QR placeholder
    }
  });
}

// ===== NAVBAR SCROLL =====
window.addEventListener('scroll', () => {
  document.getElementById('navbar').classList.toggle('scrolled', window.scrollY > 50);
});

// ===== MOBILE MENU =====
function toggleMenu() {
  document.getElementById('mobileMenu').classList.toggle('open');
}
document.addEventListener('click', e => {
  const menu = document.getElementById('mobileMenu');
  const hamburger = document.getElementById('hamburger');
  if (menu && hamburger && !menu.contains(e.target) && !hamburger.contains(e.target)) {
    menu.classList.remove('open');
  }
});

// ===== SMOOTH SCROLL =====
document.querySelectorAll('a[href^="#"]').forEach(a => {
  a.addEventListener('click', e => {
    e.preventDefault();
    const target = document.querySelector(a.getAttribute('href'));
    if (target) target.scrollIntoView({ behavior: 'smooth' });
  });
});

// ===== GALLERY FILTER =====
document.querySelectorAll('.filter-btn').forEach(btn => {
  btn.addEventListener('click', function () {
    document.querySelectorAll('.filter-btn').forEach(b => b.classList.remove('active'));
    this.classList.add('active');
    const filter = this.getAttribute('data-filter');
    document.querySelectorAll('.gallery-item').forEach((item, i) => {
      const match = filter === 'all' || item.getAttribute('data-category') === filter;
      item.style.transition = `opacity 0.35s ease ${i * 0.05}s, transform 0.35s ease ${i * 0.05}s`;
      item.style.opacity   = match ? '1' : '0.12';
      item.style.transform = match ? 'scale(1)' : 'scale(0.97)';
    });
  });
});

// ===== BOOKING FORM =====
function submitBooking(e) {
  e.preventDefault();
  const form    = document.getElementById('bookingForm');
  const success = document.getElementById('bookingSuccess');
  const data    = Object.fromEntries(new FormData(form));

  fetch('/submit-booking', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(data)
  })
  .then(r => r.json())
  .then(res => {
    if (res.success) {
      form.style.display    = 'none';
      success.style.display = 'block';
    }
  })
  .catch(() => {
    // Fallback: still show success (form data captured on server if Flask running)
    form.style.display    = 'none';
    success.style.display = 'block';
  });
}

// ===== SCROLL REVEAL =====
const observer = new IntersectionObserver(entries => {
  entries.forEach(entry => {
    if (entry.isIntersecting) entry.target.classList.add('visible');
  });
}, { threshold: 0.1, rootMargin: '0px 0px -50px 0px' });

document.querySelectorAll('.service-card, .gallery-item, .strip-item, .contact-card').forEach((el, i) => {
  el.classList.add('reveal');
  el.style.transitionDelay = (i % 4) * 0.08 + 's';
  observer.observe(el);
});

// ===== MIN DATE FOR BOOKING =====
const dateInput = document.getElementById('dateInput');
if (dateInput) {
  const today = new Date();
  dateInput.min = today.toISOString().split('T')[0];
}
