document.querySelectorAll('.password-toggle').forEach(button=>button.addEventListener('click',()=>{const inputs=button.form.querySelectorAll('input[name=password],input[name=confirm]'); const show=inputs[0].type==='password'; inputs.forEach(i=>i.type=show?'text':'password');button.textContent=show?'Hide password':'Show password';}));
document.querySelectorAll('form[data-confirm]').forEach(form=>form.addEventListener('submit',event=>{if(!confirm(form.dataset.confirm))event.preventDefault();}));
// Progressive decoration: forms and navigation still work without JavaScript.
const reducedMotion = window.matchMedia('(prefers-reduced-motion: reduce)');
const publicIntro = document.querySelector('.landing > div:first-child, .signup-layout > div:first-child');
if (publicIntro) {
 const scene = document.createElement('div');
 scene.className = 'prism-scene';
 scene.setAttribute('aria-hidden', 'true');
 const core = document.createElement('div'); core.className = 'prism-core';
 ['</>', '{ }', 'dg.', '+', '*', '01'].forEach(symbol => {
  const face = document.createElement('span'); face.className = 'prism-face'; face.textContent = symbol; core.append(face);
 });
 scene.append(core);
 [['one', '01', 'Start with curiosity'], ['two', '02', 'Build something yours']].forEach(([position, number, text]) => {
  const chip = document.createElement('span'); chip.className = 'orbit-chip ' + position;
  const label = document.createElement('b'); label.textContent = number; chip.append(label, text); scene.append(chip);
 });
 const caption = document.createElement('span'); caption.className = 'scene-caption'; caption.textContent = 'LEARN / BUILD / BELONG'; scene.append(caption);
 const oldArt = publicIntro.querySelector('.terminal, .quote');
 if (oldArt) oldArt.replaceWith(scene); else publicIntro.append(scene);
}
// The stored preference is optional; blocked storage must never break forms.
const themeButton = document.createElement('button');
themeButton.type = 'button'; themeButton.className = 'theme-toggle';
let selectedTheme = 'dark';
try { const saved = localStorage.getItem('dg-theme'); if (saved === 'light' || saved === 'dark') selectedTheme = saved; } catch (_) {}
function applyTheme(theme) {
 document.documentElement.dataset.theme = theme;
 themeButton.textContent = theme === 'dark' ? 'Light theme' : 'Dark theme';
 themeButton.setAttribute('aria-label', 'Switch to ' + (theme === 'dark' ? 'light' : 'dark') + ' theme');
 themeButton.setAttribute('aria-pressed', String(theme === 'light'));
 document.querySelector('meta[name="theme-color"]')?.setAttribute('content', theme === 'dark' ? '#090a0d' : '#f4f5f8');
}
applyTheme(selectedTheme);
(document.querySelector('.innovation-nav') || document.querySelector('header') || document.body).append(themeButton);
themeButton.addEventListener('click', () => {
 selectedTheme = document.documentElement.dataset.theme === 'dark' ? 'light' : 'dark'; applyTheme(selectedTheme);
 try { localStorage.setItem('dg-theme', selectedTheme); } catch (_) {}
});
function updateCountdowns() {
 document.querySelectorAll('[data-countdown]').forEach(el => {
  const remaining = Date.parse(el.dataset.countdown) - Date.now();
  if (!Number.isFinite(remaining)) { el.textContent = 'Check event time'; return; }
  if (remaining <= 0) { el.textContent = 'Started'; return; }
  const minutes = Math.floor(remaining / 60000), hours = Math.floor(minutes / 60), days = Math.floor(hours / 24);
  el.textContent = days ? `${days}d ${hours % 24}h remaining` : hours ? `${hours}h ${minutes % 60}m remaining` : `${minutes}m remaining`;
 });
}
updateCountdowns();
if (document.querySelector('[data-countdown]')) setInterval(updateCountdowns, 60000);
document.querySelectorAll('main > *, .grid > .card').forEach(el => el.classList.add('reveal'));
const pageLabels = {events:'DISCOVER / CONNECT / CREATE',resources:'CURIOSITY IS YOUR SUPERPOWER',community:'GOOD IDEAS START WITH A CONVERSATION',mentorship:'A LITTLE GUIDANCE GOES A LONG WAY',members:'DIFFERENT STORIES. SHARED POSSIBILITIES.',profile:'YOUR STORY, STILL UNFOLDING',admin:'THE PEOPLE BEHIND THE POSSIBILITIES'};
const heading = document.querySelector('.page-heading');
if (heading && pageLabels[document.body.dataset.page]) {
 const label = document.createElement('div'); label.className = 'page-decoration'; label.textContent = pageLabels[document.body.dataset.page]; heading.prepend(label);
}
const adminLink = document.querySelector('.sidebar nav a[href="admin.php"]');
if (adminLink && document.body.dataset.page === 'admin') adminLink.classList.add('active');
document.querySelectorAll('.sidebar nav a.active').forEach(el => el.setAttribute('aria-current', 'page'));
document.querySelectorAll('.password-toggle').forEach(button => button.setAttribute('aria-pressed', 'false'));
document.querySelectorAll('.password-toggle').forEach(button => button.addEventListener('click', () => button.setAttribute('aria-pressed', String(button.form.querySelector('input[name=password]').type === 'text'))));
const signupPassword = document.querySelector('body[data-page="signup"] input[name="password"]');
if (signupPassword) {
 const meter = document.createElement('progress'); meter.max = 4; meter.value = 0; meter.setAttribute('aria-label','Password strength');
 const note = document.createElement('p'); note.className = 'strength-note'; note.textContent = 'Use at least 10 characters, letters and a number.';
 signupPassword.closest('label').after(meter, note);
 signupPassword.addEventListener('input', () => {
  const value = signupPassword.value;
  const score = Number(value.length >= 10) + Number(/[A-Za-z]/.test(value) && /[0-9]/.test(value)) + Number(/[^A-Za-z0-9]/.test(value)) + Number(value.length >= 14);
  meter.value = score;
  note.textContent = !value ? 'Use at least 10 characters, letters and a number.' : ['Keep typing', 'Keep building your password', 'Meets some strength checks', 'Good password strength', 'Strong password'][score];
 });
}
if (window.matchMedia('(pointer: fine)').matches) {
 document.querySelectorAll('.auth').forEach(panel => {
  panel.addEventListener('pointermove', event => {
   if (reducedMotion.matches) return;
   const box = panel.getBoundingClientRect();
   const x = (event.clientX-box.left)/box.width-.5, y = (event.clientY-box.top)/box.height-.5;
   panel.style.transform = `perspective(1200px) rotateX(${-y*2}deg) rotateY(${x*2}deg)`;
  });
  panel.addEventListener('pointerleave', () => panel.style.removeProperty('transform'));
 });
}
