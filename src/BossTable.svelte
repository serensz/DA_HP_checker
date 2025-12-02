<script>
  export let bosses = [];

  let sortBy = "name";
  let sortOrder = "asc";

  $: sortedBosses = [...bosses].sort((a, b) => {
    const aStats = getBossStats(a);
    const bStats = getBossStats(b);

    let compareValue = 0;
    switch (sortBy) {
      case "name":
        compareValue = a.boss_name.localeCompare(b.boss_name);
        break;
      case "first":
        compareValue = aStats.first - bStats.first;
        break;
      case "last":
        compareValue = aStats.last - bStats.last;
        break;
      case "max":
        compareValue = aStats.max - bStats.max;
        break;
      case "growth":
        compareValue = aStats.pct - bStats.pct;
        break;
      case "runs":
        compareValue = aStats.runs - bStats.runs;
        break;
      case "days":
        compareValue = aStats.daysPassed - bStats.daysPassed;
        break;
    }

    return sortOrder === "asc" ? compareValue : -compareValue;
  });

  function getBossStats(boss) {
    if (!boss.timeline || boss.timeline.length === 0) {
      return { first: 0, last: 0, max: 0, min: 0, diff: 0, pct: 0, runs: 0, lastDate: "", daysPassed: 0 };
    }

    const hp = boss.timeline.map((t) => t.hp);
    const first = hp[0] || 0;
    const last = hp[hp.length - 1] || 0;
    const max = Math.max(...hp);
    const min = Math.min(...hp);
    const diff = last - first;
    const pct = first ? parseFloat(((diff / first) * 100).toFixed(1)) : 0;

    // คำนวณจำนวนวันที่ผ่านไป
    const lastDateObj = new Date(boss.timeline[boss.timeline.length - 1].date);
    const todayObj = new Date();
    // @ts-ignore
    const daysPassed = Math.floor((todayObj - lastDateObj) / (1000 * 60 * 60 * 24));

    return {
      first,
      last,
      max,
      min,
      diff,
      pct,
      runs: boss.timeline.length,
      lastDate: lastDateObj.toLocaleDateString('th-TH', { year: 'numeric', month: 'short', day: 'numeric' }),
      daysPassed
    };
  }

  function toggleSort(column) {
    if (sortBy === column) {
      sortOrder = sortOrder === "asc" ? "desc" : "asc";
    } else {
      sortBy = column;
      sortOrder = "desc";
    }
  }

  // Helper function to get boss image path
  function getBossImage(boss) {
    const base = import.meta.env.BASE_URL || '/';
    return boss?.image ? `${base}${boss.image}` : null;
  }

  // Fallback image ถ้าโหลดไม่ได้
  function handleImageError(e) {
    e.target.style.display = 'none';
  }
</script>

<div class="table-container">
  <div class="card-ne">
    <div class="table-header">
      <h2>Boss Data Overview</h2>
      <p class="muted">ข้อมูลสถิติของบอสทั้งหมด คลิกหัวตารางเพื่อเรียงลำดับ</p>
    </div>

    <div class="table-wrapper">
      <table>
        <thead>
          <tr>
            <th on:click={() => toggleSort("name")} class:active={sortBy === "name"}>
              Boss Name {sortBy === "name" ? (sortOrder === "asc" ? "↑" : "↓") : ""}
            </th>
            <th on:click={() => toggleSort("first")} class:active={sortBy === "first"}>
              ครั้งแรก {sortBy === "first" ? (sortOrder === "asc" ? "↑" : "↓") : ""}
            </th>
            <th on:click={() => toggleSort("last")} class:active={sortBy === "last"}>
              ล่าสุด {sortBy === "last" ? (sortOrder === "asc" ? "↑" : "↓") : ""}
            </th>
            <th on:click={() => toggleSort("max")} class:active={sortBy === "max"}>
              สูงสุด {sortBy === "max" ? (sortOrder === "asc" ? "↑" : "↓") : ""}
            </th>
            <th on:click={() => toggleSort("growth")} class:active={sortBy === "growth"}>
              Growth % {sortBy === "growth" ? (sortOrder === "asc" ? "↑" : "↓") : ""}
            </th>
            <th on:click={() => toggleSort("runs")} class:active={sortBy === "runs"}>
              จำนวนรอบ {sortBy === "runs" ? (sortOrder === "asc" ? "↑" : "↓") : ""}
            </th>
            <th on:click={() => toggleSort("days")} class:active={sortBy === "days"}>
              มาครั้งสุดท้าย {sortBy === "days" ? (sortOrder === "asc" ? "↑" : "↓") : ""}
            </th>
          </tr>
        </thead>
        <tbody>
          {#each sortedBosses as boss}
            {@const stats = getBossStats(boss)}
            <tr>
              <td class="boss-name">
                <div class="boss-info">
                  {#if getBossImage(boss)}
                    <img 
                      src={getBossImage(boss)} 
                      alt={boss.boss_name}
                      class="boss-avatar"
                      on:error={handleImageError}
                      loading="lazy"
                    />
                  {/if}
                  <span>{boss.boss_name}</span>
                </div>
              </td>
              <td>{stats.first.toLocaleString()}</td>
              <td>{stats.last.toLocaleString()}</td>
              <td>{stats.max.toLocaleString()}</td>
              <td class:positive={stats.pct >= 0} class:negative={stats.pct < 0}>
                {stats.pct >= 0 ? "+" : ""}{stats.pct}%
              </td>
              <td>{stats.runs}</td>
              <td class="text-center">
                <div class="days-ago">
                  <span class="days-value">{stats.daysPassed} วัน</span>
                  <span class="date-value">{stats.lastDate}</span>
                </div>
              </td>
            </tr>
          {/each}
        </tbody>
      </table>
    </div>
  </div>
</div>

<style>
  .table-container {
    width: 100%;
  }

  .card-ne {
    background: #101318;
    border-radius: 16px;
    border: 1px solid rgba(255,255,255,0.08);
    box-shadow: 0 22px 45px rgba(0, 0, 0, 0.85);
    padding: 24px;
  }

  .table-header {
    margin-bottom: 20px;
  }

  .table-header h2 {
    margin: 0 0 8px 0;
    color: #facc15;
    font-size: 1.5rem;
    text-transform: uppercase;
    letter-spacing: 0.1em;
  }

  .muted {
    color: #9ca3af;
    font-size: 0.9rem;
  }

  .table-wrapper {
    overflow-x: auto;
  }

  table {
    width: 100%;
    border-collapse: collapse;
  }

  th {
    background: rgba(15, 23, 42, 0.9);
    color: #f9fafb;
    padding: 12px 16px;
    text-align: left;
    font-weight: 600;
    border-bottom: 2px solid rgba(148, 163, 184, 0.4);
    cursor: pointer;
    transition: background 0.2s;
    white-space: nowrap;
  }

  th:hover {
    background: rgba(255, 123, 34, 0.2);
  }

  th.active {
    background: rgba(255, 123, 34, 0.3);
    color: #ff7b22;
  }

  td {
    padding: 12px 16px;
    border-bottom: 1px solid rgba(148, 163, 184, 0.2);
    color: #f9fafb;
  }

  tr:hover td {
    background: rgba(255, 123, 34, 0.1);
  }

  .boss-name {
    font-weight: 600;
    color: #facc15;
  }

  .boss-info {
    display: flex;
    align-items: center;
    gap: 12px;
  }

  .boss-avatar {
    width: 40px;
    height: 40px;
    border-radius: 8px;
    object-fit: cover;
    border: 2px solid rgba(250, 204, 21, 0.4);
    flex-shrink: 0;
  }

  .positive {
    color: #22c55e;
    font-weight: 600;
  }

  .negative {
    color: #ef4444;
    font-weight: 600;
  }

  .days-ago {
    display: flex;
    flex-direction: column;
    gap: 2px;
  }

  .days-value {
    font-weight: 600;
    color: #facc15;
  }

  .date-value {
    font-size: 0.75rem;
    color: #6b7280;
  }

  @media (max-width: 768px) {
    .card-ne {
      padding: 16px;
    }

    th, td {
      padding: 8px 10px;
      font-size: 0.85rem;
    }

    .table-header h2 {
      font-size: 1.2rem;
    }

    .boss-avatar {
      width: 32px;
      height: 32px;
    }
  }
</style>
