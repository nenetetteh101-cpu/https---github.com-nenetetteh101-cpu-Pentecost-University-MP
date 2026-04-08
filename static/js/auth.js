 // ── TAB SWITCHING ──
  function switchTab(tab) {
    document.getElementById('panel-login').classList.toggle('active', tab === 'login');
    document.getElementById('panel-signup').classList.toggle('active', tab === 'signup');
    document.getElementById('tab-login').classList.toggle('active', tab === 'login');
    document.getElementById('tab-signup').classList.toggle('active', tab === 'signup');
    clearErrors();
  }

  // ── PASSWORD TOGGLE ──
  function togglePw(id, btn) {
    const inp = document.getElementById(id);
    if (inp.type === 'password') {
      inp.type = 'text'; btn.textContent = '🙈';
    } else {
      inp.type = 'password'; btn.textContent = '👁️';
    }
  }

  // ── PASSWORD STRENGTH ──
  function checkStrength(val) {
    const segs = [document.getElementById('s1'), document.getElementById('s2'), document.getElementById('s3'), document.getElementById('s4')];
    const lbl = document.getElementById('strength-label');
    segs.forEach(s => { s.className = 'strength-seg'; });

    if (!val) { lbl.textContent = ''; return; }
    let score = 0;
    if (val.length >= 8) score++;
    if (/[A-Z]/.test(val)) score++;
    if (/[0-9]/.test(val)) score++;
    if (/[^A-Za-z0-9]/.test(val)) score++;

    const labels = ['', 'Weak', 'Fair', 'Good', 'Strong'];
    const classes = ['', 'weak', 'weak', 'medium', 'strong'];
    lbl.textContent = labels[score];
    lbl.style.color = score <= 1 ? 'var(--error)' : score === 2 ? '#e8c96a' : 'var(--accent2)';
    for (let i = 0; i < score; i++) segs[i].classList.add(classes[score]);
  }

  // ── SHOW / HIDE ERRORS ──
  function showErr(id, show) {
    const el = document.getElementById(id);
    if (el) el.classList.toggle('show', show);
  }
  function markInput(id, error) {
    const el = document.getElementById(id);
    if (el) el.classList.toggle('error', error);
  }
  function clearErrors() {
    document.querySelectorAll('.field-error').forEach(e => e.classList.remove('show'));
    document.querySelectorAll('input, select').forEach(e => e.classList.remove('error'));
  }

  // ── TOAST ──
  function showToast(msg, icon = '✅') {
    const t = document.getElementById('toast');
    document.getElementById('toast-msg').textContent = msg;
    document.getElementById('toast-icon').textContent = icon;
    t.classList.add('show');
    setTimeout(() => t.classList.remove('show'), 3500);
  }

  // ── LOGIN HANDLER ──
  function handleLogin() {
    clearErrors();
    const email = document.getElementById('login-email').value.trim();
    const pw = document.getElementById('login-password').value;
    let valid = true;

    if (!email || email.length < 3) {
      showErr('login-email-err', true); markInput('login-email', true); valid = false;
    }
    if (!pw) {
      showErr('login-pw-err', true); markInput('login-password', true); valid = false;
    }
    if (!valid) return;

    const btn = document.getElementById('login-btn');
    btn.classList.add('loading');
    btn.textContent = 'Logging in…';
    setTimeout(() => {
      btn.classList.remove('loading');
      btn.textContent = 'Log In to Campus';
      showToast('Welcome back! Redirecting to your dashboard…', '🎉');
    }, 1800);
  }

  // ── SIGNUP HANDLER ──
  function handleSignup() {
    clearErrors();
    let valid = true;

    const fname = document.getElementById('su-fname').value.trim();
    const lname = document.getElementById('su-lname').value.trim();
    const email = document.getElementById('su-email').value.trim();
    const username = document.getElementById('su-username').value.trim();
    const pw = document.getElementById('su-password').value;
    const confirm = document.getElementById('su-confirm').value;
    const termsEl = document.getElementById('su-terms');
    const terms = termsEl.checked;

    if (!fname) { showErr('su-fname-err', true); markInput('su-fname', true); valid = false; }
    if (!lname) { showErr('su-lname-err', true); markInput('su-lname', true); valid = false; }
    if (!email || !/\S+@\S+\.\S+/.test(email)) { showErr('su-email-err', true); markInput('su-email', true); valid = false; }
    if (!username || username.length < 3 || !/^[a-zA-Z0-9_]+$/.test(username)) { showErr('su-username-err', true); markInput('su-username', true); valid = false; }
    if (!pw || pw.length < 8) { showErr('su-pw-err', true); markInput('su-password', true); valid = false; }
    if (pw && confirm && pw !== confirm) { showErr('su-confirm-err', true); markInput('su-confirm', true); valid = false; }
    if (!terms) {
      showErr('su-terms-err', true);
      termsEl.classList.add('must-check');
      const cg = termsEl.closest('.check-group');
      cg.classList.remove('required-shake');
      void cg.offsetWidth; // reflow to restart animation
      cg.classList.add('required-shake');
      setTimeout(() => { termsEl.classList.remove('must-check'); cg.classList.remove('required-shake'); }, 600);
      valid = false;
    }

    if (!valid) return;

    const btn = document.getElementById('signup-btn');
    btn.classList.add('loading');
    btn.textContent = 'Creating account…';
    setTimeout(() => {
      btn.classList.remove('loading');
      btn.textContent = 'Create My Account';
      showToast('Account created! Check your email to verify.', '🎓');
    }, 2000);
  }

  // ── SOCIAL AUTH ──
  function handleSocial(provider) {
    showToast(`Connecting to ${provider}…`, provider === 'Google' ? '🔵' : '⚫');
  }

  // Auto-switch tab via URL hash
  if (window.location.hash === '#signup') switchTab('signup');