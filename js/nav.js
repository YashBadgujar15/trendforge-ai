


// ---- Helpers ----
function show(id) { var el = document.getElementById(id); if (el) el.style.display = 'block'; }
function hide(id) { var el = document.getElementById(id); if (el) el.style.display = 'none'; }

// ---- Toast helper ----
function showToast(msg, type) {
  type = type || 'default';
  var container = document.getElementById('toast-container');
  if (!container) {
    container = document.createElement('div');
    container.id = 'toast-container';
    document.body.appendChild(container);
  }
  var t = document.createElement('div');
  t.className = 'toast ' + type;
  var icons = { success: '✓', error: '✕', default: '✦' };
  t.innerHTML = '<span class="toast-icon">' + (icons[type] || '✦') + '</span><span>' + msg + '</span>';
  container.appendChild(t);
  setTimeout(function() {
    t.style.animation = 'slideOut 0.3s ease forwards';
    setTimeout(function() { if (t.parentNode) t.parentNode.removeChild(t); }, 300);
  }, 3000);
}

// ---- Navbar Dropdown Handlers ----
function toggleNavDropdown(id, e) {
  if (e) e.stopPropagation();
  var menu = document.getElementById(id);
  if (!menu) return;
  var isCurrentlyOpen = menu.style.display === 'block';
  closeAllNavDropdowns();
  if (!isCurrentlyOpen) {
    menu.style.display = 'block';
  }
}

function closeAllNavDropdowns() {
  document.querySelectorAll('.nav-dropdown-menu').forEach(function(m) {
    m.style.display = 'none';
  });
}

document.addEventListener('click', function(e) {
  if (!e.target.closest('.nav-dropdown-wrap')) {
    closeAllNavDropdowns();
  }
});

// Shared credits with localStorage persistence!
var currentCredits = (function() {
  try {
    var saved = localStorage.getItem('tf_credits');
    var val = saved !== null ? parseInt(saved, 10) : 50;
    if (isNaN(val) || val <= 0) {
      val = 50;
      localStorage.setItem('tf_credits', '50');
    }
    return val;
  } catch(e) { return 50; }
})();

function saveCredits() {
  try { localStorage.setItem('tf_credits', currentCredits); } catch(e) {}
}

function updateCreditUI() {
  var countEl = document.getElementById('credit-count');
  var dispEl = document.getElementById('credit-display');
  var barEl = document.getElementById('credit-bar');
  if (countEl) countEl.textContent = currentCredits;
  if (dispEl) dispEl.textContent = currentCredits;
  if (barEl) barEl.style.width = Math.min(100, (currentCredits / 50) * 100) + '%';
}

function addDemoCredits() {
  currentCredits += 50;
  saveCredits();
  updateCreditUI();
  showToast('Added +50 Free Demo Credits! Current balance: ' + currentCredits + ' 💎', 'success');
  addDynamicNotification(
    '+50 Credits Added',
    'Demo credits recharged successfully. New balance: ' + currentCredits + ' 💎.',
    '💎',
    'rgba(99,102,241,0.15)',
    '#6366f1'
  );
}

function deductCredits(amount) {
  if (currentCredits >= amount) {
    currentCredits -= amount;
  } else {
    currentCredits = 0;
  }
  saveCredits();
  updateCreditUI();
}

function markAllNotifsRead() {
  document.querySelectorAll('.notif-item.unread').forEach(function(el) {
    el.classList.remove('unread');
  });
  var dot = document.getElementById('notif-dot');
  if (dot) dot.style.display = 'none';
  var badge = document.getElementById('notif-count-badge');
  if (badge) badge.textContent = '0';
  showToast('Notifications marked as read ✓', 'default');
}

function clearAllNotifs() {
  var list = document.getElementById('notif-list');
  if (list) {
    list.innerHTML = '<div style="padding:24px 16px;text-align:center;color:var(--text-muted);font-size:12px">No notifications</div>';
  }
  var dot = document.getElementById('notif-dot');
  if (dot) dot.style.display = 'none';
  var badge = document.getElementById('notif-count-badge');
  if (badge) badge.textContent = '0';
  showToast('All notifications cleared', 'default');
}

function addDynamicNotification(title, desc, icon, iconBg, iconColor) {
  var list = document.getElementById('notif-list');
  if (!list) return;
  if (list.innerHTML.includes('No notifications')) {
    list.innerHTML = '';
  }
  var item = document.createElement('div');
  item.className = 'notif-item unread';
  item.innerHTML = 
    '<div class="notif-icon" style="background:' + iconBg + ';color:' + iconColor + '">' + icon + '</div>' +
    '<div class="notif-content">' +
      '<div class="notif-title">' + title + '</div>' +
      '<div class="notif-desc">' + desc + '</div>' +
      '<div class="notif-time">Just now</div>' +
    '</div>';
  list.insertBefore(item, list.firstChild);

  var dot = document.getElementById('notif-dot');
  if (dot) dot.style.display = 'block';
  var badge = document.getElementById('notif-count-badge');
  if (badge) {
    var cur = parseInt(badge.textContent || '0') + 1;
    badge.textContent = cur;
  }
}

// Initialize on page load
if (document.readyState === 'loading') {
  document.addEventListener('DOMContentLoaded', updateCreditUI);
} else {
  updateCreditUI();
}

