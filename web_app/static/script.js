/* Updated script.js
   - Navbar (Inforay) behavior
   - Center category chips
   - Left sidebar chips + counts & active highlight
   - Search (typing, Enter, button)
   - Dark mode toggle (top-right)
   - Hamburger toggles left sidebar for small screens
   - 3 cards per row (CSS) + infinite scroll
   - Hero rotator (6s)
*/

const API_ALL = "/api/articles?limit=200";
const PLACEHOLDER = "/static/fallbacks/default.jpg";

const CATEGORIES = ["Technology","Politics","Business","Sports","Health"];

let allArticles = [];
let page = 1;
const pageSize = 20;
let infiniteLoading = false;
let heroInterval = null;
let activeCategory = null;

const el = id => document.getElementById(id);

/* ---------- DOMContentLoaded ---------- */
document.addEventListener("DOMContentLoaded", () => {
  // wire buttons
  safeClick("darkToggleTop", toggleDarkTop);
  safeClick("hamburgerTop", toggleHamburger);
  safeClick("searchBtn", onSearchBtn);
  safeClick("allNewsBtn", () => { activeCategory = null; renderArticlesReset(); highlightSidebar(); });

  // search input events
  const si = el("searchInput");
  if (si) {
    si.addEventListener("input", onSearchInput);
    si.addEventListener("keydown", (e) => { if (e.key === "Enter") performSearch(e.target.value); });
  }

  // build categories UI initially (center chips + sidebar)
  buildCategoryChips();
  renderSidebarCategories();

  // restore dark mode
  if (localStorage.getItem("dark") === "true") document.body.classList.add("dark");

  // initial fetch
  fetchArticles();

  // infinite scroll
  window.addEventListener("scroll", () => {
    const scrollPos = window.innerHeight + window.scrollY;
    const threshold = document.body.offsetHeight - 700;
    if (scrollPos >= threshold) loadMoreArticles();
  });
});

/* ---------- Fetch articles ---------- */
async function fetchArticles(){
  showSkeleton(true);
  try {
    const res = await fetch(API_ALL);
    if (!res.ok) throw new Error("Fetch failed");
    const data = await res.json();
    allArticles = Array.isArray(data) ? data : [];
    page = 1;
    renderTrendingCarousel();
    startHeroRotator();
    renderArticles(allArticles.slice(0,pageSize));
    renderSidebarCategories();
    highlightSidebar();
  } catch (e) {
    console.error(e);
    renderArticles([]);
  } finally {
    showSkeleton(false);
  }
}

/* ---------- Render articles (append support) ---------- */
function renderArticles(list, append=false){
  const container = el("articles");
  if (!container) return;
  if (!append) container.innerHTML = "";
  container.classList.remove("d-none");

  if (!list || list.length === 0) {
    container.innerHTML = `<div class="glass-card p-3">No articles found</div>`;
    return;
  }

  list.forEach((a, idx) => {
    const thumb = a.image || a.urlToImage || PLACEHOLDER;
    const card = document.createElement("div");
    card.className = "news-card glass-card";

    card.innerHTML = `
      <div class="thumb-wrap">
    <div class="thumb-wrap">
    <img class="news-thumb" src="${thumb}" 
         onerror="this.src='${PLACEHOLDER}'" />
</div>

</div>

      <h3 class="news-title">${escapeHtml(a.title || "")}</h3>
      <p class="news-summary">${escapeHtml((a.summary || a.content || "").slice(0,320))}${(a.summary||a.content||"").length>320?"…":""}</p>
      <div class="d-flex justify-content-between align-items-center mt-2">
        <div class="d-flex align-items-center">
          ${moodDot(a.sentiment)}
          <span class="badge-cat">${escapeHtml(a.category || "N/A")}</span>
        </div>
        <small class="text-muted">${formatDate(a.publishedAt)}</small>
      </div>
      <div class="insights-bar">
        <span class="insight-chip">⏱ ${estimateReadTime(a)}</span>
        <span class="insight-chip">${sentimentLabel(a.sentiment)}</span>
        <span class="insight-chip">🔥 ${trendScore(a)}</span>
      </div>
    `;

    card.addEventListener("click", () => openModal(a));
    addTilt(card);
    container.appendChild(card);
  });
}

/* ---------- Infinite scroll loader ---------- */
function loadMoreArticles(){
  if (infiniteLoading) return;
  infiniteLoading = true;
  const start = page * pageSize;
  const batch = allArticles.slice(start, start + pageSize);
  if (batch.length) {
    renderArticles(batch, true);
    page++;
  }
  infiniteLoading = false;
}

/* ---------- Hero rotator ---------- */
function startHeroRotator(){
  const dyn = el("heroDynamic");
  if (!dyn) return;
  const headlines = allArticles.slice(0,20).map(a=>a.title).filter(Boolean);
  if (!headlines.length) { dyn.innerText = "Top stories will appear here"; return; }
  clearInterval(heroInterval);
  let i = 0;
  dyn.innerText = headlines[0];
  heroInterval = setInterval(()=>{
    dyn.style.opacity = 0;
    setTimeout(()=>{
      dyn.innerText = headlines[(i+1)%headlines.length];
      dyn.style.opacity = 1;
      i++;
    },420);
  },6000);
}

/* ---------- Categories UI (center + sidebar) ---------- */
function buildCategoryChips(){
  const center = el("categoryChipsCenter");
  if (!center) return;
  center.innerHTML = "";
  CATEGORIES.forEach(cat => {
    const b = document.createElement("button");
    b.className = "chip-center";
    b.innerText = cat;
    b.onclick = ()=> { activeCategory = cat; renderArticlesReset(); highlightSidebar(); };
    center.appendChild(b);
  });
}

/* sidebar categories (with counts) */
function renderSidebarCategories(){
  const target = el("categorySidebar");
  if (!target) return;
  target.innerHTML = "";
  const freq = getCategoryFrequency();
  CATEGORIES.forEach(cat => {
    const count = freq[cat] || 0;
    const d = document.createElement("div");
    d.className = "chip-pill";
    d.innerText = `${cat} • ${count}`;
    d.onclick = ()=> { activeCategory = cat; renderArticlesReset(); highlightSidebar(); };
    if (activeCategory === cat) d.classList.add("active");
    target.appendChild(d);
  });
}

/* highlight correct in sidebar */
function highlightSidebar(){
  const nodes = document.querySelectorAll("#categorySidebar .chip-pill");
  nodes.forEach(n => n.classList.remove("active"));
  if (!activeCategory) return;
  nodes.forEach(n => { if (n.innerText.startsWith(activeCategory)) n.classList.add("active"); });
}

/* trending (sidebar + carousel) */
function renderTrendingCarousel(){
  const c = el("trendingCarousel");
  if (!c) return;
  c.innerHTML = "";
  const freq = getCategoryFrequency();
  Object.entries(freq).sort((a,b)=>b[1]-a[1]).slice(0,8).forEach(([cat,count])=>{
    const pill = document.createElement("div"); pill.className="trend-pill"; pill.innerText=`${cat} • ${count}`;
    pill.onclick = ()=> { activeCategory = cat; renderArticlesReset(); highlightSidebar(); };
    c.appendChild(pill);
  });

  const ts = el("trendingSidebar");
  if (ts) {
    ts.innerHTML = "";
    Object.entries(freq).sort((a,b)=>b[1]-a[1]).slice(0,6).forEach(([cat,count])=>{
      const d = document.createElement("div"); d.className="chip-pill"; d.innerText=`${cat} • ${count}`;
      d.onclick = ()=> { activeCategory = cat; renderArticlesReset(); highlightSidebar(); };
      ts.appendChild(d);
    });
  }
}

/* ---------- Search ---------- */
function onSearchInput(e){
  const q = e.target.value.trim();
  if (!q) { if (!activeCategory) renderArticlesReset(); return; }
  performSearch(q);
}
function onSearchBtn(){ const v = el("searchInput").value.trim(); performSearch(v); }

function performSearch(q){
  if (!q) { renderArticlesReset(); return; }
  const lowered = q.toLowerCase();
  const filtered = allArticles.filter(a => {
    const title = (a.title||"").toLowerCase();
    const summary = (a.summary||a.content||"").toLowerCase();
    const cat = (a.category||"").toLowerCase();
    return title.includes(lowered) || summary.includes(lowered) || cat.includes(lowered);
  });
  page = 1; renderArticles(filtered.slice(0,pageSize)); // reset paging for results
}

/* ---------- Utilities ---------- */
function getCategoryFrequency(){
  const freq = {};
  allArticles.forEach(a => { const c = a.category || "Other"; freq[c] = (freq[c]||0) + 1; });
  return freq;
}

function renderArticlesReset(){
  page = 1;
  let list = allArticles;
  if (activeCategory) list = allArticles.filter(a => (a.category||"") === activeCategory);
  renderArticles(list.slice(0,pageSize));
  renderSidebarCategories();
}

/* ---------- Modal & helpers ---------- */
function openModal(a) {
  el("modalTitle").innerText = a.title || "";
  el("modalSummary").innerText = a.summary || a.content || "";
  el("modalMeta").innerText = `${a.source || ""} • ${formatDate(a.publishedAt)}`;
  el("modalLink").href = a.url || "#";
  el("modalImage").src = a.image || a.urlToImage || PLACEHOLDER;

  if (window.bootstrap && el("articleModal")) {
    const modal = new bootstrap.Modal(el("articleModal"));
    modal.show();
  }
}


/* small helpers */
function escapeHtml(s=""){ return String(s||"").replaceAll("&","&amp;").replaceAll("<","&lt;").replaceAll(">","&gt;"); }
function formatDate(d){ try{return new Date(d).toLocaleString()}catch(e){return d||""} }
function estimateReadTime(a){ const words = (a.summary||a.content||"").split(/\s+/).length; return `${Math.max(1,Math.round(words/200))} min`; }
function moodDot(s){ if(s==="Positive") return `<span class="mood-dot mood-positive"></span>`; if(s==="Negative") return `<span class="mood-dot mood-negative"></span>`; return `<span class="mood-dot mood-neutral"></span>`; }
function sentimentLabel(s){ if(s==="Positive") return "😃 Uplifting"; if(s==="Negative") return "😞 Critical"; return "😐 Neutral"; }
function trendScore(a){ const f = getCategoryFrequency(); const val = f[a.category] || 1; if(val > allArticles.length*0.15) return "Hot"; if(val > allArticles.length*0.05) return "Warm"; return "Low"; }

/* ---------- Dark mode toggle ---------- */
function toggleDarkTop(){
  document.body.classList.toggle("dark");
  localStorage.setItem("dark", document.body.classList.contains("dark"));
}

/* ---------- Hamburger ---------- */
function toggleHamburger(){
  const sb = document.querySelector(".left-sidebar");
  if (!sb) return;
  sb.style.display = sb.style.display === "none" || getComputedStyle(sb).display === "none" ? "flex" : "none";
}

/* ---------- Misc UI ---------- */
function safeClick(id,fn){ const x = el(id); if (x) x.addEventListener("click", fn); }

/* ---------- Tilt effect ---------- */
function addTilt(card){
  let rect=null;
  card.addEventListener("mousemove", e=>{
    if(!rect) rect = card.getBoundingClientRect();
    const x = e.clientX - rect.left, y = e.clientY - rect.top, cx = rect.width/2, cy = rect.height/2;
    const dx = (x-cx)/cx, dy = (y-cy)/cy;
    card.style.transform = `translateY(-8px) rotateX(${dy*6}deg) rotateY(${dx*-6}deg)`;
  });
  card.addEventListener("mouseleave", ()=> card.style.transform = "");
}

/* ---------- Skeleton control ---------- */
function showSkeleton(show){
  const s = el("pageSkeleton"), a = el("articles");
  if (!s || !a) return;
  if (show) { s.classList.remove("d-none"); a.classList.add("d-none"); } else { s.classList.add("d-none"); a.classList.remove("d-none"); }
}

/* ---------- Fetch / start ---------- */
function initFromServer(){
  // call fetchArticles() and wire stuff
  fetchArticles();
}

// expose debug
window.__news_debug = { fetchArticles, renderArticlesReset };

/* ---------- END ---------- */
document.addEventListener("DOMContentLoaded", () => {
    const toggle = document.getElementById("modeToggle");

    if (localStorage.getItem("theme") === "light") {
        document.body.classList.add("light");
        toggle.textContent = "🌞";
    }

    toggle?.addEventListener("click", () => {
        document.body.classList.toggle("light");

        if (document.body.classList.contains("light")) {
            localStorage.setItem("theme", "light");
            toggle.textContent = "🌞";
        } else {
            localStorage.setItem("theme", "dark");
            toggle.textContent = "🌙";
        }
    });
});
