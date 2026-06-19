// FileSort Pro - Popup Script

const DEFAULT_RULES = [
  { name: "CV / Resume",        pattern: "(CV|resume|curriculum)",   folder: "CV & Resumes",   icon: "📄", enabled: true },
  { name: "Cover Letter",       pattern: "cover.?letter",            folder: "Cover Letters",  icon: "✉️",  enabled: true },
  { name: "Invoice / Receipt",  pattern: "(invoice|receipt|bill)",   folder: "Invoices",       icon: "🧾", enabled: true },
  { name: "Images",             ext: ["jpg","jpeg","png","gif","webp","svg"], folder: "Images", icon: "🖼️", enabled: true },
  { name: "Videos",             ext: ["mp4","mov","avi","mkv"],       folder: "Videos",         icon: "🎬", enabled: true },
  { name: "Music",              ext: ["mp3","wav","flac","aac"],      folder: "Music",          icon: "🎵", enabled: true },
  { name: "PDF Documents",      ext: ["pdf"],                        folder: "PDFs",           icon: "📕", enabled: true },
  { name: "Word Documents",     ext: ["doc","docx"],                 folder: "Documents",      icon: "📝", enabled: true },
  { name: "Spreadsheets",       ext: ["xls","xlsx","csv"],           folder: "Spreadsheets",   icon: "📊", enabled: true },
  { name: "Zip / Archives",     ext: ["zip","rar","7z","tar","gz"],  folder: "Archives",       icon: "📦", enabled: true },
  { name: "Presentations",      ext: ["ppt","pptx"],                 folder: "Presentations",  icon: "📽️", enabled: true },
  { name: "Code Files",         ext: ["js","py","html","css","ts","json"], folder: "Code",     icon: "💻", enabled: true },
  { name: "Installers",         ext: ["exe","msi","dmg","pkg"],      folder: "Installers",     icon: "⚙️", enabled: true },
];

// ── Tab switching ─────────────────────────────────────────────────
document.querySelectorAll('.tab').forEach(tab => {
  tab.addEventListener('click', () => {
    document.querySelectorAll('.tab').forEach(t => t.classList.remove('active'));
    document.querySelectorAll('.panel').forEach(p => p.classList.remove('active'));
    tab.classList.add('active');
    document.getElementById(tab.dataset.tab).classList.add('active');
  });
});

// ── Master toggle ─────────────────────────────────────────────────
const masterToggle = document.getElementById('masterToggle');
const toggleLabel  = document.getElementById('toggleLabel');

chrome.storage.sync.get({ enabled: true }, data => {
  masterToggle.checked = data.enabled;
  toggleLabel.textContent = data.enabled ? 'ON' : 'OFF';
});

masterToggle.addEventListener('change', () => {
  const enabled = masterToggle.checked;
  toggleLabel.textContent = enabled ? 'ON' : 'OFF';
  chrome.storage.sync.set({ enabled });
});

// ── Load history ──────────────────────────────────────────────────
function loadHistory() {
  chrome.storage.local.get({ history: [] }, data => {
    const list = document.getElementById('historyList');
    const history = data.history;

    // Update stats
    document.getElementById('totalSorted').textContent = history.length;
    const folders = new Set(history.map(h => h.folder));
    document.getElementById('totalFolders').textContent = folders.size;

    if (history.length === 0) {
      list.innerHTML = `
        <div class="empty-state">
          <div class="empty-icon">📥</div>
          <p>No files sorted yet.<br>Download something and FileSort Pro<br>will organize it automatically!</p>
        </div>`;
      return;
    }

    list.innerHTML = history.map(item => `
      <div class="history-item">
        <span class="history-icon">${item.icon}</span>
        <div class="history-info">
          <div class="history-name">${item.filename}</div>
          <div class="history-folder">→ ${item.folder}</div>
        </div>
        <span class="history-time">${item.time}</span>
      </div>
    `).join('');
  });
}

loadHistory();

// ── Clear history ─────────────────────────────────────────────────
document.getElementById('clearBtn').addEventListener('click', () => {
  chrome.storage.local.set({ history: [] }, loadHistory);
});

// ── Load rules ────────────────────────────────────────────────────
chrome.storage.sync.get({ rules: DEFAULT_RULES }, data => {
  const list = document.getElementById('rulesList');
  list.innerHTML = data.rules.map((rule, i) => `
    <div class="rule-item">
      <span class="rule-icon">${rule.icon}</span>
      <div class="rule-info">
        <div class="rule-name">${rule.name}</div>
        <div class="rule-folder">→ ${rule.folder}</div>
      </div>
      <label class="rule-toggle">
        <input type="checkbox" data-index="${i}" ${rule.enabled !== false ? 'checked' : ''}>
        <span class="rule-slider"></span>
      </label>
    </div>
  `).join('');

  // Rule toggles
  list.querySelectorAll('input[data-index]').forEach(input => {
    input.addEventListener('change', () => {
      const rules = data.rules;
      rules[input.dataset.index].enabled = input.checked;
      chrome.storage.sync.set({ rules });
    });
  });
});
