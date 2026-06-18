/* ==========================================
   EduScheduler - Main JavaScript
   ========================================== */

document.addEventListener('DOMContentLoaded', function () {

  // ─── Sidebar Toggle ─────────────────────────
  const sidebar = document.getElementById('sidebar');
  const mainContent = document.getElementById('mainContent');
  const mobileSidebarToggle = document.getElementById('mobileSidebarToggle');
  const desktopSidebarToggle = document.getElementById('desktopSidebarToggle');
  const sidebarToggle = document.getElementById('sidebarToggle');

  // Mobile overlay
  let overlay = document.createElement('div');
  overlay.className = 'sidebar-overlay';
  document.body.appendChild(overlay);

  function openMobileSidebar() {
    sidebar?.classList.add('open');
    overlay.classList.add('show');
    document.body.style.overflow = 'hidden';
  }

  function closeMobileSidebar() {
    sidebar?.classList.remove('open');
    overlay.classList.remove('show');
    document.body.style.overflow = '';
  }

  mobileSidebarToggle?.addEventListener('click', openMobileSidebar);
  sidebarToggle?.addEventListener('click', closeMobileSidebar);
  overlay.addEventListener('click', closeMobileSidebar);

  // Desktop sidebar collapse
  let sidebarCollapsed = localStorage.getItem('sidebarCollapsed') === 'true';
  function applyDesktopSidebarState() {
    if (sidebar && mainContent) {
      if (sidebarCollapsed) {
        sidebar.style.width = '0';
        mainContent.style.marginLeft = '0';
      } else {
        sidebar.style.width = 'var(--sidebar-width)';
        mainContent.style.marginLeft = 'var(--sidebar-width)';
      }
    }
  }
  applyDesktopSidebarState();

  desktopSidebarToggle?.addEventListener('click', function () {
    sidebarCollapsed = !sidebarCollapsed;
    localStorage.setItem('sidebarCollapsed', sidebarCollapsed);
    applyDesktopSidebarState();
  });

  // ─── Auto-dismiss Alerts ────────────────────
  const alerts = document.querySelectorAll('.alert');
  alerts.forEach(function (alert) {
    setTimeout(function () {
      const bsAlert = new bootstrap.Alert(alert);
      bsAlert.close();
    }, 5000);
  });

  // ─── Fade-in-up Animation ───────────────────
  const cards = document.querySelectorAll('.stat-card, .card');
  cards.forEach(function (card, i) {
    card.style.animationDelay = `${i * 60}ms`;
    card.classList.add('fade-in-up');
  });

  // ─── Confirm Deletes ────────────────────────
  document.querySelectorAll('[data-confirm]').forEach(function (btn) {
    btn.addEventListener('click', function (e) {
      const msg = this.dataset.confirm || 'Are you sure?';
      if (!confirm(msg)) e.preventDefault();
    });
  });

  // ─── Form loading state ─────────────────────
  document.querySelectorAll('form').forEach(function (form) {
    form.addEventListener('submit', function () {
      const submitBtn = form.querySelector('[type="submit"]');
      if (submitBtn) {
        submitBtn.disabled = true;
        submitBtn.innerHTML = `<span class="spinner-border spinner-border-sm me-2" role="status"></span>Processing...`;
      }
    });
  });

  // ─── Tooltips ───────────────────────────────
  document.querySelectorAll('[data-bs-toggle="tooltip"]').forEach(function (el) {
    new bootstrap.Tooltip(el);
  });

  // ─── Active Nav ─────────────────────────────
  const currentPath = window.location.pathname;
  document.querySelectorAll('.sidebar-nav .nav-link').forEach(function (link) {
    if (link.getAttribute('href') === currentPath) {
      link.classList.add('active');
    }
  });

  // ─── Set Current Academic Year ──────────────
  fetch('/departments/academic-years/')
    .then(r => r.text())
    .then(html => {
      const match = html.match(/\d{4}-\d{4}/);
      const yearEl = document.getElementById('currentYear');
      if (match && yearEl) yearEl.textContent = match[0];
    }).catch(() => {});

  // ─── Timetable Cell Highlight on Hover ──────
  document.querySelectorAll('.timetable-cell').forEach(function (cell) {
    cell.addEventListener('mouseenter', function () {
      const row = this.closest('tr');
      const col = Array.from(this.closest('tr').children).indexOf(this);
      // Highlight column
      document.querySelectorAll('.timetable-grid td:nth-child(' + (col + 1) + ')').forEach(c => {
        c.style.background = 'rgba(92,107,192,0.07)';
      });
    });
    cell.addEventListener('mouseleave', function () {
      document.querySelectorAll('.timetable-grid td').forEach(c => {
        c.style.background = '';
      });
    });
  });

  console.log('%cEduScheduler initialized ✓', 'color:#3949ab;font-weight:bold;');
});
