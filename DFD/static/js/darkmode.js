// dark-mode toggle
const root   = document.documentElement;
const toggle = document.getElementById('theme-toggle');
const icon   = document.getElementById('theme-icon');

// init
if (localStorage.theme === 'dark' || (!('theme' in localStorage) && window.matchMedia('(prefers-color-scheme: dark)').matches)) {
  root.classList.add('dark');
  icon.innerHTML = '<path d="M10 2a8 8 0 108 8 8 8 0 00-8-8z"></path>'; // moon
} else {
  icon.innerHTML = '<circle cx="12" cy="12" r="5"></circle>';        // sun
}

toggle.addEventListener('click', () => {
  root.classList.toggle('dark');
  if (root.classList.contains('dark')) {
    localStorage.theme = 'dark';
    icon.innerHTML = '<path d="M10 2a8 8 0 108 8 8 8 0 00-8-8z"></path>';
  } else {
    localStorage.theme = 'light';
    icon.innerHTML = '<circle cx="12" cy="12" r="5"></circle>';
  }
  tippy(toggle); // refresh tooltip theme
});
