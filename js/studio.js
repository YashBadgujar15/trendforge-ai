// ============================================================
// TrendForge AI — Studio Controller
// ============================================================

import { DEMO_BRIEF, PIPELINE_STEPS, DEMO_CAMPAIGN } from './services/demo-data.js';

let currentSlide = 0;
let reelFrame = 0;
let reelTimer = null;
let generationDone = false;

// ---- Toast ----
function toast(msg, type = 'default') {
  const container = document.getElementById('toast-container');
  const t = document.createElement('div');
  t.className = `toast ${type}`;
  const icons = { success: '✓', error: '✕', default: '✦' };
  t.innerHTML = `<span class="toast-icon">${icons[type] || '✦'}</span><span>${msg}</span>`;
  container.appendChild(t);
  setTimeout(() => { t.style.animation = 'slideOut 0.3s ease forwards'; setTimeout(() => t.remove(), 300); }, 3000);
}

// ---- Input Mode ----
window.setInputMode = function(mode, btn) {
  document.querySelectorAll('[data-tab]').forEach(b => b.classList.remove('active'));
  btn.classList.add('active');
  const ta = document.getElementById('campaign-brief');
  const placeholders = {
    brief: 'Describe your product, campaign or content idea...\n\nExample: Launching a smart ergonomic chair for remote developers.',
    url: 'Paste a product URL...\n\nExample: https://example.com/product',
    viral: 'Paste a viral post link or text to reverse-engineer...',
  };
  ta.placeholder = placeholders[mode] || '';
};

window.fillDemoBrief = function() {
  document.getElementById('campaign-brief').value = DEMO_BRIEF;
  toast('Demo brief loaded ✦', 'success');
};

window.selectTone = function(btn) {
  document.querySelectorAll('#tone-pills .pill').forEach(p => p.classList.remove('active'));
  btn.classList.add('active');
};

// ---- Generation ----
window.startGeneration = function() {
  const brief = document.getElementById('campaign-brief').value.trim();
  if (!brief) { toast('Please enter a brief first.', 'error'); return; }
  document.getElementById('empty-state').style.display = 'none';
  document.getElementById('pipeline-view').style.display = 'block';
  document.getElementById('results-view').style.display = 'none';
  document.getElementById('generate-btn').disabled = true;
  document.getElementById('generate-btn').innerHTML = '<div class="spinner" style="width:14px;height:14px;border-width:1.5px"></div> Generating...';

  // Activate right panel
  document.getElementById('right-idle').style.display = 'none';
  document.getElementById('right-active').style.display = 'block';
  document.getElementById('ai-status-dot').style.opacity = '1';

  renderPipeline();
  runPipeline();
};

function renderPipeline() {
  const container = document.getElementById('pipeline-steps');
  container.innerHTML = '';
  const div = document.createElement('div');
  div.className = 'pipeline-steps-list';
  PIPELINE_STEPS.forEach((step, i) => {
    const s = document.createElement('div');
    s.className = 'pipeline-step pending';
    s.id = `pstep-${step.id}`;
    s.innerHTML = `
      <div class="step-icon pending" id="picon-${step.id}">○</div>
      <span id="plabel-${step.id}">${step.label}</span>
    `;
    div.appendChild(s);
  });
  container.appendChild(div);

  // Agent list
  const agents = ['🧭 Planner', '✍️ Content Writer', '🎨 Visual Generator', '🔍 Critic', '🔄 Refiner'];
  const agentList = document.getElementById('agent-list');
  agentList.innerHTML = '';
  agents.forEach(a => {
    const row = document.createElement('div');
    row.className = 'agent-row';
    row.id = `agent-${a.slice(2).toLowerCase().replace(/ /g, '-')}`;
    row.innerHTML = `<span class="agent-icon">${a[0]}</span><span class="agent-name">${a.slice(2)}</span><span class="agent-status">⏳</span>`;
    agentList.appendChild(row);
  });
}

async function runPipeline() {
  const agentMap = {
    'brief':    'planner',
    'audience': 'planner',
    'strategy': 'planner',
    'linkedin': 'content-writer',
    'twitter':  'content-writer',
    'carousel': 'visual-generator',
    'reel':     'visual-generator',
    'slop':     'critic',
    'critic':   'critic',
    'refine':   'refiner',
    'ready':    'refiner',
  };
  const agentActivate = {
    'planner': '🧭 Planner',
    'content-writer': '✍️ Content Writer',
    'visual-generator': '🎨 Visual Generator',
    'critic': '🔍 Critic',
    'refiner': '🔄 Refiner',
  };
  let lastAgent = null;

  for (let i = 0; i < PIPELINE_STEPS.length; i++) {
    const step = PIPELINE_STEPS[i];

    // Activate step
    const el = document.getElementById(`pstep-${step.id}`);
    const icon = document.getElementById(`picon-${step.id}`);
    if (el) {
      el.className = 'pipeline-step active';
      icon.className = 'step-icon spin-icon';
      icon.innerHTML = '<div class="spinner" style="width:12px;height:12px;border-width:1.5px"></div>';
      el.scrollIntoView({ block: 'nearest' });
    }
    document.getElementById('pipeline-headline').textContent = step.label + '...';

    // Activate agent
    const agentKey = agentMap[step.id];
    if (agentKey && agentKey !== lastAgent) {
      if (lastAgent) {
        const prevRow = document.getElementById(`agent-${lastAgent}`);
        if (prevRow) { prevRow.classList.remove('active'); prevRow.classList.add('done'); prevRow.querySelector('.agent-status').textContent = '✓'; }
      }
      const row = document.getElementById(`agent-${agentKey}`);
      if (row) { row.classList.add('active'); row.querySelector('.agent-status').textContent = '⚡'; }
      lastAgent = agentKey;
    }

    await delay(step.time);

    // Mark done
    if (el) {
      el.className = 'pipeline-step done';
      icon.className = 'step-icon done';
      icon.innerHTML = '✓';
    }
  }

  // All done
  if (lastAgent) {
    const row = document.getElementById(`agent-${lastAgent}`);
    if (row) { row.classList.remove('active'); row.classList.add('done'); row.querySelector('.agent-status').textContent = '✓'; }
  }

  document.getElementById('pipeline-headline').textContent = 'Campaign ready! ✦';
  document.getElementById('pipeline-badge').textContent = 'Complete';
  document.getElementById('pipeline-badge').className = 'badge badge-success';
  document.getElementById('pipeline-spinner').style.display = 'none';

  setTimeout(showResults, 600);
}

function delay(ms) { return new Promise(res => setTimeout(res, ms)); }

// ---- Show Results ----
function showResults() {
  document.getElementById('pipeline-view').style.display = 'none';
  document.getElementById('results-view').style.display = 'block';
  document.getElementById('generate-btn').disabled = false;
  document.getElementById('generate-btn').innerHTML = `
    <svg width="16" height="16" viewBox="0 0 16 16" fill="none"><path d="M8 1L10 5.5H15L11 8.5L12.5 13L8 10L3.5 13L5 8.5L1 5.5H6L8 1Z" fill="currentColor"/></svg>
    Generate Campaign`;
  generationDone = true;

  // Animate quality score
  animateCounter('quality-score', 0, DEMO_CAMPAIGN.qualityScore, 1000);

  // Show quick scores in right panel
  document.getElementById('quick-scores').style.display = 'block';
  renderQuickScores();

  // Build all tabs
  buildOverviewTab();
  buildLinkedInTab();
  buildTwitterTab();
  buildCarouselTab();
  buildReelTab();
  buildCriticTab();

  switchTab('overview', document.querySelector('#results-tabs .tab-btn'));

  toast('Campaign generated successfully! ✦', 'success');
}

function animateCounter(id, from, to, duration) {
  const el = document.getElementById(id);
  if (!el) return;
  const start = performance.now();
  function tick(now) {
    const progress = Math.min((now - start) / duration, 1);
    el.textContent = Math.round(from + (to - from) * progress);
    if (progress < 1) requestAnimationFrame(tick);
  }
  requestAnimationFrame(tick);
}

// ---- Tab Switching ----
window.switchTab = function(tab, btn) {
  document.querySelectorAll('#results-tabs .tab-btn').forEach(b => b.classList.remove('active'));
  if (btn) btn.classList.add('active');
  document.querySelectorAll('.tab-content').forEach(c => c.style.display = 'none');
  const el = document.getElementById(`tab-${tab}`);
  if (el) el.style.display = 'block';
};

// ---- Overview Tab ----
function buildOverviewTab() {
  const c = DEMO_CAMPAIGN;
  document.getElementById('tab-overview').innerHTML = `
    <div class="overview-grid" style="margin-bottom:20px">
      <div class="ov-card">
        <div class="ov-card-icon">💼</div>
        <div class="ov-card-title">LinkedIn Post</div>
        <div class="ov-card-desc">${c.linkedin.chars} chars · Hook + Body + CTA</div>
        <div class="ov-card-badge"><span class="badge badge-success">✓ Platform Compliant</span></div>
      </div>
      <div class="ov-card">
        <div class="ov-card-icon">𝕏</div>
        <div class="ov-card-title">X Thread</div>
        <div class="ov-card-desc">${c.twitter.length} tweets · Data-driven virality arc</div>
        <div class="ov-card-badge"><span class="badge badge-success">✓ All under 280 chars</span></div>
      </div>
      <div class="ov-card">
        <div class="ov-card-icon">📸</div>
        <div class="ov-card-title">Instagram Carousel</div>
        <div class="ov-card-desc">5 slides · Hook → Problem → Insight → Solution → CTA</div>
        <div class="ov-card-badge"><span class="badge badge-success">✓ Brand colors applied</span></div>
      </div>
      <div class="ov-card">
        <div class="ov-card-icon">🎬</div>
        <div class="ov-card-title">Reel Storyboard</div>
        <div class="ov-card-desc">5 scenes · 30-second arc with voiceover</div>
        <div class="ov-card-badge"><span class="badge badge-success">✓ Kinetic structure</span></div>
      </div>
    </div>
    <div class="card" style="margin-bottom:16px">
      <div style="display:flex;align-items:center;gap:8px;margin-bottom:12px">
        <span>🛡️</span>
        <h3 style="font-size:13px;font-weight:600">Anti-Slop Filter Result</h3>
        <span class="badge badge-success">LOW RISK</span>
        <span style="font-size:10px;color:var(--text-muted);margin-left:auto">⚠ Demo/Simulated</span>
      </div>
      <p style="font-size:12px;color:var(--text-secondary)">3 generic AI phrases detected and replaced. Human-likeness score: <strong>91</strong>.</p>
    </div>
    <div class="card">
      <div style="display:flex;align-items:center;gap:8px;margin-bottom:12px">
        <span>🔍</span>
        <h3 style="font-size:13px;font-weight:600">Auditable AI Trace</h3>
      </div>
      ${buildTraceHTML()}
    </div>
  `;
}

function buildTraceHTML() {
  return DEMO_CAMPAIGN.trace.map((t, i) => `
    <div class="trace-step">
      <div class="trace-step-header" onclick="toggleTrace(this)">
        <div style="display:flex;align-items:center;gap:10px">
          <span class="badge badge-success">✓</span>
          <span class="trace-agent">${t.agent}</span>
        </div>
        <svg width="14" height="14" viewBox="0 0 14 14" fill="none" class="trace-chevron" style="transition:transform 0.2s;color:var(--text-muted)">
          <path d="M3 5L7 9L11 5" stroke="currentColor" stroke-width="1.5" stroke-linecap="round"/>
        </svg>
      </div>
      <div class="trace-body">
        <div class="trace-field"><div class="trace-field-label">Input</div><div class="trace-field-val">${t.input}</div></div>
        <div class="trace-field"><div class="trace-field-label">Decision</div><div class="trace-field-val">${t.decision}</div></div>
        <div class="trace-field"><div class="trace-field-label">Output</div><div class="trace-field-val">${t.output}</div></div>
      </div>
    </div>
    ${i < DEMO_CAMPAIGN.trace.length - 1 ? '<div class="trace-connector"><div class="trace-connector-line"></div></div>' : ''}
  `).join('');
}

window.toggleTrace = function(header) {
  const body = header.nextElementSibling;
  const chevron = header.querySelector('.trace-chevron');
  body.classList.toggle('open');
  if (chevron) chevron.style.transform = body.classList.contains('open') ? 'rotate(180deg)' : '';
};

// ---- LinkedIn Tab ----
function buildLinkedInTab() {
  const li = DEMO_CAMPAIGN.linkedin;
  document.getElementById('tab-linkedin').innerHTML = `
    <div style="display:grid;grid-template-columns:1fr auto;gap:16px;align-items:start;flex-wrap:wrap">
      <div class="linkedin-preview">
        <div class="li-profile">
          <div class="li-avatar">👤</div>
          <div class="li-meta">
            <strong>Alex Chen · Founder, DevChair Pro</strong>
            <span>Remote Work Entrepreneur · 14,200 followers</span>
          </div>
        </div>
        <div class="li-hook">${li.hook}</div>
        <div class="li-body" id="li-body-text">${li.body}</div>
        <div class="li-cta">${li.cta}</div>
        <div class="li-stats">
          <span>${li.chars} characters</span>
          <span>·</span>
          <span>~3 min read</span>
        </div>
        <div class="li-compliance">✓ Platform compliance verified</div>
      </div>
      <div style="display:flex;flex-direction:column;gap:8px;min-width:140px">
        <button class="btn btn-ghost btn-sm" onclick="copyLinkedIn()">📋 Copy</button>
        <button class="btn btn-ghost btn-sm" onclick="toast('Regenerating...','default');setTimeout(()=>toast('LinkedIn post regenerated ✦','success'),1800)">🔄 Regenerate</button>
        <button class="btn btn-secondary btn-sm" onclick="approvePlatform('linkedin',this)">✓ Approve</button>
        <div class="divider"></div>
        <div style="font-size:11px;color:var(--text-muted)">
          <div style="margin-bottom:4px">Tone: Founder</div>
          <div style="margin-bottom:4px">Hook: Personal story</div>
          <div>CTA: Comment gating</div>
        </div>
      </div>
    </div>
  `;
}

window.copyLinkedIn = function() {
  const body = document.getElementById('li-body-text');
  if (body) { navigator.clipboard?.writeText(DEMO_CAMPAIGN.linkedin.hook + '\n\n' + DEMO_CAMPAIGN.linkedin.body).catch(() => {}); }
  toast('LinkedIn post copied! 📋', 'success');
};

// ---- Twitter Tab ----
function buildTwitterTab() {
  const tweets = DEMO_CAMPAIGN.twitter;
  document.getElementById('tab-twitter').innerHTML = `
    <div class="thread-list">
      ${tweets.map(tw => `
        <div class="tweet-card">
          <div class="tweet-num">TWEET ${tw.num} / ${tweets.length}</div>
          <div class="tweet-text">${tw.text}</div>
          <div class="tweet-footer">
            <span class="tweet-chars" style="color:${tw.chars > 260 ? 'var(--warning)' : 'var(--text-muted)'}">${tw.chars}/280</span>
            <div style="display:flex;gap:6px">
              <button class="btn btn-ghost btn-sm" onclick="copyTweet(${tw.num-1})">📋</button>
              <button class="btn btn-ghost btn-sm" onclick="toast('Regenerating tweet ${tw.num}...','default');setTimeout(()=>toast('Tweet ${tw.num} regenerated ✦','success'),1500)">🔄</button>
            </div>
          </div>
        </div>
      `).join('')}
      <button class="btn btn-secondary" style="width:100%;margin-top:4px" onclick="copyAllTweets()">📋 Copy Full Thread</button>
    </div>
  `;
}

window.copyTweet = function(idx) {
  navigator.clipboard?.writeText(DEMO_CAMPAIGN.twitter[idx].text).catch(() => {});
  toast(`Tweet ${idx+1} copied! 📋`, 'success');
};
window.copyAllTweets = function() {
  const text = DEMO_CAMPAIGN.twitter.map((t,i) => `${i+1}/${DEMO_CAMPAIGN.twitter.length}\n${t.text}`).join('\n\n');
  navigator.clipboard?.writeText(text).catch(() => {});
  toast('Full thread copied! 📋', 'success');
};

// ---- Carousel Tab ----
function buildCarouselTab() {
  currentSlide = 0;
  const slides = DEMO_CAMPAIGN.carousel;
  const slideColors = ['#6366f1','#8b5cf6','#6366f1','#10b981','#6366f1'];

  const slidesHTML = slides.map((s, i) => `
    <div class="carousel-slide ${i === 0 ? 'active' : ''}" id="cslide-${i}"
      style="background:${s.bg}; color:#fff;">
      <div class="slide-bg-circle" style="width:400px;height:400px;background:${s.accent};top:-100px;right:-100px;"></div>
      <div class="slide-num-badge">${String(s.slide).padStart(2,'0')}</div>
      <div class="slide-inner">
        <div class="slide-tag" style="color:${s.accent}">${s.type.toUpperCase()}</div>
        <div class="slide-headline">${s.headline}</div>
        <div class="slide-subtext">${s.subtext}</div>
        ${s.stats ? `<div class="slide-stats">${s.stats.map(st=>`<div class="slide-stat-item"><div class="slide-stat-val" style="color:${s.accent}">${st.val}</div><div class="slide-stat-lbl">${st.label}</div></div>`).join('')}</div>` : ''}
        ${s.points ? `<div class="slide-points">${s.points.map(p=>`<div class="slide-point"><span style="color:${s.accent}">→</span>${p}</div>`).join('')}</div>` : ''}
        ${s.features ? `<div class="slide-features">${s.features.map(f=>`<div class="slide-feature"><span style="color:${s.accent}">✓</span>${f}</div>`).join('')}</div>` : ''}
        ${s.cta ? `<div class="slide-cta-pill">${s.cta}</div>` : ''}
      </div>
    </div>
  `).join('');

  const dotsHTML = slides.map((_, i) => `<div class="cdot ${i===0?'active':''}" onclick="goSlide(${i})" id="cdot-${i}"></div>`).join('');

  document.getElementById('tab-carousel').innerHTML = `
    <div class="carousel-wrap">
      <div style="display:grid;grid-template-columns:1fr 200px;gap:20px;align-items:start">
        <div>
          <div class="carousel-stage">
            ${slidesHTML}
          </div>
          <div class="carousel-controls">
            <button class="carousel-btn" onclick="prevSlide()">‹</button>
            <div style="display:flex;flex-direction:column;align-items:center;gap:8px">
              <span class="slide-counter" id="slide-counter">01 / 05</span>
              <div class="carousel-dots" id="carousel-dots">${dotsHTML}</div>
            </div>
            <button class="carousel-btn" onclick="nextSlide()">›</button>
          </div>
          <div class="carousel-side-controls">
            <button class="btn btn-ghost btn-sm" onclick="toast('Style changed','default')">🎨 Change Style</button>
            <button class="btn btn-ghost btn-sm" onclick="regenerateSlide()">🔄 Regen Slide</button>
            <button class="btn btn-ghost btn-sm" onclick="downloadCarousel()">⬇ Download PNG</button>
          </div>
        </div>
        <div style="padding-top:8px">
          <div style="font-size:11px;font-weight:700;letter-spacing:0.08em;color:var(--text-muted);margin-bottom:10px">SLIDE NAVIGATOR</div>
          ${slides.map((s,i) => `
            <div onclick="goSlide(${i})" style="cursor:pointer;padding:8px 10px;border-radius:6px;border:1px solid ${i===0?'var(--border-accent)':'var(--border)'};margin-bottom:6px;transition:all 0.2s;font-size:11px;background:${i===0?'var(--accent-glow)':'transparent'}" id="snav-${i}">
              <span style="color:var(--accent);font-weight:700">0${s.slide}</span> ${s.type.toUpperCase()}<br>
              <span style="color:var(--text-muted);font-size:10px">${s.headline.substring(0,30)}...</span>
            </div>
          `).join('')}
        </div>
      </div>
    </div>
  `;
}

window.goSlide = function(n) {
  const slides = DEMO_CAMPAIGN.carousel;
  document.querySelectorAll('.carousel-slide').forEach((s, i) => {
    s.classList.toggle('active', i === n);
  });
  document.querySelectorAll('.cdot').forEach((d, i) => d.classList.toggle('active', i === n));
  document.querySelectorAll('[id^="snav-"]').forEach((d, i) => {
    d.style.border = i === n ? '1px solid var(--border-accent)' : '1px solid var(--border)';
    d.style.background = i === n ? 'var(--accent-glow)' : 'transparent';
  });
  const counter = document.getElementById('slide-counter');
  if (counter) counter.textContent = `0${n+1} / 05`;
  currentSlide = n;
};
window.nextSlide = function() { goSlide((currentSlide + 1) % 5); };
window.prevSlide = function() { goSlide((currentSlide + 4) % 5); };
window.regenerateSlide = function() {
  toast(`Regenerating slide ${currentSlide+1}...`, 'default');
  setTimeout(() => toast(`Slide ${currentSlide+1} regenerated ✦`, 'success'), 1600);
};
window.downloadCarousel = function() {
  toast('PNG download requires canvas rendering — available in live mode', 'default');
};

// ---- Reel Tab ----
function buildReelTab() {
  const reel = DEMO_CAMPAIGN.reel;
  const sceneColors = {
    HOOK: '#6366f1', PROBLEM: '#ef4444', INSIGHT: '#f59e0b', PRODUCT: '#10b981', CTA: '#8b5cf6'
  };

  const scenesHTML = reel.scenes.map((sc, i) => `
    <div class="scene-card">
      <div class="scene-time-wrap">
        <span class="scene-time">${sc.time}</span>
        <span class="scene-type" style="color:${sceneColors[sc.type]}">${sc.type}</span>
        <span class="scene-duration-badge">${sc.duration}</span>
      </div>
      <div class="scene-preview" style="background:linear-gradient(135deg,${sceneColors[sc.type]}22,${sceneColors[sc.type]}08);border:1px solid ${sceneColors[sc.type]}30">
        <div style="text-align:center;padding:8px">
          <div style="font-size:13px;font-weight:700;color:${sceneColors[sc.type]};margin-bottom:4px">${sc.text}</div>
          <div style="font-size:10px;color:var(--text-muted)">${sc.visual}</div>
        </div>
      </div>
      <div class="scene-info">
        <strong>${sc.type} Scene</strong>
        <p>Voiceover: "${sc.voiceover}"</p>
        <span class="scene-tag">On-screen: ${sc.text}</span>
      </div>
    </div>
  `).join('');

  document.getElementById('tab-reel').innerHTML = `
    <div class="reel-wrap">
      <div style="display:grid;grid-template-columns:1fr 240px;gap:20px;align-items:start">
        <div>
          <div style="display:flex;align-items:center;justify-content:space-between;margin-bottom:14px">
            <h3 style="font-size:14px;font-weight:600">Reel Storyboard · ${reel.duration}</h3>
            <button class="btn btn-secondary btn-sm" onclick="previewReel()">▶ Preview Reel</button>
          </div>
          <div class="reel-timeline">${scenesHTML}</div>
        </div>
        <div>
          <div style="font-size:11px;font-weight:700;letter-spacing:0.08em;color:var(--text-muted);margin-bottom:10px;text-align:center">KINETIC PREVIEW</div>
          <div class="reel-preview-area" id="reel-preview-area">
            <div class="reel-kinetic" id="reel-kinetic-content">
              <div style="font-size:11px;color:rgba(255,255,255,0.4);margin-bottom:16px">Click "Preview Reel"</div>
              <div style="font-size:13px;color:rgba(255,255,255,0.3)">30-second reel</div>
            </div>
          </div>
        </div>
      </div>
    </div>
  `;
}

window.previewReel = function() {
  const scenes = DEMO_CAMPAIGN.reel.scenes;
  const colors = { HOOK:'#6366f1', PROBLEM:'#ef4444', INSIGHT:'#f59e0b', PRODUCT:'#10b981', CTA:'#8b5cf6' };
  const area = document.getElementById('reel-preview-area');
  area.style.background = '#000';
  let idx = 0;

  function showScene(i) {
    if (i >= scenes.length) {
      area.querySelector('#reel-kinetic-content').innerHTML = `
        <div style="font-size:14px;color:rgba(255,255,255,0.7)">▶ Preview Complete</div>
        <button class="btn btn-ghost btn-sm" style="margin-top:10px" onclick="previewReel()">Replay</button>
      `;
      return;
    }
    const sc = scenes[i];
    const kc = area.querySelector('#reel-kinetic-content') || area;
    if (kc.id !== 'reel-kinetic-content') {
      area.innerHTML = '<div class="reel-kinetic" id="reel-kinetic-content"></div>';
    }
    const content = document.getElementById('reel-kinetic-content');
    content.innerHTML = `
      <div style="font-size:10px;font-weight:700;letter-spacing:0.1em;color:${colors[sc.type]};margin-bottom:12px">${sc.type} · ${sc.time}</div>
      <div class="rk-text" style="color:white;font-size:18px;animation:scaleIn 0.4s ease">${sc.text}</div>
      <div class="rk-sub" style="margin-top:10px;font-size:11px">${sc.voiceover.substring(0,50)}...</div>
    `;
    area.style.background = `linear-gradient(135deg, ${colors[sc.type]}22, #000)`;
    const parseDuration = s => parseInt(s) * 1000;
    setTimeout(() => showScene(i + 1), parseDuration(sc.duration));
  }
  showScene(0);
  toast('Playing 30s reel preview...', 'default');
};

// ---- Critic Tab ----
function buildCriticTab() {
  const c = DEMO_CAMPAIGN.critic;
  const scores = c.scores;
  const scoreKeys = [
    { key: 'humanLikeness',    label: 'Human-likeness',    color: '#10b981' },
    { key: 'hookStrength',     label: 'Hook strength',     color: '#6366f1' },
    { key: 'platformFit',      label: 'Platform fit',      color: '#3b82f6' },
    { key: 'brandConsistency', label: 'Brand consistency', color: '#8b5cf6' },
    { key: 'clarity',          label: 'Clarity',           color: '#6366f1' },
    { key: 'ctaStrength',      label: 'CTA strength',      color: '#f59e0b' },
  ];

  document.getElementById('tab-critic').innerHTML = `
    <div style="display:grid;grid-template-columns:1fr 1fr;gap:20px;align-items:start">
      <div>
        <div style="display:flex;align-items:center;justify-content:space-between;margin-bottom:16px">
          <h3 style="font-size:14px;font-weight:600">AI Creative Critic</h3>
          <div style="display:flex;gap:6px;align-items:center">
            <span class="badge badge-warning" style="font-size:10px">⚠ DEMO/SIMULATED</span>
          </div>
        </div>
        <div class="critic-scores" id="critic-scores">
          ${scoreKeys.map(sk => `
            <div class="cscore-row">
              <div class="cscore-header">
                <span class="cscore-label">${sk.label}</span>
                <span class="cscore-val" style="color:${sk.color}" id="cscore-${sk.key}">0</span>
              </div>
              <div class="score-bar">
                <div class="score-fill" id="sfill-${sk.key}"
                  style="width:0%;background:${sk.color};transition:width 0.8s cubic-bezier(0.4,0,0.2,1)"></div>
              </div>
            </div>
          `).join('')}
        </div>
        <div style="margin-top:16px;padding:14px;background:var(--bg-secondary);border-radius:var(--radius-md);border:1px solid var(--border)">
          <div style="font-size:11px;font-weight:700;letter-spacing:0.08em;color:var(--text-muted);margin-bottom:8px">AI SLOP RISK</div>
          <span class="badge badge-success" style="font-size:14px;padding:6px 14px">🛡️ ${scores.aiSlopRisk}</span>
        </div>
      </div>
      <div>
        <h4 style="font-size:12px;font-weight:700;letter-spacing:0.06em;color:var(--text-muted);margin-bottom:10px">DETECTED PHRASES</h4>
        <div class="slop-phrases">
          ${c.detectedPhrases.map(p => `<span class="slop-phrase">"${p}"</span>`).join('')}
        </div>
        <p style="font-size:12px;color:var(--text-secondary);margin-bottom:16px">${c.detectedPhrases.length} generic AI phrases detected and flagged.</p>
        <button class="btn btn-primary" style="width:100%;margin-bottom:16px" onclick="autoRefine()">
          ⚡ Auto-Refine
        </button>
        <div class="divider"></div>
        <h4 style="font-size:12px;font-weight:700;letter-spacing:0.06em;color:var(--text-muted);margin-bottom:10px">ISSUES FOUND & RESOLVED</h4>
        <div class="critic-issues">
          ${c.issues.map(iss => `
            <div class="issue-card ${iss.status === 'resolved' ? 'resolved' : ''}">
              <div class="issue-header">
                <span class="issue-platform">${iss.platform}</span>
                <span class="badge ${iss.severity === 'medium' ? 'badge-warning' : 'badge-muted'}">${iss.severity}</span>
              </div>
              <div class="issue-desc">🔍 ${iss.description}</div>
              <div class="issue-action">✓ ${iss.action}</div>
              ${iss.status === 'resolved' ? '<div style="margin-top:4px"><span class="badge badge-success">✓ Resolved</span></div>' : ''}
            </div>
          `).join('')}
        </div>
        <div style="margin-top:16px;padding:12px 14px;background:var(--accent-glow);border:1px solid var(--border-accent);border-radius:var(--radius-md);font-size:12px">
          <strong style="display:block;margin-bottom:4px">Critic Verdict:</strong>
          ${c.overallVerdict}
        </div>
      </div>
    </div>
  `;

  // Animate scores
  setTimeout(() => {
    scoreKeys.forEach(sk => {
      const val = scores[sk.key];
      animateCounter(`cscore-${sk.key}`, 0, val, 1200);
      setTimeout(() => {
        const fill = document.getElementById(`sfill-${sk.key}`);
        if (fill) fill.style.width = val + '%';
      }, 100);
    });
  }, 100);
}

window.autoRefine = function() {
  toast('Auto-refining outputs...', 'default');
  setTimeout(() => {
    document.querySelectorAll('.slop-phrase').forEach(el => {
      el.style.opacity = '0.3';
      el.style.transition = 'opacity 0.5s';
    });
    toast('3 phrases replaced. Quality score improved to 94 ✦', 'success');
    const el = document.getElementById('quality-score');
    if (el) animateCounter('quality-score', 91, 94, 800);
  }, 1800);
};

// ---- Quick Scores (right panel) ----
function renderQuickScores() {
  const c = DEMO_CAMPAIGN.critic.scores;
  const items = [
    { label: 'Human-likeness', val: c.humanLikeness, color: '#10b981' },
    { label: 'Hook strength',  val: c.hookStrength,  color: '#6366f1' },
    { label: 'Platform fit',   val: c.platformFit,   color: '#3b82f6' },
    { label: 'AI Slop Risk',   val: c.aiSlopRisk,    color: '#10b981', isTag: true },
  ];
  const list = document.getElementById('qscore-list');
  if (!list) return;
  list.innerHTML = items.map(item => `
    <div class="qs-row">
      <div class="qs-header">
        <span class="qs-label">${item.label}</span>
        <span class="qs-val" style="color:${item.color}">${item.val}</span>
      </div>
      ${!item.isTag ? `<div class="score-bar"><div class="score-fill" style="width:${item.val}%;background:${item.color}"></div></div>` : ''}
    </div>
  `).join('');
}

// ---- Approval ----
window.showApproval = function() {
  if (!generationDone) { toast('Generate a campaign first.', 'error'); return; }
  const platforms = [
    { icon: '💼', name: 'LinkedIn Post' },
    { icon: '𝕏',  name: 'X Thread'     },
    { icon: '📸', name: 'Carousel'      },
    { icon: '🎬', name: 'Reel'          },
  ];
  document.getElementById('approval-list').innerHTML = platforms.map((p, i) => `
    <div class="approval-item" id="ap-${i}">
      <span class="approval-icon">${p.icon}</span>
      <span class="approval-name">${p.name}</span>
      <div class="approval-check" id="apcheck-${i}" onclick="toggleApprove(${i})">○</div>
    </div>
  `).join('');
  document.getElementById('approval-modal').style.display = 'flex';
};

window.toggleApprove = function(i) {
  const item = document.getElementById(`ap-${i}`);
  const check = document.getElementById(`apcheck-${i}`);
  item.classList.toggle('approved');
  check.classList.toggle('checked');
  check.textContent = check.classList.contains('checked') ? '✓' : '○';
};

window.approveCampaign = function() {
  document.querySelectorAll('[id^="apcheck-"]').forEach((el, i) => {
    el.classList.add('checked');
    el.textContent = '✓';
    document.getElementById(`ap-${i}`)?.classList.add('approved');
  });
  setTimeout(() => {
    closeModal('approval-modal');
    toast('Campaign approved! Ready for export. ✦', 'success');
  }, 400);
};

window.approvePlatform = function(platform, btn) {
  btn.className = 'btn btn-success btn-sm';
  btn.textContent = '✓ Approved';
  btn.disabled = true;
  toast(`${platform} approved ✦`, 'success');
};

// ---- Export ----
window.openExportModal = function() {
  if (!generationDone) { toast('Generate a campaign first.', 'error'); return; }
  document.getElementById('export-modal').style.display = 'flex';
};

window.exportItem = function(type) {
  const messages = {
    linkedin: 'LinkedIn post copied to clipboard! 📋',
    twitter:  'X thread copied to clipboard! 📋',
    carousel: 'Carousel PNG download requires live mode',
    package:  'Full campaign package export ready! 📦',
  };
  closeModal('export-modal');
  if (type === 'linkedin') navigator.clipboard?.writeText(DEMO_CAMPAIGN.linkedin.hook + '\n\n' + DEMO_CAMPAIGN.linkedin.body).catch(() => {});
  if (type === 'twitter') {
    const text = DEMO_CAMPAIGN.twitter.map((t,i) => `${i+1}/${DEMO_CAMPAIGN.twitter.length}\n${t.text}`).join('\n\n');
    navigator.clipboard?.writeText(text).catch(() => {});
  }
  toast(messages[type] || 'Exported!', 'success');
};

window.closeModal = function(id) {
  document.getElementById(id).style.display = 'none';
};
