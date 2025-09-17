document.addEventListener('DOMContentLoaded', function () {
  const btn = document.getElementById('togglePassword');
  const pwd = document.getElementById('password');
  if (!btn || !pwd) return;

  btn.addEventListener('click', function () {
    const isPassword = pwd.type === 'password';
    pwd.type = isPassword ? 'text' : 'password';
    btn.textContent = isPassword ? 'Hide' : 'Show';
    btn.setAttribute('aria-pressed', isPassword ? 'true' : 'false');
    btn.setAttribute('aria-label', isPassword ? 'Hide password' : 'Show password');
  });
});
