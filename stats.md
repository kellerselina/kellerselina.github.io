---
layout: default
---

<div id="password_overlay" class="password-overlay">
  <div class="password-box">
    <h3>enter password</h3>
    <input type="password" id="password_input" placeholder="password (press enter)">
    <p id="password_error" class="password-error">incorrect password</p>
  </div>
</div>

<div class="stats-page" id="stats_content" style="display:none;">
  <h1>Billable Hours Stats</h1>
  <p>Upload a CSV with columns <code>date</code>, <code>hours</code>, <code>type</code>. Dates should be in <code>YYYY-MM-DD</code>.</p>

  <div class="upload">
    <label for="csvFile"><strong>CSV file</strong></label>
    <input id="csvFile" type="file" accept=".csv,.xlsx,application/vnd.openxmlformats-officedocument.spreadsheetml.sheet,text/csv" />
    <div id="status" class="status" aria-live="polite"></div>
  </div>

  <div class="grid">
    <section class="card">
      <h2>Weekly</h2>
      <canvas id="chartWeekly" height="150"></canvas>
      <button class="table-toggle" type="button" data-target="tableWeeklyWrap">Show table</button>
      <div class="table-wrap" id="tableWeeklyWrap" hidden>
        <table id="tableWeekly" class="data-table">
          <thead><tr><th>week</th><th>hours</th></tr></thead>
          <tbody></tbody>
        </table>
      </div>
    </section>

    <section class="card">
      <h2>Biweekly (14 days)</h2>
      <canvas id="chartBiweekly" height="150"></canvas>
      <button class="table-toggle" type="button" data-target="tableBiweeklyWrap">Show table</button>
      <div class="table-wrap" id="tableBiweeklyWrap" hidden>
        <table id="tableBiweekly" class="data-table">
          <thead><tr><th>two_weeks</th><th>hours</th></tr></thead>
          <tbody></tbody>
        </table>
      </div>
    </section>

    <section class="card">
      <h2>Monthly</h2>
      <canvas id="chartMonthly" height="150"></canvas>
      <button class="table-toggle" type="button" data-target="tableMonthlyWrap">Show table</button>
      <div class="table-wrap" id="tableMonthlyWrap" hidden>
        <table id="tableMonthly" class="data-table">
          <thead><tr><th>month</th><th>hours</th></tr></thead>
          <tbody></tbody>
        </table>
      </div>
    </section>
  </div>
</div>

<style>
  .stats-page {
    max-width: 900px;
    margin: 0 auto;
  }
  #author-name {
    font-family: "Inconsolata", monospace;
    text-transform: none;
  }
  .navbar-ul { display: none; }
  .upload {
    margin: 1rem 0 1.5rem 0;
    display: grid;
    gap: 0.5rem;
  }
  .status {
    font-size: 0.9rem;
    color: #333;
  }
  .grid {
    display: grid;
    gap: 1.5rem;
  }
  .card {
    padding: 1rem;
    border: 1px solid #e5e5e5;
    border-radius: 8px;
    background: #fafafa;
  }
  .card canvas {
    width: 100%;
    max-height: 275px;
  }
  .table-toggle {
    margin-top: 0.5rem;
    background: transparent;
    border: 1px solid #bbb;
    padding: 0.35rem 0.6rem;
    border-radius: 6px;
    cursor: pointer;
    font-size: 0.9rem;
  }
  .password-overlay {
    position: fixed;
    top: 0;
    left: 0;
    width: 100%;
    height: 100%;
    background: white;
    z-index: 10000;
    display: flex;
    align-items: center;
    justify-content: center;
  }
  .password-box {
    text-align: center;
    padding: 30px;
    border: 1px solid #ddd;
    border-radius: 5px;
    background: #f9f9f9;
  }
  .password-box h3 { margin-bottom: 20px; }
  .password-box input {
    padding: 10px;
    border: 1px solid #ddd;
    border-radius: 3px;
    font-family: "Inconsolata", monospace;
    margin-bottom: 10px;
    width: 200px;
  }
  .password-error {
    color: #ff4444;
    margin-top: 10px;
    display: none;
  }
  .table-wrap {
    overflow-x: auto;
    margin-top: 0.75rem;
  }
  .data-table {
    width: 100%;
    border-collapse: collapse;
    font-size: 0.9rem;
  }
  .data-table th,
  .data-table td {
    text-align: left;
    padding: 0.2rem 0.35rem;
    border-bottom: 1px solid #ddd;
    white-space: nowrap;
  }
  @media (min-width: 900px) {
    .grid {
      grid-template-columns: 1fr;
    }
  }
</style>

<script src="https://cdn.jsdelivr.net/npm/papaparse@5.4.1/papaparse.min.js"></script>
<script src="files/xlsx.full.min.js"></script>
<script src="https://cdn.jsdelivr.net/npm/chart.js@4.4.1/dist/chart.umd.min.js"></script>
<script>
  const keepTypes = new Set([
    "billable",
    "pro_bono",
    "recruitment",
    "management",
    "practice_development",
  ]);

  const typeMap = {
    "OTH": "others",
    "BIL": "billable",
    "PSQ": "pro_bono",
    "REC": "recruitment",
    "MAN": "management",
    "ADM": "administrative",
    "PD": "practice_development",
    "SICK": "sick",
    "VAC": "vacation",
  };

  const statusEl = document.getElementById("status");
  const fileInput = document.getElementById("csvFile");

  let chartWeekly = null;
  let chartBiweekly = null;
  let chartMonthly = null;
  const STATS_PASSWORD = "fands_2025";

  function setStatus(msg) {
    statusEl.textContent = msg;
  }

  function checkPassword() {
    if (sessionStorage.getItem("stats_authenticated") === "true") {
      document.getElementById("password_overlay").style.display = "none";
      document.getElementById("stats_content").style.display = "block";
      return true;
    }
    return false;
  }

  function authenticate() {
    const input = document.getElementById("password_input").value;
    if (input === STATS_PASSWORD) {
      sessionStorage.setItem("stats_authenticated", "true");
      document.getElementById("password_overlay").style.display = "none";
      document.getElementById("stats_content").style.display = "block";
    } else {
      document.getElementById("password_error").style.display = "block";
      document.getElementById("password_input").value = "";
      document.getElementById("password_input").focus();
    }
  }

  document.addEventListener("DOMContentLoaded", () => {
    const author = document.getElementById("author-name");
    if (author) author.textContent = "\\keller";
    const footerLink = document.querySelector(".container.content p a");
    if (footerLink) {
      const span = document.createElement("span");
      span.innerHTML = footerLink.innerHTML;
      footerLink.replaceWith(span);
    }
    if (!checkPassword()) {
      const input = document.getElementById("password_input");
      input.focus();
      input.addEventListener("keypress", (e) => {
        if (e.key === "Enter") authenticate();
      });
      return;
    }
  });

  function pad2(n) {
    return String(n).padStart(2, "0");
  }

  function formatDateUTC(dt) {
    return `${dt.getUTCFullYear()}-${pad2(dt.getUTCMonth() + 1)}-${pad2(dt.getUTCDate())}`;
  }

  function parseDate(raw) {
    if (!raw) return null;
    if (raw instanceof Date && !isNaN(raw)) {
      return new Date(Date.UTC(raw.getFullYear(), raw.getMonth(), raw.getDate()));
    }
    if (typeof raw === "number" && Number.isFinite(raw) && typeof XLSX !== "undefined" && XLSX && XLSX.SSF) {
      const p = XLSX.SSF.parse_date_code(raw);
      if (p && p.y && p.m && p.d) {
        return new Date(Date.UTC(p.y, p.m - 1, p.d));
      }
    }
    const s = String(raw).trim();
    let m = s.match(/^(\d{4})[-/](\d{2})[-/](\d{2})(?:[ T].*)?$/);
    if (m) {
      const y = Number(m[1]);
      const mo = Number(m[2]);
      const d = Number(m[3]);
      if (!y || !mo || !d) return null;
      return new Date(Date.UTC(y, mo - 1, d));
    }
    m = s.match(/^(\d{1,2})\/(\d{1,2})\/(\d{2,4})(?:[ T].*)?$/);
    if (m) {
      const mo = Number(m[1]);
      const d = Number(m[2]);
      let y = Number(m[3]);
      if (y < 100) y += 2000;
      if (!y || !mo || !d) return null;
      return new Date(Date.UTC(y, mo - 1, d));
    }
    return null;
  }

  function weekStartMondayUTC(dt) {
    const day = dt.getUTCDay();
    const diff = (day + 6) % 7;
    return new Date(Date.UTC(dt.getUTCFullYear(), dt.getUTCMonth(), dt.getUTCDate() - diff));
  }

  function biweekStartMondayUTC(dt) {
    const weekStart = weekStartMondayUTC(dt);
    const epoch = Date.UTC(1970, 0, 5);
    const weeksSince = Math.floor((weekStart.getTime() - epoch) / (7 * 86400000));
    const biweekIndex = Math.floor(weeksSince / 2);
    return new Date(epoch + biweekIndex * 2 * 7 * 86400000);
  }

  function monthKeyUTC(dt) {
    return `${dt.getUTCFullYear()}-${pad2(dt.getUTCMonth() + 1)}`;
  }

  function normalizeHeaders(fields) {
    const map = {};
    for (const f of fields) {
      const key = String(f).trim().toLowerCase().replace(/[^a-z0-9]+/g, " ").trim();
      if (key === "date" || key === "work date") map.date = f;
      if (key === "hours" || key === "work hours") map.hours = f;
      if (key === "type" || key === "work type") map.type = f;
    }
    return map;
  }

  function ensureXlsxLoaded() {
    return new Promise((resolve, reject) => {
      if (typeof XLSX !== "undefined") return resolve();
      const script = document.createElement("script");
      script.src = "files/xlsx.full.min.js";
      script.onload = () => resolve();
      script.onerror = () => reject(new Error("Failed to load XLSX library."));
      document.head.appendChild(script);
    });
  }

  function fromXlsxFile(file) {
    return new Promise((resolve, reject) => {
      const reader = new FileReader();
      reader.onload = (e) => {
        try {
          const data = new Uint8Array(e.target.result);
          const wb = XLSX.read(data, { type: "array", cellDates: true });
          if (!wb.SheetNames || !wb.SheetNames.length) {
            throw new Error("No sheets found.");
          }
          const ws = wb.Sheets[wb.SheetNames[0]];
          const rows = XLSX.utils.sheet_to_json(ws, { header: 1, defval: "", raw: false });
          resolve(rows);
        } catch (err) {
          reject(err);
        }
      };
      reader.onerror = () => reject(new Error("Failed to read file."));
      reader.readAsArrayBuffer(file);
    });
  }

  function toFloat(v) {
    const num = Number(v);
    return Number.isFinite(num) ? num : null;
  }

  function parseRows(rows, headerMap) {
    const cleaned = [];
    for (const row of rows) {
      const rawDate = row[headerMap.date];
      const rawHours = row[headerMap.hours];
      const rawType = row[headerMap.type];
      const dt = parseDate(rawDate);
      const hours = toFloat(rawHours);
      if (!dt || hours === null || rawType === undefined || rawType === null) continue;
      const code = String(rawType).trim().toUpperCase();
      const mapped = typeMap[code] || String(rawType).trim().toLowerCase();
      cleaned.push({ dt, hours, type: mapped });
    }
    return cleaned;
  }

  function aggregate(cleaned) {
    const weekly = new Map();
    const biweekly = new Map();
    const monthly = new Map();

    for (const row of cleaned) {
      if (!keepTypes.has(row.type)) continue;
      const w = formatDateUTC(weekStartMondayUTC(row.dt));
      const bw = formatDateUTC(biweekStartMondayUTC(row.dt));
      const m = monthKeyUTC(row.dt);

      weekly.set(w, (weekly.get(w) || 0) + row.hours);
      biweekly.set(bw, (biweekly.get(bw) || 0) + row.hours);
      monthly.set(m, (monthly.get(m) || 0) + row.hours);
    }

    const toSortedArray = (map) => {
      return Array.from(map.entries())
        .sort((a, b) => a[0].localeCompare(b[0]))
        .map(([k, v]) => ({ key: k, value: v }));
    };

    return {
      weekly: toSortedArray(weekly),
      biweekly: toSortedArray(biweekly),
      monthly: toSortedArray(monthly),
    };
  }

  function renderTable(tableId, rows, keyLabel) {
    const tbody = document.querySelector(`#${tableId} tbody`);
    tbody.innerHTML = "";
    for (const row of rows) {
      const tr = document.createElement("tr");
      const tdKey = document.createElement("td");
      const tdVal = document.createElement("td");
      tdKey.textContent = row.key;
      tdVal.textContent = row.value.toFixed(2);
      tr.appendChild(tdKey);
      tr.appendChild(tdVal);
      tbody.appendChild(tr);
    }
  }

  function renderChart(canvasId, rows, title) {
    const labels = rows.map((r) => r.key);
    const data = rows.map((r) => Number(r.value.toFixed(2)));
    const ctx = document.getElementById(canvasId).getContext("2d");
    return new Chart(ctx, {
      type: "line",
      data: {
        labels,
        datasets: [{
          label: title,
          data,
          borderColor: "#111",
          backgroundColor: "rgba(0,0,0,0.05)",
          borderWidth: 1.5,
          pointRadius: 1.5,
          tension: 0.1,
        }],
      },
      options: {
        responsive: true,
        maintainAspectRatio: false,
        plugins: {
          legend: { display: false },
        },
        scales: {
          x: {
            ticks: {
              maxRotation: 30,
              minRotation: 30,
            },
          },
          y: {
            beginAtZero: true,
          },
        },
      },
    });
  }

  function destroyCharts() {
    if (chartWeekly) chartWeekly.destroy();
    if (chartBiweekly) chartBiweekly.destroy();
    if (chartMonthly) chartMonthly.destroy();
    chartWeekly = chartBiweekly = chartMonthly = null;
  }

  function findHeaderRow(rows) {
    for (let i = 0; i < rows.length; i++) {
      const row = rows[i] || [];
      const headerMap = normalizeHeaders(row);
      if (headerMap.date && headerMap.hours && headerMap.type) return i;
    }
    return -1;
  }

  function rowsToObjects(rows, headerIndex) {
    const header = rows[headerIndex].map((h) => String(h).trim());
    const out = [];
    for (let i = headerIndex + 1; i < rows.length; i++) {
      const r = rows[i] || [];
      if (!r.length) continue;
      const obj = {};
      for (let c = 0; c < header.length; c++) {
        if (!header[c]) continue;
        obj[header[c]] = r[c];
      }
      out.push(obj);
    }
    return { data: out, fields: header };
  }

  function handleRows(rows, fields) {
    const headerMap = normalizeHeaders(fields);
    if (!headerMap.date || !headerMap.hours || !headerMap.type) {
      const shown = fields.slice(0, 10).join(", ");
      setStatus(`Missing columns. Need date, hours, type (or Work Date, Work Hours, Work Type). Found: ${shown}`);
      return;
    }

    const cleaned = parseRows(rows, headerMap);
    const agg = aggregate(cleaned);
    destroyCharts();

    renderTable("tableWeekly", agg.weekly);
    renderTable("tableBiweekly", agg.biweekly);
    renderTable("tableMonthly", agg.monthly);

    chartWeekly = renderChart("chartWeekly", agg.weekly, "Weekly hours");
    chartBiweekly = renderChart("chartBiweekly", agg.biweekly, "Biweekly hours");
    chartMonthly = renderChart("chartMonthly", agg.monthly, "Monthly hours");

    setStatus(`Loaded ${cleaned.length} rows. Showing billable/pro bono/recruitment/management/practice development only.`);
  }

  fileInput.addEventListener("change", () => {
    const file = fileInput.files[0];
    if (!file) return;

    const name = (file.name || "").toLowerCase();
    if (name.endsWith(".xlsx")) {
      setStatus("Parsing XLSX...");
      ensureXlsxLoaded().then(() => {
        return fromXlsxFile(file);
      }).then((rows) => {
        if (!rows.length) {
          setStatus("XLSX appears empty.");
          return;
        }
        const headerIndex = findHeaderRow(rows);
        let parsed = null;
        if (headerIndex !== -1) {
          parsed = rowsToObjects(rows, headerIndex);
          handleRows(parsed.data, parsed.fields);
          return;
        }
        const firstNonEmpty = rows.findIndex((r) => (r || []).some((v) => String(v).trim() !== ""));
        if (firstNonEmpty !== -1) {
          parsed = rowsToObjects(rows, firstNonEmpty);
          handleRows(parsed.data, parsed.fields);
          return;
        }
        setStatus("Missing header row in XLSX. Need Work Date/Work Hours/Work Type.");
      }).catch((err) => {
        const msg = err && err.message ? err.message : "unknown error";
        setStatus(`Failed to parse XLSX: ${msg}`);
      });
      return;
    }

    setStatus("Parsing CSV...");
    Papa.parse(file, {
      header: true,
      skipEmptyLines: true,
      complete: (results) => {
        const fields = results.meta.fields || [];
        handleRows(results.data, fields);
      },
      error: () => {
        setStatus("Failed to parse CSV.");
      },
    });
  });

  document.querySelectorAll(".table-toggle").forEach((btn) => {
    btn.addEventListener("click", () => {
      const targetId = btn.getAttribute("data-target");
      const wrap = document.getElementById(targetId);
      const isHidden = wrap.hasAttribute("hidden");
      if (isHidden) {
        wrap.removeAttribute("hidden");
        btn.textContent = "Hide table";
      } else {
        wrap.setAttribute("hidden", "");
        btn.textContent = "Show table";
      }
    });
  });
</script>
