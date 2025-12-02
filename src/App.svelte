<script>
  import { onMount } from "svelte";
  import Chart from "chart.js/auto";

  let bosses = [];
  let selectedName = "";
  let chart;
  let canvasEl;

  // โหลดข้อมูล bosses.json ด้วย path ที่รองรับทั้ง dev และ GitHub Pages
  onMount(async () => {
    const base = import.meta.env.BASE_URL;       // <-- จุดสำคัญ
    const url = `${base}bosses.json`;

    const res = await fetch(url);
    bosses = await res.json();

    bosses.sort((a, b) => a.boss_name.localeCompare(b.boss_name));
    selectedName = bosses[0]?.boss_name ?? "";

    initChart();
  });

  // สร้างกราฟ
  function initChart() {
    if (!canvasEl || !selectedName) return;

    const bossData = bosses.find((b) => b.boss_name === selectedName);
    if (!bossData) return;

    const labels = bossData.timeline.map((t) => t.date);
    const hpValues = bossData.timeline.map((t) => t.hp);

    // ล้าง chart เก่าออกก่อน
    if (chart) chart.destroy();

    chart = new Chart(canvasEl, {
      type: "line",
      data: {
        labels,
        datasets: [
          {
            label: `${selectedName} HP Trend`,
            data: hpValues,
            borderColor: "#4db8ff",
            backgroundColor: "rgba(77,184,255,0.15)",
            borderWidth: 2,
            tension: 0.2,
            pointRadius: 4,
            pointHoverRadius: 6,
            pointBackgroundColor: "#4db8ff"
          }
        ]
      },
      options: {
        responsive: true,
        maintainAspectRatio: false,
        scales: {
          y: {
            ticks: {
              callback: (value) =>
                value.toLocaleString("en-US"), // format ตัวเลข
            },
          },
        },
      },
    });
  }

  // อัปเดตกราฟเมื่อเลือกบอสใหม่
  $: if (bosses.length > 0 && selectedName) {
    initChart();
  }
</script>

<style>
  .container {
    max-width: 900px;
    margin: 0 auto;
    padding: 1.5rem;
    color: white;
  }

  .title {
    text-align: center;
    font-size: 2rem;
    margin-bottom: 1.2rem;
  }

  select {
    padding: 0.5rem 1rem;
    margin-bottom: 1rem;
    border-radius: 6px;
    background: #1e1e1e;
    color: white;
    border: 1px solid #333;
  }

  .chart-box {
    background: #111;
    border-radius: 12px;
    padding: 1rem;
    height: 420px;
  }
</style>

<div class="container">
  <h1 class="title">ZZZ Boss HP Growth Trends</h1>

  <label>
    เลือกบอส:
    <select bind:value={selectedName}>
      {#each bosses as b}
        <option value={b.boss_name}>{b.boss_name}</option>
      {/each}
    </select>
  </label>

  <div class="chart-box">
    <canvas bind:this={canvasEl}></canvas>
  </div>
</div>
