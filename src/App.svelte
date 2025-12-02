<script>
  import { onMount } from "svelte";
  import Chart from "chart.js/auto";

  let bosses = [];
  let selectedName = "";
  let chart;
  let canvasEl;

  onMount(async () => {
    const base = import.meta.env.BASE_URL || '/';
    const res = await fetch(`${base}bosses.json`);
    bosses = await res.json();

    bosses.sort((a, b) => a.boss_name.localeCompare(b.boss_name));
    selectedName = bosses[0]?.boss_name ?? "";

    initChart();
  });

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

    return { boss, first, last, max, min, diff, pct, runs: boss.timeline.length };
  })();
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
          <span class="fw-semibold">ONLINE</span>
          <span class="muted">Boss records synced</span>
        </span>
      </div>
    </div>

    <div class="title-block">
      <h1 class="main-title">Boss HP Growth Trends</h1>
      <p class="muted">
        ดูว่า HP ของแต่ละบอสเติบโตยังไงตั้งแต่เปิดตัวจนถึงรอบกิจกรรมล่าสุด
      </p>
    </div>

    <!-- Selector + stats -->
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
              <div class="stat-pill">
                <span class="stat-label">ครั้งแรก</span>
                <span class="stat-value">{stats.first.toLocaleString()}</span>
              </div>
              <div class="stat-pill">
                <span class="stat-label">ล่าสุด</span>
                <span class="stat-value">{stats.last.toLocaleString()}</span>
              </div>
              <div class="stat-pill">
                <span class="stat-label">สูงสุด</span>
                <span class="stat-value">{stats.max.toLocaleString()}</span>
              </div>
              <div class="stat-pill">
                <span class="stat-label">ต่ำสุด</span>
                <span class="stat-value">{stats.min.toLocaleString()}</span>
              </div>
              <div class="stat-pill">
                <span class="stat-label">Δ จากครั้งแรก</span>
                <span class="stat-value">
                  {stats.diff >= 0 ? "+" : ""}{stats.diff.toLocaleString()}
                  {" "}
                  ({stats.diff >= 0 ? "+" : ""}{stats.pct}%)
                </span>
              </div>
              <div class="stat-pill">
                <span class="stat-label">จำนวนรอบ</span>
                <span class="stat-value">{stats.runs}</span>
              </div>
            </div>
          {/if}
        </div>
      </div>
    </div>

    <!-- Chart card -->
    <div class="card-ne">
      <div class="chart-header">
        <div>
          <div class="badge-phase" id="chartSubtitle">
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
        <div class="chart-note muted">
          หนึ่งจุด = HP ของบอสในกิจกรรมแต่ละรอบ
        </div>
      </div>

      <div class="chart-shell">
        <canvas bind:this={canvasEl}></canvas>
      </div>
    </div>

  </div>
</div>

<style>
  :global(body) {
    margin: 0;
    min-height: 100vh;
    font-family: system-ui, -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif;
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
    font-size: 1.05rem;
    letter-spacing: 0.25em;
    text-transform: uppercase;
    font-weight: 700;
  }

  .ne-logo-text span {
    color: #ff7b22;
  }

  .ne-subtitle {
    font-size: 0.8rem;
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
    border-radius: 999px;
    background: #ff7b22;
    box-shadow: 0 0 8px #ff9100;
  }

  .ne-status-pill {
    font-size: 0.75rem;
    border-radius: 999px;
    padding: 4px 10px;
    background: linear-gradient(
      90deg,
      rgba(255, 123, 34, 0.2),
      rgba(250, 204, 21, 0.2)
    );
    border: 1px solid rgba(255,255,255,0.14);
    display: inline-flex;
    align-items: center;
    gap: 6px;
  }

  .muted {
    color: #9ca3af;
  }

  .title-block {
    text-align: center;
    margin-bottom: 20px;
  }

  .main-title {
    font-weight: 700;
    text-transform: uppercase;
    letter-spacing: 0.16em;
    margin: 0 0 6px;
    color: #facc15;
  }

  .card-ne {
    background: #101318;
    border-radius: 16px;
    border: 1px solid rgba(255,255,255,0.08);
    box-shadow:
      0 22px 45px rgba(0, 0, 0, 0.85),
      0 0 0 1px rgba(148, 163, 184, 0.18);
    padding: 18px 18px 20px;
  }

  .selector-row {
    display: flex;
    flex-wrap: wrap;
    gap: 18px;
    align-items: center;
  }

  .selector-col {
    flex: 0 0 260px;
    max-width: 100%;
    display: flex;
    flex-direction: column;
    gap: 4px;
  }

  .selector-label {
    font-size: 0.8rem;
  }

  select {
    background: #050816;
    color: #f9fafb;
    border-radius: 999px;
    border: 1px solid rgba(148, 163, 184, 0.55);
    padding: 8px 14px;
    font-size: 0.9rem;
    outline: none;
  }

  select:focus {
    border-color: #ff7b22;
    box-shadow: 0 0 0 2px rgba(255, 123, 34, 0.35);
  }

  .stats-col {
    flex: 1 1 auto;
  }

  .stats-bar {
    display: flex;
    flex-wrap: wrap;
    gap: 10px;
    justify-content: flex-end;
  }

  .stat-pill {
    background: rgba(15, 23, 42, 0.9);
    padding: 8px 14px;
    border-radius: 12px;
    display: inline-flex;
    flex-direction: column;
    min-width: 130px;
    border: 1px solid rgba(148, 163, 184, 0.4);
    box-shadow: 0 0 0 1px rgba(15,23,42,0.9);
  }

  .stat-label {
    font-size: 0.75rem;
    color: #9ca3af;
  }

  .stat-value {
    font-size: 0.95rem;
    font-weight: 600;
    color: #f9fafb;
  }

  .chart-header {
    display: flex;
    flex-wrap: wrap;
    justify-content: space-between;
    gap: 10px;
    align-items: center;
    margin-bottom: 10px;
  }

  .badge-phase {
    background: rgba(15, 23, 42, 0.9);
    border-radius: 999px;
    border: 1px solid rgba(255,255,255,0.16);
    font-size: 0.75rem;
    padding: 4px 10px;
    display: inline-block;
    margin-bottom: 4px;
  }

  .chart-title {
    margin: 0;
  }

  .chart-note {
    font-size: 0.8rem;
  }

  .chart-shell {
    background:
      radial-gradient(circle at top, rgba(255,123,34,0.22), transparent 60%),
      #020617;
    border-radius: 16px;
    padding: 16px;
    border: 1px solid rgba(148, 163, 184, 0.4);
  }

  canvas {
    width: 100% !important;
    height: auto !important;
    max-height: 520px;
  }

  @media (max-width: 768px) {
    .ne-topbar {
      flex-direction: column;
      align-items: flex-start;
      gap: 8px;
    }
    .stats-bar {
      justify-content: flex-start;
    }
    .selector-row {
      flex-direction: column;
      align-items: stretch;
    }
    .selector-col {
      flex: 1 1 auto;
    }
  }
</style>
