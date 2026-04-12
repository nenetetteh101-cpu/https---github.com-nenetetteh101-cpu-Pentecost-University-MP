
function toggleAcc(btn) {
    const item = btn.closest('.acc-item');
    const isOpen = item.classList.contains('open');
    // Close all
    document.querySelectorAll('.acc-item.open').forEach(i => i.classList.remove('open'));
    if (!isOpen) item.classList.add('open');
  }

  // Sidebar active
  const faqSections = document.querySelectorAll('.faq-section[id]');
  const sideLinks = document.querySelectorAll('.sidebar-list a');
  const sideObs = new IntersectionObserver((entries) => {
    entries.forEach(e => {
      if (e.isIntersecting) {
        sideLinks.forEach(l => l.classList.remove('active'));
        const a = document.querySelector(`.sidebar-list a[href="#${e.target.id}"]`);
        if (a) a.classList.add('active');
      }
    });
  }, { rootMargin: '-20% 0px -65% 0px' });
  faqSections.forEach(s => sideObs.observe(s));

  // Search
  const allFAQs = [];
  document.querySelectorAll('.acc-item').forEach(item => {
    const q = item.querySelector('.acc-question').textContent;
    const a = item.querySelector('.acc-content').textContent;
    const section = item.closest('.faq-section');
    const sectionId = section ? section.id : '';
    const sectionTitle = section ? section.querySelector('.faq-section-title').textContent.trim() : '';
    allFAQs.push({ q, a, sectionId, sectionTitle });
  });

  function handleSearch(val) {
    const resultsEl = document.getElementById('searchResults');
    if (!val || val.length < 2) { resultsEl.classList.remove('show'); return; }
    const lower = val.toLowerCase();
    const matches = allFAQs.filter(f => f.q.toLowerCase().includes(lower) || f.a.toLowerCase().includes(lower)).slice(0, 6);
    if (!matches.length) { resultsEl.innerHTML = '<div class="search-result-item"><span class="sr
    