// FileSort Pro - Background Service Worker v2

const RULES = [
  { name: "CV / Resume",       pattern: "(CV|resume|curriculum)",          folder: "CV & Resumes",   icon: "📄" },
  { name: "Cover Letter",      pattern: "cover.?letter",                   folder: "Cover Letters",  icon: "✉️" },
  { name: "Invoice / Receipt", pattern: "(invoice|receipt|bill)",          folder: "Invoices",       icon: "🧾" },
  { name: "Images",            ext: ["jpg","jpeg","png","gif","webp","jfif","svg"], folder: "Images", icon: "🖼️" },
  { name: "Videos",            ext: ["mp4","mov","avi","mkv"],             folder: "Videos",         icon: "🎬" },
  { name: "Music",             ext: ["mp3","wav","flac","aac"],            folder: "Music",          icon: "🎵" },
  { name: "PDF Documents",     ext: ["pdf"],                               folder: "PDFs",           icon: "📕" },
  { name: "Word Documents",    ext: ["doc","docx"],                        folder: "Documents",      icon: "📝" },
  { name: "Spreadsheets",      ext: ["xls","xlsx","csv"],                  folder: "Spreadsheets",   icon: "📊" },
  { name: "Zip / Archives",    ext: ["zip","rar","7z","tar","gz"],         folder: "Archives",       icon: "📦" },
  { name: "Presentations",     ext: ["ppt","pptx"],                        folder: "Presentations",  icon: "📽️" },
  { name: "Code Files",        ext: ["js","py","html","css","ts","json"],  folder: "Code",           icon: "💻" },
  { name: "Installers",        ext: ["exe","msi","dmg","pkg"],             folder: "Installers",     icon: "⚙️" },
];

function matchRule(filename) {
  const name = filename.toLowerCase();
  const ext  = name.split('.').pop();
  for (const rule of RULES) {
    if (rule.pattern && new RegExp(rule.pattern, 'i').test(name)) return rule;
    if (rule.ext && rule.ext.includes(ext)) return rule;
  }
  return null;
}

// Keep service worker alive
chrome.runtime.onInstalled.addListener(() => {
  console.log('FileSort Pro installed');
});

chrome.runtime.onStartup.addListener(() => {
  console.log('FileSort Pro started');
});

// Listen for downloads
chrome.downloads.onChanged.addListener((delta) => {
  if (!delta.state || delta.state.current !== 'complete') return;

  chrome.downloads.search({ id: delta.id }, (downloads) => {
    if (!downloads || !downloads[0]) return;

    const filename = downloads[0].filename.split(/[\\/]/).pop();
    const matched  = matchRule(filename);
    if (!matched) return;

    // Show notification
    chrome.notifications.create({
      type: 'basic',
      iconUrl: 'icons/icon128.png',
      title: `FileSort Pro ${matched.icon}`,
      message: `"${filename}"`,
      contextMessage: `Belongs in: ${matched.folder}`,
      priority: 2,
      requireInteraction: false
    });

    // Save to history
    chrome.storage.local.get({ history: [], total: 0 }, (data) => {
      data.history.unshift({
        filename,
        folder: matched.folder,
        icon: matched.icon,
        time: new Date().toLocaleTimeString()
      });
      chrome.storage.local.set({
        history: data.history.slice(0, 20),
        total: data.total + 1
      });
    });
  });
});

// Notification click opens downloads folder
chrome.notifications.onClicked.addListener(() => {
  chrome.downloads.showDefaultFolder();
});
