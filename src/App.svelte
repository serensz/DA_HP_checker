<script>
  import { onMount } from "svelte";
  import Chart from "chart.js/auto";
  import Navigation from "./Navigation.svelte";
  import BossTable from "./BossTable.svelte";

  let bosses = [];
  let selectedName = "";
  let chart;
  let canvasEl;
  let currentPage = "chart";

  onMount(async () => {
    const base = import.meta.env.BASE_URL || '/';
    const res = await fetch(`${base}bosses.json`);
    bosses = await res.json();

    bosses.sort((a, b) => a.boss_name.localeCompare(b.boss_name));
    selectedName = bosses[0]?.boss_name ?? "";

    const hash = window.location.hash.slice(1) || "chart";
    currentPage = hash;

    window.addEventListener("hashchange", () => {
      currentPage = window.location.hash.slice(1) || "chart";
      if (currentPage === "chart") {
        chart = null;
        setTimeout(() => {
          if (canvasEl) initChart();
        }, 100);
      }
    });
  });

  $: if (canvasEl && bosses.length > 0 && !chart && currentPage === "chart") {
    setTimeout(() => initChart(), 50);
  }

  $: if (chart && selectedName) {
    const boss = bosses.find((b) => b.boss_name === selectedName);
    if (boss) {
      const labels = boss.timeline.map((t) => t.date);
      const values = boss.timeline.map((t) => t.hp);

      chart.data.labels = labels;
      chart.data.datasets[0].data = values;
      chart.data.datasets[0].label = boss.boss_name;
      chart.update();
    }
  }

  function initChart() {
    if (!canvasEl || bosses.length === 0) return;

    if (chart) {
      chart.destroy();
    }

    const firstBoss = bosses[0];
    const labels = firstBoss.timeline.map((t) => t.date);
    const values = firstBoss.timeline.map((t) => t.hp);

    chart = new Chart(canvasEl, {
      type: "line",
      data: {
        labels,
        datasets: [
          {
            label: firstBoss.boss_name,
            data: values,
            borderColor: "#ff7b22",
            backgroundColor: "rgba(255,123,34,0.25)",
            fill: true,
            borderWidth: 3,
            tension: 0.28,
            pointRadius: 5,
            pointHoverRadius: 9,
            pointBackgroundColor: "#facc15",
            pointBorderColor: "#ff7b22"
          }
        ]
      },
      options: {
        responsive: true,
        plugins: {
          legend: { labels: { color: "#f9fafb" } },
          tooltip: {
            callbacks: {
              label: (ctx) => {
                const v = ctx.parsed.y || 0;
                return " HP: " + v.toLocaleString();
              }
            }
          }
        },
        scales: {
          x: {
            ticks: { color: "#9ca3af" },
            grid: { color: "rgba(148, 163, 184, 0.18)" }
          },
          y: {
            ticks: {
              color: "#9ca3af",
              callback: (value) => value.toLocaleString()
            },
            grid: { color: "rgba(148, 163, 184, 0.18)" }
          }
        }
      }
    });
  }

  $: stats = (() => {
    const boss = bosses.find((b) => b.boss_name === selectedName);
    if (!boss) return null;

    const hp = boss.timeline.map((t) => t.hp);
    const first = hp[0];
    const last = hp[hp.length - 1];
    const max = Math.max(...hp);
    const min = Math.min(...hp);
    const diff = last - first;
    const pct = first ? ((diff / first) * 100).toFixed(1) : "0.0";

    // คำนวณจำนวนวันที่ผ่านไปจากครั้งสุดท้าย
    const lastDate = new Date(boss.timeline[boss.timeline.length - 1].date);
    const today = new Date();
    // @ts-ignore
    const daysPassed = Math.floor((today - lastDate) / (1000 * 60 * 60 * 24));

    return { 
      boss, 
      first, 
      last, 
      max, 
      min, 
      diff, 
      pct, 
      runs: boss.timeline.length,
      lastDate: lastDate.toLocaleDateString('th-TH'),
      daysPassed
    };
  })();

  function getBossImage(boss) {
    const base = import.meta.env.BASE_URL || '/';
    return boss?.image ? `${base}${boss.image}` : null;
  }

  function handleImageError(e) {
    e.target.style.display = 'none';
  }
</script>

<svelte:head>
  <title>New Eridu Boss HP Terminal</title>
</svelte:head>

<div class="page">
  <div class="container">

    <!-- Top bar -->
    <div class="ne-topbar">
      <div>
        <div class="ne-logo-text">
          <span>NEW</span> ERIDU // ZZZ
        </div>
        <div class="ne-subtitle">
          Hollow Data Console · Boss HP Analytics
        </div>
      </div>
      <div class="topbar-right">
        <span class="accent-dot"></span>
        <span class="ne-status-pill">
          <span class="fw-semibold status-online">ONLINE</span>
          <span class="status-divider">//</span>
          <span class="muted"> Updated : 2025/12/02 </span>
        </span>
        <div class="social-links">
          <a href="https://github.com/serensz" target="_blank" rel="noopener noreferrer" class="social-link" title="GitHub: serensz">
            <svg width="16" height="16" viewBox="0 0 24 24" fill="currentColor">
              <path d="M12 0c-6.626 0-12 5.373-12 12 0 5.302 3.438 9.8 8.207 11.387.599.111.793-.261.793-.577v-2.234c-3.338.726-4.033-1.416-4.033-1.416-.546-1.387-1.333-1.756-1.333-1.756-1.089-.745.083-.729.083-.729 1.205.084 1.839 1.237 1.839 1.237 1.07 1.834 2.807 1.304 3.492.997.107-.775.418-1.305.762-1.604-2.665-.305-5.467-1.334-5.467-5.931 0-1.311.469-2.381 1.236-3.221-.124-.303-.535-1.524.117-3.176 0 0 1.008-.322 3.301 1.23.957-.266 1.983-.399 3.003-.404 1.02.005 2.047.138 3.006.404 2.291-1.552 3.297-1.23 3.297-1.23.653 1.653.242 2.874.118 3.176.77.84 1.235 1.911 1.235 3.221 0 4.609-2.807 5.624-5.479 5.921.43.372.823 1.102.823 2.222v3.293c0 .319.192.694.801.576 4.765-1.589 8.199-6.086 8.199-11.386 0-6.627-5.373-12-12-12z"/>
            </svg>
          </a>
          <a href="https://discord.com/users/himesakihikari" target="_blank" rel="noopener noreferrer" class="social-link" title="Discord: himesakihikari">
            <svg width="16" height="16" viewBox="0 0 24 24" fill="currentColor">
              <path d="M20.317 4.37a19.791 19.791 0 0 0-4.885-1.515a.074.074 0 0 0-.079.037c-.21.375-.444.864-.608 1.25a18.27 18.27 0 0 0-5.487 0a12.64 12.64 0 0 0-.617-1.25a.077.077 0 0 0-.079-.037A19.736 19.736 0 0 0 3.677 4.37a.07.07 0 0 0-.032.027C.533 9.046-.32 13.58.099 18.057a.082.082 0 0 0 .031.057a19.9 19.9 0 0 0 5.993 3.03a.078.078 0 0 0 .084-.028a14.09 14.09 0 0 0 1.226-1.994a.076.076 0 0 0-.041-.106a13.107 13.107 0 0 1-1.872-.892a.077.077 0 0 1-.008-.128a10.2 10.2 0 0 0 .372-.292a.074.074 0 0 1 .077-.01c3.928 1.793 8.18 1.793 12.062 0a.074.074 0 0 1 .078.01c.12.098.246.198.373.292a.077.077 0 0 1-.006.127a12.299 12.299 0 0 1-1.873.892a.077.077 0 0 0-.041.107c.36.698.772 1.362 1.225 1.993a.076.076 0 0 0 .084.028a19.839 19.839 0 0 0 6.002-3.03a.077.077 0 0 0 .032-.054c.5-5.177-.838-9.674-3.549-13.66a.061.061 0 0 0-.031-.03zM8.02 15.33c-1.183 0-2.157-1.085-2.157-2.419c0-1.333.956-2.419 2.157-2.419c1.21 0 2.176 1.096 2.157 2.42c0 1.333-.956 2.418-2.157 2.418zm7.975 0c-1.183 0-2.157-1.085-2.157-2.419c0-1.333.955-2.419 2.157-2.419c1.21 0 2.176 1.096 2.157 2.42c0 1.333-.946 2.418-2.157 2.418z"/>
            </svg>
          </a>
        </div>
      </div>
    </div>

    <div class="title-block">
      <h1 class="main-title">ZZZ Deadly Assault HP Checker</h1>
      <p class="muted">
        เว็บไซต์สำหรับเช็คเทรนด์เลือดของบอสต่างๆในโหมด Deadly Assault ของเกม Zenless Zone Zero เพื่อแสดงให้เห็นว่าทำไมบอสถึงถึกหนังหมาได้ขนาดนั้น
      </p>
    </div>

    <!-- Burnice Video Section -->
    <div class="burnice-section">
      <img src="{import.meta.env.BASE_URL || '/'}burnice_dance.gif" alt="Burnice Dance" class="burnice-video">
    </div>

    <Navigation {currentPage} />

    {#if currentPage === "chart"}
      <!-- Selector + stats -->
      <div class="content-with-image">
        <div class="main-content">
          <div class="card-ne mb-4">
            <div class="selector-row">
              <div class="selector-col">
                <label for="bossSelect" class="selector-label muted">เลือกบอส</label>
                <select
                  id="bossSelect"
                  bind:value={selectedName}
                >
                  {#each bosses as b}
                    <option value={b.boss_name}>{b.boss_name}</option>
                  {/each}
                </select>
              </div>

              <div class="stats-col">
                {#if stats}
                  <div class="stats-bar">
                    <div class="stat-pill stat-first">
                      <span class="stat-label">ครั้งแรก</span>
                      <span class="stat-value">{stats.first.toLocaleString()}</span>
                    </div>
                    <div class="stat-pill stat-last">
                      <span class="stat-label">ล่าสุด</span>
                      <span class="stat-value">{stats.last.toLocaleString()}</span>
                    </div>
                    <div class="stat-pill stat-runs">
                      <span class="stat-label">จำนวนรอบ</span>
                      <span class="stat-value">{stats.runs}</span>
                    </div>
                    <div class="stat-pill stat-max">
                      <span class="stat-label">สูงสุด</span>
                      <span class="stat-value">{stats.max.toLocaleString()}</span>
                    </div>
                    <div class="stat-pill stat-min">
                      <span class="stat-label">ต่ำสุด</span>
                      <span class="stat-value">{stats.min.toLocaleString()}</span>
                    </div>
                    <div class="stat-pill stat-delta">
                      <span class="stat-label">Δ จากครั้งแรก</span>
                      <span class="stat-value" class:positive={stats.diff >= 0} class:negative={stats.diff < 0}>
                        {stats.diff >= 0 ? "+" : ""}{stats.diff.toLocaleString()}
                        {" "}
                        ({stats.diff >= 0 ? "+" : ""}{stats.pct}%)
                      </span>
                    </div>
                    <div class="stat-pill stat-pill-full stat-days">
                      <span class="stat-label">มาครั้งสุดท้าย</span>
                      <span class="stat-value">{stats.daysPassed} วันที่แล้ว</span>
                      <span class="stat-date">({stats.lastDate})</span>
                    </div>
                  </div>
                {/if}
              </div>
            </div>
          </div>

          <!-- Chart card -->
          {#key currentPage}
            <div class="card-ne">
              <div class="chart-header">
                <div class="chart-header-left">
                  {#if stats && getBossImage(stats.boss)}
                    <img 
                      src={getBossImage(stats.boss)} 
                      alt={stats.boss.boss_name}
                      class="boss-header-image"
                      on:error={handleImageError}
                      loading="lazy"
                    />
                  {/if}
                  <div>
                    <div class="badge-phase">
                      {#if stats}
                        HP Timeline · {stats.runs} runs
                      {:else}
                        HP Timeline
                      {/if}
                    </div>
                    <h5 class="chart-title">
                      {stats ? stats.boss.boss_name : "Boss HP Timeline"}
                    </h5>
                  </div>
                </div>
                <div class="chart-note muted">
                  หนึ่งจุด = HP ของบอสในกิจกรรมแต่ละรอบ
                </div>
              </div>

              <div class="chart-shell">
                <canvas bind:this={canvasEl}></canvas>
              </div>
            </div>
          {/key}
        </div>

        <!-- Boss Image Sidebar -->
        {#if stats && getBossImage(stats.boss)}
          <div class="boss-sidebar">
            <div class="boss-image-wrapper">
              <img 
                src={getBossImage(stats.boss)} 
                alt={stats.boss.boss_name}
                class="boss-large-image"
                on:error={handleImageError}
                loading="lazy"
              />
              <div class="boss-name-overlay">
                {stats.boss.boss_name}
              </div>
            </div>
          </div>
        {/if}
      </div>
    {:else if currentPage === "table"}
      <BossTable {bosses} />
    {/if}

    <footer class="footer">
      <p>Developed by Hikari <span class="heart">♥</span></p>
      <p class="footer-credit">Burnice GIF credit: <a href="https://x.com/KW7MD8FEWT7lMXx" target="_blank" rel="noopener noreferrer">SuperAppleMan🍎</a> (x)</p>
    </footer>

  </div>
</div>

<style>
  :global(body) {
    margin: 0;
    min-height: 100vh;
    font-family: system-ui, -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif;
    font-size: 16px;
    background:
      radial-gradient(circle at 0% 0%, rgba(255, 123, 34, 0.15) 0, transparent 55%),
      radial-gradient(circle at 100% 0%, rgba(250, 204, 21, 0.2) 0, transparent 55%),
      radial-gradient(circle at 50% 100%, rgba(15, 23, 42, 0.8) 0, transparent 55%),
      #050608;
    color: #f9fafb;
  }

  .page {
    padding: 24px 12px;
    display: flex;
    justify-content: center;
  }

  .container {
    width: 100%;
    max-width: 1100px;
  }

  /* Top Bar */
  .ne-topbar {
    background: #000;
    border-radius: 14px;
    padding: 10px 18px;
    display: flex;
    justify-content: space-between;
    align-items: center;
    border: 1px solid rgba(255,255,255,0.08);
    box-shadow: 0 18px 40px rgba(0,0,0,0.65);
    margin-bottom: 24px;
  }

  .ne-logo-text {
    font-size: 1.15rem;
    letter-spacing: 0.25em;
    text-transform: uppercase;
    font-weight: 700;
  }

  .ne-logo-text span {
    color: #ff7b22;
  }

  .ne-subtitle {
    font-size: 0.9rem;
    color: #9ca3af;
  }

  .topbar-right {
    display: flex;
    gap: 8px;
    align-items: center;
  }

  .accent-dot {
    width: 7px;
    height: 7px;
    border-radius: 50%;
    background: #ff7b22;
    box-shadow: 0 0 8px #ff9100;
  }

  .ne-status-pill {
    font-size: 0.8rem;
    border-radius: 999px;
    padding: 4px 10px;
    background: linear-gradient(90deg, rgba(255, 123, 34, 0.2), rgba(250, 204, 21, 0.2));
    border: 1px solid rgba(255,255,255,0.14);
    display: inline-flex;
    align-items: center;
    gap: 4px;
  }

  .status-online {
    color: #22c55e;
    font-weight: 700;
  }

  .status-divider {
    color: #6b7280;
  }

  .social-links {
    display: flex;
    gap: 6px;
  }

  .social-link {
    display: flex;
    align-items: center;
    justify-content: center;
    width: 28px;
    height: 28px;
    border-radius: 6px;
    background: rgba(15, 23, 42, 0.6);
    border: 1px solid rgba(148, 163, 184, 0.3);
    color: #9ca3af;
    transition: all 0.2s;
    text-decoration: none;
  }

  .social-link:hover {
    background: rgba(255, 123, 34, 0.2);
    border-color: #ff7b22;
    color: #ff7b22;
    transform: translateY(-2px);
  }

  /* Title Block */
  .title-block {
    text-align: center;
    margin-bottom: 24px;
  }

  .main-title {
    font-weight: 700;
    text-transform: uppercase;
    letter-spacing: 0.16em;
    margin: 0 0 6px;
    color: #facc15;
    font-size: 2rem;
  }

  .muted {
    color: #9ca3af;
  }

  /* Burnice Section */
  .burnice-section {
    margin: 0 auto 24px;
    max-width: 120px;
    opacity: 0.7;
  }

  .burnice-video {
    width: 100%;
    height: auto;
    display: block;
    border-radius: 8px;
  }

  /* Card */
  .card-ne {
    background: #101318;
    border-radius: 16px;
    border: 1px solid rgba(255,255,255,0.08);
    box-shadow: 0 22px 45px rgba(0, 0, 0, 0.85);
    padding: 18px 18px 20px;
    margin-bottom: 16px;
  }

  /* Selector */
  .selector-row {
    display: flex;
    flex-direction: column;
    gap: 20px;
  }

  .selector-col {
    display: flex;
    flex-direction: column;
    gap: 8px;
  }

  .selector-label {
    font-size: 0.9rem;
  }

  select {
    background: #050816;
    color: #f9fafb;
    border-radius: 999px;
    border: 1px solid rgba(148, 163, 184, 0.55);
    padding: 8px 14px;
    font-size: 1rem;
    outline: none;
    cursor: pointer;
  }

  select:focus {
    border-color: #ff7b22;
    box-shadow: 0 0 0 2px rgba(255, 123, 34, 0.35);
  }

  /* Stats */
  .stats-bar {
    display: grid;
    grid-template-columns: repeat(3, 1fr);
    gap: 12px;
  }

  .stat-pill {
    padding: 14px 18px;
    border-radius: 12px;
    display: flex;
    flex-direction: column;
    gap: 6px;
    transition: all 0.2s;
    background: rgba(15, 23, 42, 0.7);
    border: 1px solid rgba(148, 163, 184, 0.3);
  }

  .stat-pill:hover {
    transform: translateY(-2px);
    background: rgba(30, 41, 59, 0.8);
    border-color: rgba(148, 163, 184, 0.5);
  }

  /* เน้นสีเฉพาะ value ตัวสำคัญ */
  .stat-first .stat-value { color: #93c5fd; }
  .stat-last .stat-value { color: #c4b5fd; }
  .stat-runs .stat-value { color: #fcd34d; }
  .stat-max .stat-value { color: #fca5a5; }
  .stat-min .stat-value { color: #86efac; }
  .stat-delta .stat-value { color: #fdba74; }
  .stat-days .stat-value { color: #c4b5fd; }

  .stat-pill-full {
    grid-column: 1 / -1;
    text-align: center;
    align-items: center;
  }

  .stat-label {
    font-size: 0.85rem;
    color: #d1d5db;
    font-weight: 600;
    text-transform: uppercase;
    letter-spacing: 0.05em;
  }

  .stat-value {
    font-size: 1.4rem;
    font-weight: 700;
    color: #facc15;
    line-height: 1.2;
  }

  .stat-value.positive { color: #22c55e; }
  .stat-value.negative { color: #ef4444; }

  .stat-date {
    font-size: 0.75rem;
    color: #9ca3af;
    margin-top: 4px;
    font-weight: 500;
  }

  /* Chart */
  .chart-header {
    display: flex;
    flex-wrap: wrap;
    justify-content: space-between;
    gap: 12px;
    align-items: center;
    margin-bottom: 10px;
  }

  .chart-header-left {
    display: flex;
    align-items: center;
    gap: 16px;
  }

  .boss-header-image {
    width: 64px;
    height: 64px;
    border-radius: 12px;
    object-fit: cover;
    border: 2px solid rgba(250, 204, 21, 0.5);
    box-shadow: 0 4px 12px rgba(0, 0, 0, 0.4);
  }

  .badge-phase {
    background: rgba(15, 23, 42, 0.9);
    border-radius: 999px;
    border: 1px solid rgba(255,255,255,0.16);
    font-size: 0.8rem;
    padding: 4px 10px;
    display: inline-block;
    margin-bottom: 4px;
  }

  .chart-title {
    margin: 0;
    font-size: 1.3rem;
  }

  .chart-note {
    font-size: 0.9rem;
  }

  .chart-shell {
    background: radial-gradient(circle at top, rgba(255,123,34,0.22), transparent 60%), #020617;
    border-radius: 16px;
    padding: 16px;
    border: 1px solid rgba(148, 163, 184, 0.4);
  }

  canvas {
    width: 100% !important;
    height: auto !important;
    max-height: 520px;
  }

  /* Footer */
  .footer {
    margin-top: 40px;
    padding: 20px 0;
    text-align: center;
    border-top: 1px solid rgba(148, 163, 184, 0.2);
  }

  .footer p {
    margin: 0 0 8px 0;
    font-size: 0.9rem;
    color: #9ca3af;
  }

  .footer p:last-child {
    margin-bottom: 0;
  }

  .footer-credit {
    font-size: 0.75rem !important;
    color: #6b7280 !important;
  }

  .footer-credit a {
    color: #9ca3af;
    text-decoration: none;
    transition: color 0.2s;
  }

  .footer-credit a:hover {
    color: #ff7b22;
  }

  .heart {
    color: #ff7b22;
    display: inline-block;
    animation: heartbeat 1.5s ease-in-out infinite;
  }

  @keyframes heartbeat {
    0%, 100% { transform: scale(1); }
    10%, 30% { transform: scale(1.1); }
    20%, 40% { transform: scale(1); }
  }

  /* Content Layout with Sidebar */
  .content-with-image {
    display: flex;
    gap: 24px;
    align-items: flex-start;
  }

  .main-content {
    flex: 1;
    min-width: 0;
  }

  .boss-sidebar {
    width: 300px;
    flex-shrink: 0;
    position: sticky;
    top: 24px;
  }

  .boss-image-wrapper {
    position: relative;
    border-radius: 16px;
    overflow: hidden;
    box-shadow: 0 8px 24px rgba(0, 0, 0, 0.6);
    border: 2px solid rgba(250, 204, 21, 0.5);
  }

  .boss-large-image {
    width: 100%;
    height: auto;
    display: block;
    object-fit: cover;
  }

  .boss-name-overlay {
    position: absolute;
    bottom: 0;
    left: 0;
    right: 0;
    background: linear-gradient(to top, rgba(0, 0, 0, 0.9), transparent);
    padding: 16px 12px 12px;
    color: #facc15;
    font-weight: 700;
    font-size: 1.1rem;
    text-align: center;
    text-shadow: 0 2px 4px rgba(0, 0, 0, 0.8);
  }

  /* Responsive */
  @media (max-width: 1024px) {
    .content-with-image {
      flex-direction: column;
    }

    .boss-sidebar {
      width: 100%;
      position: static;
      max-width: 400px;
      margin: 0 auto;
    }
  }

  @media (max-width: 768px) {
    .ne-topbar {
      flex-direction: column;
      align-items: flex-start;
      gap: 8px;
    }
    .topbar-right {
      width: 100%;
      justify-content: space-between;
    }
    .stats-bar {
      grid-template-columns: repeat(2, 1fr);
      gap: 10px;
    }
    .stat-pill {
      padding: 12px 14px;
    }
    .stat-label {
      font-size: 0.8rem;
    }
    .stat-value {
      font-size: 1.15rem;
    }
    .burnice-section {
      max-width: 100px;
    }
    .boss-header-image {
      width: 48px;
      height: 48px;
    }

    .boss-sidebar {
      max-width: 300px;
    }
  }

  @media (max-width: 480px) {
    .stats-bar {
      grid-template-columns: 1fr;
    }
    .stat-value {
      font-size: 1.05rem;
    }
  }
</style>
