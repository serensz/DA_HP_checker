<script>
  export let currentPage = "chart";
</script>

<nav class="nav-bar">
  <button 
    class="nav-btn" 
    class:active={currentPage === "chart"}
    on:click={() => window.location.hash = "chart"}
  >
    📊 HP Trends
  </button>
  <button 
    class="nav-btn" 
    class:active={currentPage === "table"}
    on:click={() => window.location.hash = "table"}
  >
    📋 Boss Data
  </button>
</nav>

<style>
  .nav-bar {
    display: flex;
    gap: 12px;
    margin-bottom: 24px;
    justify-content: center;
  }

  .nav-btn {
    background: rgba(15, 23, 42, 0.9);
    color: #f9fafb;
    border: 1px solid rgba(148, 163, 184, 0.4);
    border-radius: 999px;
    padding: 10px 24px;
    font-size: 0.95rem;
    font-weight: 600;
    cursor: pointer;
    transition: all 0.2s;
  }

  .nav-btn:hover {
    background: rgba(255, 123, 34, 0.2);
    border-color: #ff7b22;
    transform: translateY(-2px);
  }

  .nav-btn.active {
    background: linear-gradient(90deg, rgba(255, 123, 34, 0.3), rgba(250, 204, 21, 0.3));
    border-color: #ff7b22;
    box-shadow: 0 0 20px rgba(255, 123, 34, 0.4);
  }
</style>
